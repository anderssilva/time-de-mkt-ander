#!/usr/bin/env python3
"""Guarda na pasta da empresa um arquivo que o usuário enviou no chat (ou indicou por caminho).

Uso (de dentro da pasta da empresa):
  python3 guardar-arquivo.py <arquivo> <destino> ["descrição curta"]

<destino> é uma pasta relativa à pasta da empresa. Atalhos:
  marca        00-contexto/materiais/marca          (logos, manual de marca, paleta)
  fotos        00-contexto/fotos                    (fotos reais de pessoas, bastidores, eventos)
  documentos   00-contexto/materiais/documentos     (apresentações, PDFs, textos, planilhas)
  redes        00-contexto/materiais/redes          (exportações e capturas das redes sociais)
  design       00-contexto/referencias-design       (referências de estilo, DESIGN.md)
  video-ref    00-contexto/referencias-video        (vídeos de referência, gravações de tela)
  trilhas      00-contexto/materiais/trilhas        (músicas e efeitos licenciados)
  outros       00-contexto/materiais/outros
Ou o caminho de uma peça, ex.: 03-producao/2026-10/S43_P012_tema/video-bruto

Regras: copia (nunca move o original), nunca sobrescreve (acrescenta -2, -3...), e anota
cada arquivo em 00-contexto/materiais/indice.md (data, nome original, onde ficou, descrição).
"""
import os, shutil, sys
from datetime import datetime

ATALHOS = {
    "marca": "00-contexto/materiais/marca",
    "fotos": "00-contexto/fotos",
    "documentos": "00-contexto/materiais/documentos",
    "redes": "00-contexto/materiais/redes",
    "design": "00-contexto/referencias-design",
    "video-ref": "00-contexto/referencias-video",
    "trilhas": "00-contexto/materiais/trilhas",
    "outros": "00-contexto/materiais/outros",
}
INDICE = os.path.join("00-contexto", "materiais", "indice.md")


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    origem, destino = a[0], ATALHOS.get(a[1], a[1]).strip("/")
    desc = a[2] if len(a) > 2 else ""
    if not os.path.isfile(origem):
        sys.exit(f"Arquivo não encontrado: {origem}")
    if os.path.isabs(destino) or ".." in destino.split("/"):
        sys.exit("O destino precisa ser uma pasta dentro da pasta da empresa.")
    if not os.path.exists("status-implantacao.md") and not os.path.isdir("00-contexto"):
        print("Aviso: a pasta atual não parece ser de uma empresa (sem status-implantacao.md ou 00-contexto/).", file=sys.stderr)
    os.makedirs(destino, exist_ok=True)
    nome = os.path.basename(origem)
    base, ext = os.path.splitext(nome)
    final, n = os.path.join(destino, nome), 2
    while os.path.exists(final):
        final = os.path.join(destino, f"{base}-{n}{ext}")
        n += 1
    shutil.copy2(origem, final)
    os.makedirs(os.path.dirname(INDICE), exist_ok=True)
    novo = not os.path.exists(INDICE)
    with open(INDICE, "a", encoding="utf-8") as f:
        if novo:
            f.write("# Materiais recebidos\n\nTudo o que foi enviado no chat e guardado na pasta da empresa.\n\n"
                    "| Data | Arquivo original | Onde ficou | Descrição |\n|---|---|---|---|\n")
        f.write(f"| {datetime.now().strftime('%d/%m/%Y %H:%M')} | {nome} | `{final}` | {desc} |\n")
    print(f"Guardado em {final}")


if __name__ == "__main__":
    main()
