#!/usr/bin/env python3
"""Dá nota aos ganchos (primeira frase de um vídeo ou capa) antes de gravar.

Uso:
  python3 gancho.py "Perdi R$ 18 mil por causa de uma cláusula" "Oi pessoal, hoje vou falar de contratos"
  python3 gancho.py --arquivo ganchos.txt          (um gancho por linha)
  python3 gancho.py --json ...

Cinco critérios (0 a 100 cada) e uma nota final ponderada:
  TAMANHO       cabe em ~3 segundos falados (até 12 palavras; ideal 6 a 10)
  CONCRETO      tem número, valor, prazo, nome ou objeto específico
  RISCO         mostra o que se ganha ou se perde (dinheiro, tempo, erro, cliente)
  INÍCIO        as primeiras palavras já entregam o assunto (sem saudação, sem enrolação)
  CONVERSA      fala com alguém ("você", "seu", "sua empresa") ou em primeira pessoa com história
Eliminatórios (derrubam a nota): saudação, "neste vídeo", "pare de rolar", pedir atenção.

Adaptado para português a partir da ideia do hookscore do projeto instagram-agent-skill
(Jake Schincariol, licença MIT). Listas e pesos próprios, pensados para o português do Brasil.
"""
import json, re, sys, unicodedata

PALAVRA = re.compile(r"[\wÀ-ÿ$%R]+", re.U)
NUMERO = re.compile(r"(?:R\$\s?)?\d[\d.,]*\s?(?:%|mil|milhões?|bi|k|dias?|horas?|minutos?|meses|anos?|x)?", re.I)
NUM_EXTENSO = set("um uma dois duas três quatro cinco seis sete oito nove dez doze quinze vinte trinta cem mil milhão milhões metade dobro triplo".split())
RISCO = set("""perdi perder perde perdeu prejuízo prejuizo quebrou quebrar faliu falência erro errado erros
caro custou custa caiu cair demitir demiti multa processo risco cancelou cancelar sumiu atrasou atraso nada perde desperdiça desperdício trava travou
ganhei ganhar dobrei dobrar triplicou lucro faturei faturamento economizei economia vendi vender cliente
clientes contrato contratos dinheiro tempo noite noites sozinho problema nunca ninguém segredo
""".split())
IMPERATIVO = set("pare evite faça use corte nunca jamais esqueça troque mude comece aprenda veja anote salve".split())
VOCE = set("você voce vocês seu sua seus suas teu tua te contigo".split())
PRIMEIRA = set("eu meu minha meus minhas perdi ganhei errei aprendi descobri fiz".split())
ENROLACAO = ["então", "bom", "olha", "gente", "galera", "pessoal", "hoje eu", "hoje vou", "hoje a gente",
             "nesse vídeo", "neste vídeo", "no vídeo de hoje", "vamos falar", "quero falar", "vou falar"]
ELIMINATORIOS = [
    (re.compile(r"(?i)^\s*(?:oi|olá|ola|e a[ií]|fala|bom dia|boa tarde|boa noite|tudo bem)\b"),
     "Começa com saudação. Ninguém entrou no feed para ser cumprimentado."),
    (re.compile(r"(?i)\b(?:neste|nesse|no) (?:vídeo|video|reels?)( de hoje)?\b|\bvou (?:te )?mostrar\b|\bhoje (?:eu )?vou\b"),
     "Anuncia o vídeo em vez de entregar. Comece pelo conteúdo."),
    (re.compile(r"(?i)\b(?:pare de rolar|n[aã]o role|n[aã]o pule|espera a[ií]|presta aten[cç][aã]o|assiste at[eé] o final)\b"),
     "Pede atenção. Pedir atenção mostra que o gancho ainda não ganhou."),
    (re.compile(r"(?i)^\s*(?:voc[eê] sabia que)\b"),
     "\"Você sabia que\" virou fórmula gasta. Diga o fato direto."),
]


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFKD", t.lower()) if not unicodedata.combining(c))


def palavras(t):
    return [p for p in PALAVRA.findall(t)]


def nota(g):
    ps = palavras(g)
    n = len(ps)
    low = [p.lower() for p in ps]
    base = [sem_acento(p) for p in ps]
    # TAMANHO
    if n == 0:
        tam = 0
    elif 6 <= n <= 10:
        tam = 100
    elif n <= 5:
        tam = 70 if n >= 3 else 40
    elif n <= 12:
        tam = 80
    elif n <= 16:
        tam = 45
    else:
        tam = 15
    # CONCRETO
    nums = len(NUMERO.findall(g)) + sum(1 for p in low if p in NUM_EXTENSO)
    proprios = len(re.findall(r"(?<!^)(?<![.!?]\s)\b[A-ZÁÉÍÓÚÂÊÔÃÕ][a-záéíóúâêôãõç]{2,}", g))
    conc = min(100, 35 + 40 * min(nums, 2) + 15 * min(proprios, 1)) if (nums or proprios) else 30
    # RISCO
    r = sum(1 for p in base if p in {sem_acento(x) for x in RISCO})
    risco = min(100, 40 + 30 * r) if r else 35
    # INÍCIO
    inicio3 = " ".join(low[:3])
    ini = 100
    for e in ENROLACAO:
        if " ".join(low[:5]).startswith(e) or inicio3.startswith(e):
            ini = 20
            break
    if ini == 100 and low and low[0] in ("então", "bom", "é", "tipo", "assim"):
        ini = 40
    # CONVERSA
    if any(p in VOCE for p in low) or (low and low[0] in IMPERATIVO):
        conv = 100
    elif any(p in PRIMEIRA for p in low):
        conv = 85
    else:
        conv = 55
    criterios = {"TAMANHO": tam, "CONCRETO": conc, "RISCO": risco, "INÍCIO": ini, "CONVERSA": conv}
    pesos = {"TAMANHO": .2, "CONCRETO": .25, "RISCO": .2, "INÍCIO": .2, "CONVERSA": .15}
    final = sum(criterios[k] * pesos[k] for k in pesos)
    genericas = {"importante", "fundamental", "essencial", "dica", "dicas", "incrível", "incrivel", "sucesso", "segredos"}
    if any(p in genericas for p in low) and conc < 50 and risco < 50:
        final = min(final, 48.0)
    elif conc < 50 and risco < 50:
        final = min(final, 58.0)
    problemas = [msg for rx, msg in ELIMINATORIOS if rx.search(g)]
    if problemas:
        final *= 0.45
    final = round(final, 1)
    faixa = "FORTE" if final >= 75 else "OK" if final >= 55 else "FRACO"
    pior = min(criterios, key=criterios.get)
    return {"gancho": g, "nota": final, "faixa": faixa, "palavras": n, "segundos": round(n / 2.6, 1),
            "criterios": criterios, "mais_fraco": pior, "eliminatorios": problemas}


DICAS = {
    "TAMANHO": "Corte para 6 a 10 palavras: precisa caber em 3 segundos.",
    "CONCRETO": "Coloque um número, valor, prazo ou nome concreto.",
    "RISCO": "Mostre o que se ganha ou se perde (dinheiro, tempo, cliente, erro).",
    "INÍCIO": "Tire a enrolação do começo; a primeira palavra já deve ser o assunto.",
    "CONVERSA": "Fale com a pessoa (\"você\", \"sua empresa\") ou conte em primeira pessoa.",
}


def main():
    a = sys.argv[1:]
    js = "--json" in a
    a = [x for x in a if x != "--json"]
    if "--arquivo" in a:
        with open(a[a.index("--arquivo") + 1], encoding="utf-8") as f:
            ganchos = [l.strip() for l in f if l.strip()]
    else:
        ganchos = a
    if not ganchos:
        sys.exit(__doc__)
    res = sorted((nota(g) for g in ganchos), key=lambda r: -r["nota"])
    if js:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print("NOTA DOS GANCHOS")
    print("=" * 72)
    for i, r in enumerate(res):
        seta = "->" if i == 0 else "  "
        print(f"{seta} {r['nota']:5.1f} {r['faixa']:<6} {r['gancho'][:60]}")
        print(f"         {r['palavras']} palavras (~{r['segundos']} s) · mais fraco: {r['mais_fraco']} ({r['criterios'][r['mais_fraco']]}) — {DICAS[r['mais_fraco']]}")
        for e in r["eliminatorios"]:
            print(f"         ELIMINATÓRIO: {e}")


if __name__ == "__main__":
    main()
