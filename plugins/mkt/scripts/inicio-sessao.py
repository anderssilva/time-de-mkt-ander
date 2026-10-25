#!/usr/bin/env python3
"""Início de sessão do Time de Marketing (chamado pelo gancho SessionStart do plugin).

1. Idioma: se o Claude Code ainda não estiver configurado para responder em português,
   acrescenta ao contexto da sessão que o usuário trabalha em português do Brasil.
2. Pasta de empresa: se a sessão foi aberta numa pasta de empresa, lembra que os arquivos
   enviados no chat devem ser guardados nela.
3. Versão: confere, no máximo uma vez por dia, se há versão nova (verificar-atualizacao.py --rapido).

Uso manual:
  python3 inicio-sessao.py                      o mesmo que o gancho faz
  python3 inicio-sessao.py --configurar-idioma  grava "language": "portuguese" nas configurações do usuário
                                                (~/.claude/settings.json), mantendo todo o resto
  python3 inicio-sessao.py --ver-idioma         mostra o idioma configurado
"""
import json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
IDIOMA = "portuguese"


def arq_config():
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    return os.path.join(base, "settings.json")


def ler_config():
    try:
        with open(arq_config(), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except ValueError:
        return None  # arquivo com erro: não mexer


def idioma_ok(cfg):
    lang = str((cfg or {}).get("language", "")).lower()
    return "portug" in lang or lang.startswith("pt")


def configurar_idioma():
    cfg = ler_config()
    if cfg is None:
        sys.exit(f"Não alterei nada: {arq_config()} tem um erro de formatação. Corrija o arquivo e rode de novo.")
    if idioma_ok(cfg):
        print(f"O idioma já está em português ({cfg.get('language')}).")
        return
    anterior = cfg.get("language")
    cfg["language"] = IDIOMA
    os.makedirs(os.path.dirname(arq_config()), exist_ok=True)
    tmp = arq_config() + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, arq_config())
    print(f"Idioma configurado: \"language\": \"{IDIOMA}\" em {arq_config()}"
          + (f" (antes: {anterior})." if anterior else ".")
          + " Vale para as próximas sessões do Claude Code.")


def main():
    a = sys.argv[1:]
    if "--configurar-idioma" in a:
        configurar_idioma()
        return
    if "--ver-idioma" in a:
        cfg = ler_config() or {}
        print(cfg.get("language") or "(não configurado: o Claude Code usa o idioma da conversa)")
        return

    linhas = []
    if not idioma_ok(ler_config()):
        linhas.append("O usuário trabalha em português do Brasil e espera todas as respostas, perguntas, avisos de "
                      "andamento e arquivos em português do Brasil, inclusive quando ferramentas ou erros aparecem em inglês. "
                      "O idioma padrão do Claude Code ainda não está em português; o comando /mkt:atualizar-time faz essa "
                      "configuração com a autorização do usuário.")
    proj = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    if os.path.exists(os.path.join(proj, "status-implantacao.md")) or os.path.isdir(os.path.join(proj, "00-contexto")):
        linhas.append("Esta pasta é a pasta de marketing de uma empresa. Todo arquivo que o usuário enviar no chat deve ser "
                      "guardado nela, na subpasta certa, com o programa guardar-arquivo.py do plugin mkt "
                      "(regras em referencias/arquivos-recebidos.md do plugin). Nenhum arquivo fica solto na raiz da pasta: cada "
                      "arquivo vai direto para o lugar certo (referencias/organizacao-pasta.md do plugin).")
    try:
        r = subprocess.run([sys.executable, os.path.join(AQUI, "verificar-atualizacao.py"), "--rapido"],
                           capture_output=True, text=True, timeout=25)
        if r.stdout.strip():
            linhas.append(r.stdout.strip())
    except (OSError, subprocess.TimeoutExpired):
        pass
    if linhas:
        print("Time de Marketing:\n" + "\n".join(linhas))


if __name__ == "__main__":
    main()
