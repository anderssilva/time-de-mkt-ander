#!/usr/bin/env python3
"""Tira a "cara de IA" de um texto em português antes de ele chegar ao responsável.

Uso:
  python3 humanizar.py texto.md                 detecta e dá a nota (não altera nada)
  python3 humanizar.py texto.md --aplicar       corrige o que é seguro corrigir sozinho e grava texto.md
  python3 humanizar.py --texto "..."            analisa um texto curto
  python3 humanizar.py texto.md --json

Cinco verificações (nota final de 0 a 100; 80 ou mais = pode ir; abaixo disso, reescreva os trechos apontados):
  1. INVISÍVEIS    caracteres invisíveis e marcas d'água (sempre removidos com --aplicar)
  2. PONTUAÇÃO     travessões (—) e reticências em excesso, aspas e símbolos tipográficos de IA
  3. PALAVRAS      vocabulário típico de texto gerado ("crucial", "alavancar", "jornada", "no cenário atual"...)
  4. ESTRUTURAS    fórmulas de IA ("não é apenas X, é Y", "Imagine...", "Em resumo", três adjetivos seguidos...)
  5. RITMO         frases todas do mesmo tamanho, excesso de emojis, listas em tudo

--aplicar só mexe no que não muda o sentido (invisíveis, travessões, espaços). Palavras e estruturas
são apontadas com sugestão: quem reescreve é o redator, no tom de voz da empresa.

Ideia adaptada do humanizer do projeto instagram-agent-skill (Jake Schincariol, licença MIT);
listas próprias para o português do Brasil.
"""
import json, re, statistics, sys

INVISIVEIS = {
    "​": "", "‌": "", "‍": "", "⁠": "", "﻿": "", "­": "", "᠎": "",
    "؜": "", "‎": "", "‏": "", "‪": "", "‫": "", "‬": "", "‭": "", "‮": "",
    " ": " ", " ": " ", " ": " ", " ": " ",
}
TAGS = re.compile("[\U000E0000-\U000E007F]")

PALAVRAS = {  # palavra ou expressão -> sugestão
    "crucial": "importante (ou diga por quê)", "fundamental": "diga o efeito concreto", "essencial": "diga o efeito concreto",
    "alavanc*": "aumentar / usar", "potencializ*": "aumentar", "otimiz*": "melhorar / acertar", "maximiz*": "aumentar",
    "impulsion*": "aumentar", "desbloque*": "liberar / conseguir", "elevar": "melhorar", "transformador*": "corte",
    "revolucion*": "corte ou \"mudar\"", "inovador": "diga o que é novo", "robusto": "sólido / completo",
    "sinergia": "corte", "holístico": "completo", "disruptivo": "corte", "jornada": "caminho / processo",
    "mergulh*": "ver / entender", "navegar": "lidar com",
    "no cenário atual": "hoje", "nos dias de hoje": "hoje", "em um mundo cada vez mais": "corte a frase de abertura",
    "num mundo cada vez mais": "corte a frase de abertura", "vale ressaltar": "corte", "vale destacar": "corte",
    "é importante destacar": "corte", "é importante ressaltar": "corte", "é importante lembrar": "corte",
    "não podemos esquecer": "corte", "em suma": "corte", "em resumo": "corte", "em conclusão": "corte",
    "por fim, mas não menos importante": "por fim", "além disso,": "e / também (varie)", "nesse sentido": "corte",
    "dessa forma": "assim", "desta forma": "assim", "de forma eficaz": "corte ou diga como", "de maneira eficiente": "corte ou diga como",
    "eficaz": "que funciona", "ecossistema": "diga o que é", "paradigma": "corte", "tapeçaria": "corte",
    "panorama": "situação", "fomentar": "estimular", "catalisar": "acelerar", "agregar valor": "diga o ganho",
    "game changer": "corte", "next level": "corte", "insights": "conclusões (ideias)", "insight": "ideia",
    "gamechanger": "corte", "descubra": "veja", "o segredo": "diga qual é", "simplesmente": "corte",
    "verdadeiramente": "corte", "absolutamente": "corte", "extremamente": "muito (ou corte)", "incrivelmente": "corte",
}
ESTRUTURAS = [
    (re.compile(r"(?i)\bn[aã]o (?:é|e) (?:apenas|s[oó]|somente) [^.!?]{2,60}[,;—-]\s*(?:é|e|mas)\b"), "\"Não é apenas X, é Y\": diga direto o que é."),
    (re.compile(r"(?im)^\s*imagine\b"), "Abertura com \"Imagine...\": comece pelo fato ou pela história real."),
    (re.compile(r"(?im)^\s*(?:em resumo|em suma|concluindo|para concluir)\b"), "Fecho com \"Em resumo\": termine com a ação ou a pergunta."),
    (re.compile(r"(?i)\b(?:mais do que (?:nunca|apenas))\b"), "\"Mais do que nunca\": clichê de abertura."),
    (re.compile(r"(?i)\b(\w{4,}), (\w{4,}) e (\w{4,})\b(?= (?:para|que|em|de)\b)"), "Três palavras em série (ritmo de IA): fique com a mais forte."),
    (re.compile(r"(?i)\bquer (?:saber|descobrir) (?:como|o que)[^?]{0,60}\?"), "Pergunta retórica de gancho genérico: troque por uma afirmação concreta."),
    (re.compile(r"(?i)\bseja (?:você|voce) [^,]{3,40} ou [^,]{3,40},"), "\"Seja você X ou Y\": genérico; fale com um público só."),
    (re.compile(r"(?im)^.{0,80}:\s*$\n(?:\s*[-•✅✔️👉]\s.+\n){3,}"), "Lista logo após dois-pontos em todo bloco: varie, use frase corrida às vezes."),
]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def analisar(t):
    achados = {"INVISÍVEIS": [], "PONTUAÇÃO": [], "PALAVRAS": [], "ESTRUTURAS": [], "RITMO": []}
    inv = sum(t.count(c) for c in INVISIVEIS if c not in (" ",)) + len(TAGS.findall(t))
    if inv:
        achados["INVISÍVEIS"].append(f"{inv} caractere(s) invisível(is) ou marca d'água")
    trav = t.count("—") + t.count("–")
    if trav:
        achados["PONTUAÇÃO"].append(f"{trav} travessão(ões): troque por vírgula, ponto ou dois-pontos")
    if len(re.findall(r"\.\.\.|…", t)) > 2:
        achados["PONTUAÇÃO"].append("reticências em excesso")
    baixo = t.lower()
    for p, sug in PALAVRAS.items():
        rx = r"(?<!\w)" + re.escape(p[:-1]) + r"\w*" if p.endswith("*") else r"(?<!\w)" + re.escape(p) + r"(?!\w)"
        n = len(re.findall(rx, baixo))
        if n:
            achados["PALAVRAS"].append(f"\"{p[:-1] + '…' if p.endswith('*') else p}\" ({n}x) → {sug}")
    for rx, msg in ESTRUTURAS:
        if rx.search(t):
            achados["ESTRUTURAS"].append(msg)
    frases = [f for f in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", t)) if len(f.split()) >= 3]
    if len(frases) >= 5:
        tams = [len(f.split()) for f in frases]
        if statistics.pstdev(tams) < 3.5:
            achados["RITMO"].append("frases todas do mesmo tamanho: alterne frases curtas e longas")
    em = len(EMOJI.findall(t))
    pal = max(1, len(t.split()))
    if em > 3 and em / pal > 0.03:
        achados["RITMO"].append(f"{em} emojis: use no máximo 1 ou 2, onde fizerem sentido")
    pesos = {"INVISÍVEIS": 25, "PONTUAÇÃO": 8, "PALAVRAS": 7, "ESTRUTURAS": 10, "RITMO": 8}
    tetos = {"INVISÍVEIS": 25, "PONTUAÇÃO": 15, "PALAVRAS": 35, "ESTRUTURAS": 30, "RITMO": 15}
    perda = 0
    for k, lst in achados.items():
        if k == "PALAVRAS":
            qtd = sum(int(re.search(r"\((\d+)x\)", x).group(1)) for x in lst)
        elif k == "PONTUAÇÃO":
            qtd = trav + (1 if len(lst) > (1 if trav else 0) else 0)
        else:
            qtd = len(lst)
        perda += min(tetos[k], pesos[k] * qtd)
    nota = max(0, 100 - perda)
    return {"nota": nota, "pode_ir": nota >= 80, "achados": achados}


def corrigir(t):
    for c, r in INVISIVEIS.items():
        t = t.replace(c, r)
    t = TAGS.sub("", t)
    t = re.sub(r"\s*[—–]\s*(?=\w)", ", ", t)          # travessão no meio da frase vira vírgula
    t = re.sub(r"\s*[—–]\s*$", ".", t, flags=re.M)
    t = re.sub(r",\s*,", ",", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    js = "--json" in a
    if "--texto" in a:
        t, arq = a[a.index("--texto") + 1], None
    else:
        arq = a[0]
        with open(arq, encoding="utf-8") as f:
            t = f.read()
    if "--aplicar" in a:
        novo = corrigir(t)
        if arq and novo != t:
            with open(arq, "w", encoding="utf-8") as f:
                f.write(novo)
            print(f"Correções seguras aplicadas em {arq} (invisíveis, travessões, espaços).")
        t = novo
    r = analisar(t)
    if js:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    print(f"CARA DE IA · nota {r['nota']}/100 · {'pode ir' if r['pode_ir'] else 'reescreva os pontos abaixo antes de mostrar'}")
    for k, lst in r["achados"].items():
        for x in lst:
            print(f"  [{k}] {x}")


if __name__ == "__main__":
    main()
