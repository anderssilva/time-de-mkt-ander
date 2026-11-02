#!/usr/bin/env python3
"""Ranking de desempenho das publicações da empresa, comparando cada post com a própria conta.

Uso (de dentro da pasta da empresa):
  python3 desempenho.py . [--dias 90] [--canal instagram] [--json]

Lê registro/publicacoes.csv (status "publicado", com alcance preenchido) e calcula, por post:
  - MÚLTIPLO: alcance do post ÷ alcance mediano da conta no período (2,0 = o dobro do normal).
    Visualização bruta engana; o múltiplo mostra o que realmente funcionou para esta conta.
  - ENVIOS POR ALCANCE: compartilhamentos ÷ alcance (por mil). É o sinal mais forte de conteúdo que circula.
  - SALVAMENTOS POR ALCANCE: salvamentos ÷ alcance (por mil). Mostra conteúdo útil, de guardar.
E aponta: os 3 melhores (o que repetir), os 3 piores (o que parar) e o padrão de gancho, formato e pilar
dos que passaram de 1,5x.

Métricas inspiradas no ig-audit do projeto instagram-agent-skill (Jake Schincariol, licença MIT).
"""
import csv, json, os, statistics, sys
from datetime import date, datetime, timedelta


def num(v):
    try:
        return float(str(v).replace(".", "").replace(",", ".")) if v not in ("", None) else None
    except ValueError:
        return None


def data(v):
    for f in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(str(v).strip()[:16], f).date()
        except ValueError:
            pass
    return None


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    pasta = a[0]
    dias = int(a[a.index("--dias") + 1]) if "--dias" in a else 90
    canal = a[a.index("--canal") + 1].lower() if "--canal" in a else None
    arq = os.path.join(pasta, "registro", "publicacoes.csv")
    if not os.path.exists(arq):
        sys.exit(f"Não encontrei {arq}.")
    with open(arq, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    corte = date.today() - timedelta(days=dias)
    posts = []
    for l in linhas:
        if l.get("status") != "publicado":
            continue
        if canal and l.get("canal", "").lower() != canal:
            continue
        d = data(l.get("data_publicacao"))
        if d and d < corte:
            continue
        alc = num(l.get("alcance"))
        if not alc:
            continue
        posts.append({"id": l.get("id"), "data": str(d or ""), "canal": l.get("canal"), "formato": l.get("formato"),
                      "pilar": l.get("pilar"), "gancho": l.get("gancho"), "alcance": alc,
                      "envios": num(l.get("compartilhamentos")) or 0, "salvos": num(l.get("salvamentos")) or 0})
    if len(posts) < 3:
        print(f"Só {len(posts)} publicação(ões) com alcance nos últimos {dias} dias: preencha as métricas no registro primeiro.")
        return
    med = statistics.median(p["alcance"] for p in posts)
    for p in posts:
        p["multiplo"] = round(p["alcance"] / med, 2) if med else 0
        p["envios_mil"] = round(1000 * p["envios"] / p["alcance"], 1)
        p["salvos_mil"] = round(1000 * p["salvos"] / p["alcance"], 1)
    posts.sort(key=lambda p: (-p["multiplo"], -p["envios_mil"]))
    acima = [p for p in posts if p["multiplo"] >= 1.5]
    padrao = {}
    for k in ("formato", "pilar"):
        cont = {}
        for p in acima:
            cont[p[k] or "(vazio)"] = cont.get(p[k] or "(vazio)", 0) + 1
        padrao[k] = sorted(cont.items(), key=lambda x: -x[1])
    res = {"periodo_dias": dias, "publicacoes": len(posts), "alcance_mediano": med, "ranking": posts, "padrao_acima_1_5x": padrao}
    if "--json" in a:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    print(f"DESEMPENHO · {len(posts)} publicações · últimos {dias} dias · alcance mediano {int(med)}")
    print("=" * 84)
    print(f"  {'peça':<6}{'múltiplo':>9}{'envios/mil':>12}{'salvos/mil':>12}  formato      gancho")
    for p in posts:
        print(f"  {p['id']:<6}{p['multiplo']:>8.2f}x{p['envios_mil']:>12}{p['salvos_mil']:>12}  {str(p['formato'])[:11]:<12} {str(p['gancho'])[:34]}")
    print("-" * 84)
    print("  Repetir (melhores): " + ", ".join(p["id"] for p in posts[:3]))
    print("  Repensar (piores):  " + ", ".join(p["id"] for p in posts[-3:]))
    if acima:
        print("  Acima de 1,5x · formatos: " + ", ".join(f"{k} ({v})" for k, v in padrao["formato"]) +
              " · pilares: " + ", ".join(f"{k} ({v})" for k, v in padrao["pilar"]))


if __name__ == "__main__":
    main()
