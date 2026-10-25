#!/usr/bin/env python3
"""Mantém a pasta da empresa organizada: lista o que está fora do lugar e move com segurança.

Uso (de dentro da pasta da empresa):
  python3 organizar-pasta.py .                              lista o que está solto na raiz e sugere destino
  python3 organizar-pasta.py . --mover "<arquivo>" "<pasta>"  move um item (nunca sobrescreve) e anota no índice

Na raiz só ficam: LEIA-ME.md, status-implantacao.md, CLAUDE.md, pastas numeradas (00-, 01-...),
registro/, _lixeira/ e itens ocultos. Regras em referencias/organizacao-pasta.md do plugin.
"""
import os, re, shutil, sys
from datetime import datetime

PERMITIDOS = {"LEIA-ME.md", "status-implantacao.md", "CLAUDE.md", "registro", "_lixeira"}
INDICE = os.path.join("00-contexto", "materiais", "indice.md")
IMAGENS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic", ".svg")
VIDEOS = (".mp4", ".mov", ".m4v", ".webm")
DOCS = (".pdf", ".doc", ".docx", ".ppt", ".pptx", ".key", ".xls", ".xlsx", ".csv", ".txt", ".md")
LINKS_GOOGLE = (".gsheet", ".gdoc", ".gslides")


def sugestao(nome, pasta):
    base, ext = os.path.splitext(nome.lower())
    if ext in LINKS_GOOGLE:
        return "registro" if "registro" in base and ext == ".gsheet" else "00-contexto/materiais/documentos"
    if ext in IMAGENS or ext == ".pdf" and re.match(r"^(q|l|lamina|slide)?_?\d+", base):
        if re.match(r"^(q|l|lamina|slide|carrossel)?[_-]?\d{1,2}$", base) or "carrossel" in base:
            return "<pasta da peça>/carrossel  (pergunte de qual peça é)"
        if "logo" in base or "marca" in base:
            return "00-contexto/materiais/marca"
        return "00-contexto/fotos  ou  <pasta da peça>  (pergunte)"
    if ext in VIDEOS:
        return "<pasta da peça>/video-bruto  ou  00-contexto/referencias-video  (pergunte)"
    if ext in DOCS:
        return "00-contexto/materiais/documentos"
    if os.path.isdir(os.path.join(pasta, nome)):
        return "pasta fora do padrão: pergunte se é de uma peça, de materiais ou se vai para _lixeira"
    return "00-contexto/materiais/outros"


def listar(pasta):
    soltos = []
    for n in sorted(os.listdir(pasta)):
        if n.startswith(".") or n in PERMITIDOS or re.match(r"^\d\d-", n):
            continue
        soltos.append(n)
    if not soltos:
        print("Pasta organizada: nada solto na raiz.")
        return
    print(f"{len(soltos)} item(ns) fora do lugar na raiz da pasta da empresa:")
    for n in soltos:
        print(f"  - {n}  →  {sugestao(n, pasta)}")


def mover(pasta, item, destino):
    origem = os.path.join(pasta, item)
    if not os.path.exists(origem):
        sys.exit(f"Não encontrei: {item}")
    if os.path.isabs(destino) or ".." in destino.replace("\\", "/").split("/"):
        sys.exit("O destino precisa ser uma pasta dentro da pasta da empresa.")
    dpasta = os.path.join(pasta, destino)
    os.makedirs(dpasta, exist_ok=True)
    nome = os.path.basename(item.rstrip("/"))
    base, ext = os.path.splitext(nome)
    final, n = os.path.join(dpasta, nome), 2
    while os.path.exists(final):
        final = os.path.join(dpasta, f"{base}-{n}{ext}")
        n += 1
    shutil.move(origem, final)
    ind = os.path.join(pasta, INDICE)
    os.makedirs(os.path.dirname(ind), exist_ok=True)
    novo = not os.path.exists(ind)
    with open(ind, "a", encoding="utf-8") as f:
        if novo:
            f.write("# Materiais recebidos\n\nTudo o que foi enviado no chat ou organizado na pasta da empresa.\n\n"
                    "| Data | Arquivo original | Onde ficou | Descrição |\n|---|---|---|---|\n")
        f.write(f"| {datetime.now().strftime('%d/%m/%Y %H:%M')} | {nome} | `{os.path.relpath(final, pasta)}` | organizado (estava solto na raiz) |\n")
    print(f"Movido para {os.path.relpath(final, pasta)}")


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    pasta = a[0]
    if "--mover" in a:
        i = a.index("--mover")
        if len(a) < i + 3:
            sys.exit("Uso: organizar-pasta.py . --mover \"<arquivo>\" \"<pasta destino>\"")
        mover(pasta, a[i + 1], a[i + 2])
    else:
        listar(pasta)


if __name__ == "__main__":
    main()
