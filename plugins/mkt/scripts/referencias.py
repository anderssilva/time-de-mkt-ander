#!/usr/bin/env python3
"""Arquivo de referências do nicho: ordena vídeos de outros perfis por quanto superaram a própria conta.

Uso (de dentro da pasta da empresa):
  python3 referencias.py 02-pautas/referencias-nicho.tsv [--saida 02-pautas/arquivo-referencias.md] [--json]

O .tsv (separado por tabulação, com cabeçalho) é preenchido enquanto se navega, uma linha por vídeo:
  perfil	seguidores	mediana	visualizacoes	gancho	formato	link
  @perfil	48000	11000	412000	ninguém te conta que...	reels	https://...

- mediana = visualizações típicas recentes daquele perfil (a melhor base). Sem ela, usa seguidores (avisa).
- O que importa é o MÚLTIPLO (visualizações ÷ mediana): 2 milhões de seguidores com 400 mil visualizações
  foi um dia comum; 4 mil seguidores com 400 mil visualizações achou algo que vale estudar.
- Cada gancho recebe a nota do gancho.py e a fórmula mais provável (referencias/ganchos.md).

Ideia adaptada do swipe.py do projeto instagram-agent-skill (Jake Schincariol, licença MIT).
"""
import csv, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gancho as G  # noqa: E402

FORMULAS = [
    ("Custo do erro", r"\b(?:custou|perdi|preju[ií]zo|r\$)"), ("Pare e troque", r"^\s*(?:pare|para) de\b"),
    ("Ninguém te conta", r"ningu[eé]m (?:te )?(?:conta|fala|diz)"), ("Antes e depois de tempo", r"\b(?:levava|demorava)\b.*\b(?:hoje|agora)\b"),
    ("O recibo", r"\bfiz(?:emos)? .* por \d+"), ("Errado sem culpa", r"jeito errado|est[aá] errando"),
    ("Dos bastidores", r"\b(?:anos|dentro d[ae])\b.*\b(?:nunca|ningu[eé]m)\b"), ("Leve este modelo", r"\b(?:copie|pegue|roube|use) (?:este|esse|essa|esta)\b"),
    ("Se isto, então veja", r"^\s*se (?:voc[eê]|sua|seu)\b"), ("Lista com favorito", r"^\s*\d+ \w+"),
    ("A pergunta real", r"^\s*[\"“].+\?[\"”]"), ("Um contra o outro", r"\b(?:ou|vs\.?|versus|contra)\b.*\?"),
    ("Permissão", r"voc[eê] n[aã]o precisa"), ("O número", r"\d+\s?%"), ("O único", r"\b(?:único|mais r[aá]pido|melhor) jeito\b"),
]


def num(v):
    v = str(v or "").strip().lower().replace(".", "").replace(",", ".")
    mult = 1
    if v.endswith("k") or v.endswith("mil"):
        mult, v = 1000, v.rstrip("k").replace("mil", "").strip()
    elif v.endswith("m") or "mi" in v:
        mult, v = 1_000_000, re.sub(r"(mi|m)$", "", v).strip()
    try:
        return float(v) * mult
    except ValueError:
        return None


def formula(g):
    for nome, rx in FORMULAS:
        if re.search(rx, g or "", re.I):
            return nome
    return "—"


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    with open(a[0], encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter="\t"))
    itens, sem_mediana = [], 0
    for l in linhas:
        v = num(l.get("visualizacoes"))
        base = num(l.get("mediana"))
        if not base:
            seg = num(l.get("seguidores"))
            base = seg * 0.1 if seg else None   # aproximação grosseira: 10% dos seguidores
            sem_mediana += 1
        if not v or not base:
            continue
        g = (l.get("gancho") or "").strip()
        nota = G.nota(g)["nota"] if g else None
        itens.append({"perfil": l.get("perfil"), "multiplo": round(v / base, 1), "visualizacoes": int(v), "gancho": g,
                      "nota_gancho": nota, "formula": formula(g), "formato": l.get("formato", ""), "link": l.get("link", "")})
    itens.sort(key=lambda x: -x["multiplo"])
    if "--json" in a:
        print(json.dumps(itens, ensure_ascii=False, indent=2))
        return
    out = ["# Arquivo de referências do nicho", "",
           f"{len(itens)} vídeos, ordenados pelo múltiplo sobre a mediana do próprio perfil."
           + (f" {sem_mediana} sem mediana (estimada por 10% dos seguidores: confira)." if sem_mediana else ""), "",
           "| # | Múltiplo | Perfil | Gancho | Nota | Fórmula | Formato | Link |", "|---|---|---|---|---|---|---|---|"]
    for i, x in enumerate(itens, 1):
        out.append(f"| {i} | {x['multiplo']}x | {x['perfil']} | {x['gancho'][:70]} | {x['nota_gancho'] or ''} | {x['formula']} | {x['formato']} | {x['link']} |")
    cont = {}
    for x in itens[:10]:
        cont[x["formula"]] = cont.get(x["formula"], 0) + 1
    out += ["", "## Fórmulas mais frequentes entre os 10 melhores", ""] + [f"- {k}: {v}" for k, v in sorted(cont.items(), key=lambda y: -y[1])]
    out += ["", "Use a estrutura e o gancho como inspiração; o conteúdo vem sempre da experiência da empresa."]
    texto = "\n".join(out) + "\n"
    if "--saida" in a:
        dest = a[a.index("--saida") + 1]
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"Arquivo gravado em {dest}")
    else:
        print(texto)


if __name__ == "__main__":
    main()
