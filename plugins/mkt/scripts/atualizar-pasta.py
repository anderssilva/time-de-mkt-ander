#!/usr/bin/env python3
"""Alinha a pasta de uma empresa com o modelo da versão instalada do Time de Marketing.

Uso (de dentro da pasta da empresa):
  python3 atualizar-pasta.py .            mostra o que mudaria (não altera nada)
  python3 atualizar-pasta.py . --aplicar  aplica as mudanças

O que faz, sempre sem apagar e sem sobrescrever nada:
  1. aplica as migrações de estrutura registradas em modelos/migracoes.json para versões
     mais novas que a "Versão do modelo" da empresa (mover/renomear pastas e arquivos);
  2. cria as pastas e copia os arquivos do modelo que ainda não existem;
  3. acrescenta colunas novas nas planilhas de registro (registro.py iniciar);
  4. grava a nova "Versão do modelo" no status-implantacao.md.
Tudo o que for feito fica anotado em status-implantacao.md (seção "Atualizações da pasta").
"""
import json, os, re, shutil, subprocess, sys
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELO = os.path.join(RAIZ, "modelos", "empresa")
MIGRACOES = os.path.join(RAIZ, "modelos", "migracoes.json")
PULAR = (os.path.join("01-plano", "plano-AAAA-Tn.md"),)  # renomeado na implantação


def num(v):
    return tuple(int(x) for x in re.findall(r"\d+", v or "0")[:3]) or (0,)


def versao_plugin():
    with open(os.path.join(RAIZ, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
        return json.load(f)["version"]


def versao_empresa(pasta):
    st = os.path.join(pasta, "status-implantacao.md")
    if not os.path.exists(st):
        return None
    with open(st, encoding="utf-8") as f:
        m = re.search(r"Versão do modelo:\s*([\d.]+)", f.read())
    return m.group(1) if m else None


def plano(pasta):
    acoes = []
    atual = versao_empresa(pasta) or "0.0.0"
    # 1. migrações registradas
    if os.path.exists(MIGRACOES):
        with open(MIGRACOES, encoding="utf-8") as f:
            migs = json.load(f).get("migracoes", [])
        for m in sorted(migs, key=lambda x: num(x["versao"])):
            if num(m["versao"]) <= num(atual):
                continue
            for de, para in m.get("mover", []):
                o, d = os.path.join(pasta, de), os.path.join(pasta, para)
                if os.path.exists(o) and not os.path.exists(d):
                    acoes.append(("mover", de, para, m["versao"]))
    # 2. pastas e arquivos que faltam
    for raiz, dirs, arqs in os.walk(MODELO):
        rel_dir = os.path.relpath(raiz, MODELO)
        if rel_dir != "." and not os.path.isdir(os.path.join(pasta, rel_dir)):
            acoes.append(("criar-pasta", rel_dir, "", ""))
        for a in arqs:
            if a.startswith("."):
                continue
            rel = os.path.normpath(os.path.join(rel_dir, a))
            if rel in PULAR:
                continue
            if not os.path.exists(os.path.join(pasta, rel)):
                acoes.append(("copiar", rel, "", ""))
    return acoes


def aplicar(pasta, acoes, nova):
    feitos = []
    for tipo, a, b, ver in acoes:
        if tipo == "mover":
            os.makedirs(os.path.dirname(os.path.join(pasta, b)) or pasta, exist_ok=True)
            shutil.move(os.path.join(pasta, a), os.path.join(pasta, b))
            feitos.append(f"movido `{a}` → `{b}` (estrutura da versão {ver})")
        elif tipo == "criar-pasta":
            os.makedirs(os.path.join(pasta, a), exist_ok=True)
            feitos.append(f"pasta criada `{a}/`")
        elif tipo == "copiar":
            d = os.path.join(pasta, a)
            if os.path.exists(d):
                continue
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(os.path.join(MODELO, a), d)
            feitos.append(f"arquivo novo `{a}`")
    # 3. colunas novas no registro
    if os.path.isdir(os.path.join(pasta, "registro")):
        r = subprocess.run([sys.executable, os.path.join(RAIZ, "scripts", "registro.py"), "iniciar", pasta],
                           capture_output=True, text=True)
        for l in r.stdout.splitlines():
            if "colunas adicionadas" in l or "criado" in l:
                feitos.append(f"registro: {l.strip()}")
    # 4. versão e histórico no status
    st = os.path.join(pasta, "status-implantacao.md")
    if os.path.exists(st):
        with open(st, encoding="utf-8") as f:
            s = f.read()
        if re.search(r"Versão do modelo:\s*\S+", s):
            s = re.sub(r"Versão do modelo:\s*\S+", f"Versão do modelo: {nova}", s, count=1)
        else:
            s = s.rstrip() + f"\n\nVersão do modelo: {nova}\n"
        if "## Atualizações da pasta" not in s:
            s = s.rstrip() + "\n\n## Atualizações da pasta\n"
        s = s.rstrip() + f"\n- {date.today().strftime('%d/%m/%Y')} — versão {nova}: " + ("; ".join(feitos) if feitos else "nenhuma mudança de estrutura") + "\n"
        with open(st, "w", encoding="utf-8") as f:
            f.write(s)
    return feitos


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    pasta = a[0].rstrip("/") or "."
    if not os.path.isdir(pasta):
        sys.exit(f"Pasta não encontrada: {pasta}")
    if not os.path.exists(os.path.join(pasta, "status-implantacao.md")):
        sys.exit("Esta pasta não parece ser de uma empresa (não tem status-implantacao.md). Nada foi alterado.")
    nova, atual = versao_plugin(), versao_empresa(pasta)
    acoes = plano(pasta)
    if "--aplicar" not in a:
        print(f"Pasta da empresa: modelo {atual or 'sem versão registrada'} · time de marketing {nova}.")
        if not acoes and atual == nova:
            print("Nada a fazer: a pasta já está alinhada com o modelo atual.")
            return
        if acoes:
            print("Mudanças que serão feitas (nada é apagado nem sobrescrito):")
            for tipo, x, y, ver in acoes:
                print({"mover": f"  - mover {x} → {y}", "criar-pasta": f"  - criar pasta {x}/",
                       "copiar": f"  - copiar arquivo novo {x}"}[tipo])
        print("  - conferir colunas das planilhas de registro e registrar a versão no status-implantacao.md")
        return
    feitos = aplicar(pasta, acoes, nova)
    print(f"Pasta atualizada para o modelo {nova}.")
    for f in feitos:
        print(f"  - {f}")
    if not feitos:
        print("  - nenhuma mudança de estrutura; versão registrada.")


if __name__ == "__main__":
    main()
