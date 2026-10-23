#!/usr/bin/env python3
"""Registro de marketing por empresa (quatro tabelas: publicacoes, ideias, plano, melhorias).

Duas formas de guardar, escolhidas na implantação (arquivo registro/fonte.json):
- "csv" (padrão): os CSV em <pasta da empresa>/registro/ são a fonte oficial.
- "planilhas": uma Planilha Google (link) é a fonte oficial; os CSV viram espelho local para
  cálculo e cópia de segurança. Leia referencias/registro-planilhas.md do plugin.

Uso (de dentro da pasta da empresa, onde o caminho é "."; ou passando o caminho da pasta):
  python3 registro.py iniciar   <pasta>
  python3 registro.py proximo   <pasta> publicacoes|ideias|melhorias
  python3 registro.py adicionar <pasta> <tabela> '{"campo": "valor", ...}'
  python3 registro.py atualizar <pasta> <tabela> <id> '{"campo": "valor", ...}'
  python3 registro.py listar    <pasta> <tabela> [campo=valor ...]
  python3 registro.py repeticao <pasta> "<gancho>" "<ângulo>" [--limite 0.45]
  python3 registro.py melhoria-parecida <pasta> "<problema>"
  python3 registro.py fonte     <pasta> [csv | planilhas <link>]
  python3 registro.py cabecalhos
  python3 registro.py espelhar  <pasta> <tabela> <arquivo.json>   (só no modo planilhas)
  python3 registro.py pendentes <pasta>                           (só no modo planilhas)
  python3 registro.py sincronizado <pasta>                        (só no modo planilhas)

Regras:
- "adicionar" gera o id sozinho se ele não vier (P001, I001, M001). Campos desconhecidos são recusados.
- "repeticao" compara gancho e ângulo com TODAS as publicações e ideias (inclusive descartadas)
  e lista as mais parecidas com uma nota de 0 a 1. Acima de 0,45 merece atenção; acima de 0,65 é repetição.
- Nunca apaga linhas. Para descartar, mude o status.
"""
import csv, json, os, re, sys, unicodedata
from difflib import SequenceMatcher
from datetime import date, datetime

REF_PLANILHAS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "referencias", "registro-planilhas.md")
ESPELHO_VALIDO_MIN = 30
_AVISADO = False

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


def arq_fonte(emp):
    return os.path.join(emp, "registro", "fonte.json")


def fonte(emp):
    p = arq_fonte(emp)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {"tipo": "csv"}


def salvar_fonte(emp, dados):
    os.makedirs(os.path.join(emp, "registro"), exist_ok=True)
    with open(arq_fonte(emp), "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def id_planilha(link):
    m = re.search(r"/spreadsheets/d/([A-Za-z0-9_-]+)", link)
    return m.group(1) if m else link.strip()


def modo_planilhas(emp):
    return fonte(emp).get("tipo") == "planilhas"


def avisar_espelho(emp):
    """No modo planilhas, avisa se o espelho local está velho (a planilha pode ter mudado)."""
    global _AVISADO
    if _AVISADO or not modo_planilhas(emp):
        return
    _AVISADO = True
    ult = fonte(emp).get("ultimo_espelho")
    idade = None
    if ult:
        try:
            idade = (datetime.now() - datetime.fromisoformat(ult)).total_seconds() / 60
        except ValueError:
            idade = None
    if idade is None or idade > ESPELHO_VALIDO_MIN:
        quando = "nunca" if idade is None else f"há {int(idade)} min"
        print(f"ATENÇÃO: esta empresa usa Planilha Google e o espelho local foi atualizado {quando}. "
              f"Baixe as quatro abas antes de confiar nestes dados (passo 'Baixar' em {REF_PLANILHAS}).", file=sys.stderr)


def registrar_pendente(emp, tab, acao, linha):
    if not modo_planilhas(emp):
        return
    cols = TABELAS[tab][1]
    reg = {"tabela": tab, "acao": acao, "id": linha.get("id", ""), "valores": [linha.get(c, "") for c in cols]}
    with open(os.path.join(emp, "registro", ".pendentes.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    print(f"PLANILHA: alteração pendente em '{tab}'. Envie para a Planilha Google (passo 'Enviar' em {REF_PLANILHAS}).")


def pendentes(emp):
    p = os.path.join(emp, "registro", ".pendentes.jsonl")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def sincronizado(emp):
    p = os.path.join(emp, "registro", ".pendentes.jsonl")
    if os.path.exists(p):
        hist = os.path.join(emp, "registro", ".sincronizados.log")
        with open(p, encoding="utf-8") as f, open(hist, "a", encoding="utf-8") as h:
            for l in f:
                if l.strip():
                    h.write(datetime.now().isoformat(timespec="seconds") + " " + l)
        os.remove(p)
    print("Pendências marcadas como enviadas.")


def espelhar(emp, tab, arquivo):
    """Grava no CSV local o conteúdo de uma aba da planilha (lista de linhas; a primeira é o cabeçalho)."""
    if not modo_planilhas(emp):
        sys.exit("Esta empresa não está no modo planilhas. Use: registro.py fonte <pasta> planilhas <link>")
    if pendentes(emp):
        sys.exit("Há alterações locais ainda não enviadas para a planilha. Rode o passo 'Enviar' antes de baixar.")
    with open(arquivo, encoding="utf-8") as f:
        valores = json.load(f)
    if isinstance(valores, dict):
        valores = valores.get("values", [])
    if not valores:
        sys.exit(f"Aba {tab} vazia: a planilha precisa ter ao menos a linha de cabeçalho (registro.py cabecalhos).")
    cab = [str(c).strip() for c in valores[0]]
    cols = TABELAS[tab][1]
    faltam = [c for c in cols if c not in cab]
    sobram = [c for c in cab if c and c not in cols]
    linhas = []
    for v in valores[1:]:
        if not any(str(x).strip() for x in v):
            continue
        linhas.append({c: (str(v[i]) if i < len(v) else "") for i, c in enumerate(cab) if c in cols})
    gravar(emp, tab, linhas)
    f = fonte(emp)
    f["ultimo_espelho"] = datetime.now().isoformat(timespec="seconds")
    salvar_fonte(emp, f)
    print(f"{tab}: {len(linhas)} linhas espelhadas.")
    if faltam:
        print(f"Colunas que faltam na planilha (acrescente no fim da aba '{tab}'): {faltam}")
    if sobram:
        print(f"Colunas da planilha ignoradas (não fazem parte do registro): {sobram}")


def caminho(emp, tab):
    return os.path.join(emp, "registro", f"{tab}.csv")


def ler(emp, tab, avisar=True):
    if avisar:
        avisar_espelho(emp)
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
                linhas = ler(emp, tab, avisar=False)
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
    registrar_pendente(emp, tab, "adicionar", dados)


def atualizar(emp, tab, ident, dados):
    validar(tab, dados)
    linhas = ler(emp, tab)
    for l in linhas:
        if l.get("id") == ident:
            l.update(dados)
            gravar(emp, tab, linhas)
            print(f"{ident} atualizado")
            registrar_pendente(emp, tab, "atualizar", l)
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
    if a[:1] == ["cabecalhos"]:
        print(json.dumps({t: c for t, (_, c) in TABELAS.items()}, ensure_ascii=False, indent=2))
        return
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
    elif cmd == "fonte":
        if len(a) == 2:
            print(json.dumps(fonte(emp), ensure_ascii=False, indent=2))
        elif a[2] == "csv":
            salvar_fonte(emp, {"tipo": "csv"})
            print("Fonte oficial: CSV na pasta registro/.")
        elif a[2] == "planilhas" and len(a) >= 4:
            salvar_fonte(emp, {"tipo": "planilhas", "link": a[3], "id_planilha": id_planilha(a[3])})
            print(f"Fonte oficial: Planilha Google {id_planilha(a[3])}. Os CSV passam a ser espelho local. Veja {REF_PLANILHAS}.")
        else:
            sys.exit("Uso: registro.py fonte <pasta> [csv | planilhas <link>]")
    elif cmd == "espelhar":
        espelhar(emp, a[2], a[3])
    elif cmd == "pendentes":
        print(json.dumps(pendentes(emp), ensure_ascii=False, indent=2))
    elif cmd == "sincronizado":
        sincronizado(emp)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
