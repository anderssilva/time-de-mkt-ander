#!/usr/bin/env python3
"""Registro de marketing por empresa (planilhas em CSV dentro de empresas/<slug>/registro/).

As quatro planilhas são a fonte oficial do que foi pensado, produzido, publicado e aprendido.
Ficam na pasta da empresa, sincronizadas pelo Google Drive; para ver, abra no Google Planilhas.

Uso (sempre a partir da pasta Marketing):
  python3 registro.py iniciar   empresas/<slug>
  python3 registro.py proximo   empresas/<slug> publicacoes|ideias|melhorias
  python3 registro.py adicionar empresas/<slug> <tabela> '{"campo": "valor", ...}'
  python3 registro.py atualizar empresas/<slug> <tabela> <id> '{"campo": "valor", ...}'
  python3 registro.py listar    empresas/<slug> <tabela> [campo=valor ...]
  python3 registro.py repeticao empresas/<slug> "<gancho>" "<ângulo>" [--limite 0.45]
  python3 registro.py melhoria-parecida empresas/<slug> "<problema>"

Regras:
- "adicionar" gera o id sozinho se ele não vier (P001, I001, M001). Campos desconhecidos são recusados.
- "repeticao" compara gancho e ângulo com TODAS as publicações e ideias (inclusive descartadas)
  e lista as mais parecidas com uma nota de 0 a 1. Acima de 0,45 merece atenção; acima de 0,65 é repetição.
- Nunca apaga linhas. Para descartar, mude o status.
"""
import csv, json, os, re, sys, unicodedata
from difflib import SequenceMatcher
from datetime import date

TABELAS = {
    "publicacoes": ("P", ["id", "data_publicacao", "semana", "canal", "formato", "pilar", "tema", "gancho", "angulo",
                          "resumo", "cta", "pasta", "link", "status", "nota_estrategista", "nota_qualidade",
                          "aprovado_por", "data_aprovacao", "alcance", "curtidas", "comentarios", "salvamentos",
                          "compartilhamentos", "cliques", "seguidores_ganhos", "observacoes", "origem"]),
    "ideias": ("I", ["id", "data", "ideia", "gancho", "angulo", "pilar", "formato", "origem", "decisao", "motivo",
                     "virou_peca"]),
    "plano": (None, ["trimestre", "mes", "tema", "pilar_foco", "peca_mae", "meta_entrada", "meta_saida", "resultado"]),
    "melhorias": ("M", ["id", "data", "peca", "origem", "problema", "causa", "regra_proposta", "onde_aplicar",
                        "ocorrencias", "status", "data_incorporacao"]),
}
STATUS = {
    "publicacoes": {"ideia", "aprovado", "em produção", "em revisão", "pronto", "agendado", "publicado", "descartado"},
    "melhorias": {"proposta", "aprovada", "incorporada", "recusada"},
}


def caminho(emp, tab):
    return os.path.join(emp, "registro", f"{tab}.csv")


def ler(emp, tab):
    p = caminho(emp, tab)
    if not os.path.exists(p):
        sys.exit(f"Arquivo não encontrado: {p}. Rode: registro.py iniciar {emp}")
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def gravar(emp, tab, linhas):
    cols = TABELAS[tab][1]
    p = caminho(emp, tab)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="raise")
        w.writeheader()
        for l in linhas:
            w.writerow({c: l.get(c, "") for c in cols})
    os.replace(tmp, p)


def iniciar(emp):
    os.makedirs(os.path.join(emp, "registro"), exist_ok=True)
    for tab, (_, cols) in TABELAS.items():
        p = caminho(emp, tab)
        if os.path.exists(p):
            with open(p, encoding="utf-8", newline="") as f:
                atuais = next(csv.reader(f), [])
            faltam = [c for c in cols if c not in atuais]
            if faltam:  # migra colunas novas sem perder dados
                linhas = ler(emp, tab)
                gravar(emp, tab, linhas)
                print(f"{tab}: colunas adicionadas {faltam}")
            else:
                print(f"{tab}: ok")
        else:
            gravar(emp, tab, [])
            print(f"{tab}: criado")


def proximo(emp, tab):
    pref = TABELAS[tab][0]
    if not pref:
        sys.exit("Esta tabela não usa id.")
    nums = [int(m.group(1)) for l in ler(emp, tab) if (m := re.fullmatch(pref + r"(\d+)", l.get("id", "")))]
    return f"{pref}{(max(nums) + 1 if nums else 1):03d}"


def validar(tab, dados):
    cols = TABELAS[tab][1]
    ruins = [k for k in dados if k not in cols]
    if ruins:
        sys.exit(f"Campos desconhecidos em {tab}: {ruins}. Válidos: {cols}")
    st = dados.get("status")
    if st and tab in STATUS and st not in STATUS[tab]:
        sys.exit(f"Status inválido '{st}'. Válidos: {sorted(STATUS[tab])}")


def adicionar(emp, tab, dados):
    validar(tab, dados)
    linhas = ler(emp, tab)
    if TABELAS[tab][0]:
        dados.setdefault("id", proximo(emp, tab))
        if any(l["id"] == dados["id"] for l in linhas):
            sys.exit(f"Id {dados['id']} já existe em {tab}.")
    if tab == "ideias":
        dados.setdefault("data", date.today().isoformat())
    if tab == "melhorias":
        dados.setdefault("data", date.today().isoformat())
        dados.setdefault("status", "proposta")
        dados.setdefault("ocorrencias", "1")
    linhas.append(dados)
    gravar(emp, tab, linhas)
    print(dados.get("id", "linha adicionada"))


def atualizar(emp, tab, ident, dados):
    validar(tab, dados)
    linhas = ler(emp, tab)
    for l in linhas:
        if l.get("id") == ident:
            l.update(dados)
            gravar(emp, tab, linhas)
            print(f"{ident} atualizado")
            return
    sys.exit(f"Id {ident} não encontrado em {tab}.")


def norm(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", t).split()


PARADAS = set("a o e de da do das dos em no na nos nas um uma para por com que se seu sua como mais nao ou ao".split())


def parecido(a, b):
    ta = [w for w in norm(a) if w not in PARADAS]
    tb = [w for w in norm(b) if w not in PARADAS]
    if not ta or not tb:
        return 0.0
    jac = len(set(ta) & set(tb)) / len(set(ta) | set(tb))
    seq = SequenceMatcher(None, " ".join(ta), " ".join(tb)).ratio()
    return round(0.5 * jac + 0.5 * seq, 2)


def repeticao(emp, gancho, angulo, limite):
    achados = []
    for tab in ("publicacoes", "ideias"):
        for l in ler(emp, tab):
            nota = round(0.6 * parecido(gancho, l.get("gancho", "")) + 0.4 * parecido(angulo, l.get("angulo", "")), 2)
            if nota >= limite:
                achados.append((nota, tab, l.get("id", ""), l.get("status") or l.get("decisao", ""), l.get("gancho", ""), l.get("angulo", "")))
    achados.sort(reverse=True)
    if not achados:
        print(f"Nenhuma pauta parecida (limite {limite}).")
    for n, tab, i, st, g, a in achados[:10]:
        alerta = "REPETIÇÃO" if n >= 0.65 else "atenção"
        print(f"{n:.2f} [{alerta}] {tab} {i} ({st}) | gancho: {g} | ângulo: {a}")


def melhoria_parecida(emp, problema):
    achados = sorted(((parecido(problema, l.get("problema", "")), l) for l in ler(emp, "melhorias")), key=lambda x: -x[0])
    achados = [(n, l) for n, l in achados if n >= 0.4]
    if not achados:
        print("Nenhuma melhoria parecida já registrada.")
    for n, l in achados[:5]:
        print(f"{n:.2f} {l['id']} ({l['status']}, {l['ocorrencias']}x) {l['problema']} -> {l['regra_proposta']}")


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    cmd, emp = a[0], a[1].rstrip("/")
    if cmd == "iniciar":
        iniciar(emp)
    elif cmd == "proximo":
        print(proximo(emp, a[2]))
    elif cmd == "adicionar":
        adicionar(emp, a[2], json.loads(a[3]))
    elif cmd == "atualizar":
        atualizar(emp, a[2], a[3], json.loads(a[4]))
    elif cmd == "listar":
        filtros = dict(x.split("=", 1) for x in a[3:])
        for l in ler(emp, a[2]):
            if all(l.get(k, "") == v for k, v in filtros.items()):
                print(json.dumps(l, ensure_ascii=False))
    elif cmd == "repeticao":
        lim = float(a[a.index("--limite") + 1]) if "--limite" in a else 0.45
        repeticao(emp, a[2], a[3], lim)
    elif cmd == "melhoria-parecida":
        melhoria_parecida(emp, a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
