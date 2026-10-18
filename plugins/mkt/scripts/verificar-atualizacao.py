#!/usr/bin/env python3
"""Confere se o plugin mkt instalado está na última versão publicada no GitHub
e, opcionalmente, se a pasta de uma empresa está alinhada com o modelo atual.

Uso:
  python3 verificar-atualizacao.py                     confere agora e mostra o resultado
  python3 verificar-atualizacao.py --rapido            para o início de sessão: no máximo 1 consulta a cada 20 h,
                                                       e só escreve algo se houver novidade
  python3 verificar-atualizacao.py --aplicar           atualiza o catálogo e o plugin (pede /reload-plugins depois)
  python3 verificar-atualizacao.py --empresa empresas/<slug>
                                                       também confere a pasta da empresa contra o modelo

Como descobre a última versão (na ordem, até uma funcionar):
  1. cópia do catálogo que o Claude Code mantém no computador (git fetch, sem alterar nada);
  2. GitHub pela ferramenta gh (usa o login já feito);
  3. endereço público do arquivo (só funciona se o repositório for público).
Sem internet ou sem acesso, avisa e segue: nunca bloqueia o trabalho.
"""
import json, os, re, subprocess, sys, time, urllib.request
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(RAIZ, "catalogo.json"), encoding="utf-8") as _f:
    CFG = json.load(_f)
CAT, PLUGIN, REPO, RAMO = CFG["catalogo"], CFG["plugin"], CFG["repositorio"], CFG.get("ramo", "main")
CAMINHO_FICHA = f"plugins/{PLUGIN}/.claude-plugin/plugin.json"
CAMINHO_HIST = "CHANGELOG.md"
INTERVALO_H = 20


def rodar(cmd, timeout=40, cwd=None):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        return r.returncode, r.stdout
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""


def num(v):
    return tuple(int(x) for x in re.findall(r"\d+", v or "0")[:3]) or (0,)


def versao_local():
    with open(os.path.join(RAIZ, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
        return json.load(f).get("version", "0.0.0")


def pasta_catalogo():
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    p = os.path.join(base, "plugins", "marketplaces", CAT)
    return p if os.path.isdir(os.path.join(p, ".git")) else None


def remoto_git():
    p = pasta_catalogo()
    if not p:
        return None
    ok, _ = rodar(["git", "-C", p, "fetch", "--quiet", "--depth", "1", "origin", RAMO])
    if ok != 0:
        return None
    _, ficha = rodar(["git", "-C", p, "show", f"FETCH_HEAD:{CAMINHO_FICHA}"])
    _, hist = rodar(["git", "-C", p, "show", f"FETCH_HEAD:{CAMINHO_HIST}"])
    return (ficha, hist) if ficha.strip() else None


def remoto_gh():
    def pega(caminho):
        ok, out = rodar(["gh", "api", f"repos/{REPO}/contents/{caminho}?ref={RAMO}",
                         "-H", "Accept: application/vnd.github.raw"])
        return out if ok == 0 else ""
    ficha = pega(CAMINHO_FICHA)
    return (ficha, pega(CAMINHO_HIST)) if ficha.strip() else None


def remoto_publico():
    def pega(caminho):
        try:
            with urllib.request.urlopen(f"https://raw.githubusercontent.com/{REPO}/{RAMO}/{caminho}", timeout=15) as r:
                return r.read().decode("utf-8")
        except Exception:
            return ""
    ficha = pega(CAMINHO_FICHA)
    return (ficha, pega(CAMINHO_HIST)) if ficha.strip() else None


def versao_remota():
    for f in (remoto_git, remoto_gh, remoto_publico):
        r = f()
        if r:
            try:
                return json.loads(r[0]).get("version"), r[1]
            except ValueError:
                continue
    return None, ""


def novidades(hist, local):
    """Trechos do CHANGELOG com versão maior que a instalada."""
    partes, atual = [], None
    for linha in hist.splitlines():
        m = re.match(r"##\s+(\d+\.\d+\.\d+)", linha)
        if m:
            atual = m.group(1) if num(m.group(1)) > num(local) else None
        if atual:
            partes.append(linha)
    return "\n".join(partes).strip()


def arq_cache():
    base = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.expanduser("~/.cache/time-de-mkt")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "verificacao.json")


def ler_cache():
    try:
        with open(arq_cache(), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def gravar_cache(d):
    try:
        with open(arq_cache(), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
    except OSError:
        pass


def comandos():
    return (f"claude plugin marketplace update {CAT} && claude plugin update {PLUGIN}@{CAT}", "/reload-plugins")


def conferir_empresa(pasta, local):
    modelo = os.path.join(RAIZ, "modelos", "empresa")
    if not os.path.isdir(pasta):
        print(f"Pasta da empresa não encontrada: {pasta}")
        return
    faltam = []
    for raiz, _, arqs in os.walk(modelo):
        for a in arqs:
            if a.startswith("."):
                continue
            rel = os.path.relpath(os.path.join(raiz, a), modelo)
            if rel.startswith("01-plano" + os.sep + "plano-AAAA"):
                continue  # renomeado na implantação
            if not os.path.exists(os.path.join(pasta, rel)):
                faltam.append(rel)
    versao_emp = None
    st = os.path.join(pasta, "status-implantacao.md")
    if os.path.exists(st):
        with open(st, encoding="utf-8") as f:
            m = re.search(r"Versão do modelo:\s*([\d.]+)", f.read())
            versao_emp = m.group(1) if m else None
    print(f"Pasta {pasta}: modelo {versao_emp or 'sem versão registrada'} · plugin {local}.")
    if faltam:
        print("Arquivos novos do modelo que esta empresa ainda não tem (copiar sem sobrescrever nada):")
        for f in sorted(faltam):
            print(f"  - {f}")
    elif versao_emp == local:
        print("Pasta alinhada com o modelo atual.")
    else:
        print("Nenhum arquivo faltando. Registre 'Versão do modelo: " + local + "' no status-implantacao.md.")


def main():
    a = sys.argv[1:]
    rapido, aplicar = "--rapido" in a, "--aplicar" in a
    empresa = a[a.index("--empresa") + 1] if "--empresa" in a and a.index("--empresa") + 1 < len(a) else None
    local = versao_local()
    cache = ler_cache()

    if rapido and time.time() - cache.get("quando", 0) < INTERVALO_H * 3600:
        remota, hist = cache.get("remota"), cache.get("hist", "")
    else:
        remota, hist = versao_remota()
        if remota:
            gravar_cache({"quando": time.time(), "remota": remota, "hist": hist})

    cmd_shell, cmd_sessao = comandos()
    if not remota:
        if not rapido:
            print(f"Time de Marketing {local} instalado. Não foi possível consultar a última versão agora "
                  f"(sem internet ou sem acesso ao GitHub). Siga normalmente e confira depois.")
    elif num(remota) > num(local):
        print(f"Há uma versão nova do Time de Marketing: {remota} (instalada: {local}).")
        txt = novidades(hist, local)
        if txt:
            print("O que mudou:\n" + txt[:3000])
        if aplicar:
            ok, out = rodar(["sh", "-c", cmd_shell], timeout=180)
            print(out.strip())
            print("Atualização baixada." if ok == 0 else "A atualização falhou; rode no Terminal: " + cmd_shell)
            print(f"Para começar a usar agora, digite {cmd_sessao} (ou abra uma sessão nova).")
        else:
            print(f"Para atualizar: peça 'atualiza o time de marketing' ou rode no Terminal: {cmd_shell} "
                  f"e depois digite {cmd_sessao}.")
    elif not rapido:
        print(f"Time de Marketing atualizado (versão {local}).")

    if empresa:
        conferir_empresa(empresa.rstrip("/"), local)


if __name__ == "__main__":
    main()
