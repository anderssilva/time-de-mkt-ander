#!/usr/bin/env python3
"""Confere a legenda de um post do Instagram antes de publicar.

Uso:
  python3 legenda.py legenda.txt [--json]
  python3 legenda.py --texto "..."

Mostra exatamente o que aparece no feed antes do "... mais" (cerca de 125 caracteres) e avisa:
  - a primeira linha não segura sozinha (curta demais, começa com saudação, emoji ou hashtag);
  - mais de 3 hashtags (o recomendado hoje é 3 a 5 bem específicas; o time usa até 3);
  - mais de uma chamada para ação (peça uma coisa só);
  - link na legenda (não é clicável no Instagram: use "link na bio" ou palavra-chave);
  - legenda acima de 2.200 caracteres (limite do Instagram) ou bloco de texto sem respiro;
  - sinais de "cara de IA" (usa o humanizar.py).

Ideia adaptada do caption.py do projeto instagram-agent-skill (Jake Schincariol, licença MIT).
"""
import json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import humanizar  # noqa: E402

CTA = re.compile(r"(?i)\b(?:salve|salva|comente|comenta|compartilhe|manda para|envie|chame|me chama|clique|acesse|link na bio|agende|baixe|inscreva|siga|marque)\b")
SAUDACAO = re.compile(r"(?i)^\s*(?:oi|olá|ola|bom dia|boa tarde|boa noite|e a[ií]|fala)\b")
LINK = re.compile(r"https?://\S+|\bwww\.\S+|\b[\w-]+\.(?:com|com\.br|br|io|app|net|org)\b(?:/\S*)?", re.I)
EMOJI_INI = re.compile("^[\U0001F300-\U0001FAFF☀-➿]")


def checar(t):
    t = t.strip()
    avisos = []
    previa = t.replace("\n", " ")[:125]
    primeira = t.splitlines()[0] if t else ""
    if len(primeira) < 25:
        avisos.append("A primeira linha é curta demais para segurar sozinha: ela é o gancho da legenda.")
    if SAUDACAO.search(primeira):
        avisos.append("A legenda começa com saudação: comece pelo assunto.")
    if EMOJI_INI.search(primeira) or primeira.startswith("#"):
        avisos.append("A legenda começa com emoji ou hashtag: comece com palavras.")
    tags = re.findall(r"(?<!\w)#\w+", t)
    if len(tags) > 3:
        avisos.append(f"{len(tags)} hashtags: use até 3, específicas do assunto e do público.")
    ctas = len(CTA.findall(t))
    if ctas > 2:
        avisos.append(f"{ctas} pedidos de ação: peça uma coisa só (salvar, comentar uma palavra, link na bio).")
    if ctas == 0:
        avisos.append("Sem chamada para ação: termine pedindo uma coisa (a do funil).")
    if LINK.search(t):
        avisos.append("Link na legenda não é clicável no Instagram: use \"link na bio\" ou uma palavra-chave para receber por mensagem.")
    if len(t) > 2200:
        avisos.append(f"{len(t)} caracteres: o limite do Instagram é 2.200.")
    if any(len(b) > 400 for b in re.split(r"\n\s*\n", t)):
        avisos.append("Há um bloco de texto longo sem respiro: quebre em parágrafos curtos.")
    ia = humanizar.analisar(t)
    if not ia["pode_ir"]:
        avisos.append(f"Cara de IA: nota {ia['nota']}/100. Rode humanizar.py e reescreva os pontos apontados.")
    return {"previa": previa, "caracteres": len(t), "hashtags": len(tags), "avisos": avisos, "nota_ia": ia["nota"]}


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if "--texto" in a:
        t = a[a.index("--texto") + 1]
    else:
        with open(a[0], encoding="utf-8") as f:
            t = f.read()
    r = checar(t)
    if "--json" in a:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    print("O QUE APARECE ANTES DO \"... mais\":")
    print(f"  {r['previa']}{'... mais' if r['caracteres'] > 125 else ''}")
    print(f"{r['caracteres']} caracteres · {r['hashtags']} hashtags · cara de IA {r['nota_ia']}/100")
    if r["avisos"]:
        for x in r["avisos"]:
            print(f"  - {x}")
    else:
        print("  Tudo certo.")


if __name__ == "__main__":
    main()
