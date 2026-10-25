#!/usr/bin/env python3
"""Gera as lâminas de um carrossel (PNG 1080x1350), um PDF para o LinkedIn e uma folha de revisão leve
(folha-revisao.jpg, todas as lâminas lado a lado) a partir de um laminas.json.

Uso:
  python3 renderizar.py <laminas.json> [--saida <pasta>] [--sem-pdf] [--so-validar] [--laminas 1,3]

  --so-validar  só confere o JSON (contraste, palavras, arquivos), sem gerar imagens.
  --laminas     gera só as lâminas indicadas (ex.: 1,3). Use para a prova visual e para refazer só o que mudou.
                O PDF só é gerado quando todas as lâminas são geradas.

Requisitos (uma vez): pip install playwright pillow  &&  python3 -m playwright install chromium

O laminas.json tem duas partes: "marca" (ou "marca_arquivo", apontando para 00-contexto/carrossel-marca.json da empresa)
e "laminas" (o conteúdo aprovado). Caminhos dentro do arquivo de marca são relativos a ele.
Caminhos de arquivos (logo, fotos, fontes) podem ser absolutos ou relativos ao laminas.json.

{
  "marca": {
    "cores": {"fundo": "#FFFFFF", "fundo_alt": "#F7F7FA", "escuro": "#14213D", "escuro_2": "#1F3460",
              "texto": "#14213D", "texto_suave": "#4A5675", "destaque": "#2A6FDB", "destaque_2": "#5B93EA",
              "linha": "#E4E4EC"},
    "fonte": "Montserrat",
    "fonte_url": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap",
    "fonte_arquivos": {"400": "fontes/m-400.woff2", "700": "fontes/m-700.woff2"},   (opcional, sem internet)
    "logo": "logo-colorido.png", "logo_claro": "logo-branco.png",
    "marca_dagua": "simbolo.png",            (opcional, 4 a 7% de opacidade)
    "assinatura": "suaempresa.com.br",               (opcional, aparece na última lâmina)
    "numeros_cor": "texto"                   ("texto" ou "destaque": cor dos números grandes)
  },
  "laminas": [
    {"tipo": "capa", "tema": "escuro", "rotulo": "GOVERNANÇA", "titulo": "Texto com *destaque*", "subtitulo": "...", "foto": "fotos/x.jpg", "foto_posicao": "center 20%"},
    {"tipo": "conteudo", "tema": "claro", "numero": "01", "titulo": "...", "texto": "..."},
    {"tipo": "acao", "tema": "claro", "numero": "01", "rotulo": "Ação", "titulo": "...", "passos": ["...", "..."], "exemplo": "..."},
    {"tipo": "lista", "tema": "claro", "rotulo": "...", "titulo": "...", "itens": ["...", "..."]},
    {"tipo": "numero", "tema": "claro", "valor": "3x", "titulo": "...", "texto": "...", "fonte": "provas.md #2"},
    {"tipo": "citacao", "tema": "escuro", "texto": "...", "autor": "..."},
    {"tipo": "comparacao", "tema": "claro", "titulo": "...", "antes_titulo": "Antes", "antes": ["..."], "depois_titulo": "Depois", "depois": ["..."]},
    {"tipo": "cta", "tema": "claro", "titulo": "...", "texto": "...", "acao": "Salve e compartilhe"}
  ]
}

Destaque: escreva *palavra* para destacar. Em fundo escuro, a palavra ganha a cor de destaque.
Em fundo claro, se a cor de destaque não tiver contraste suficiente, vira marca-texto (texto escuro com faixa colorida).
"""
import html, json, os, re, sys, tempfile

LARG, ALT = 1080, 1350


# ---------- cor e contraste ----------
def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(hexcor):
    h = hexcor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contraste(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


def rgba(hexcor, alfa):
    h = hexcor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alfa})"


# ---------- texto ----------
def fmt(t, escuro, marca_texto):
    t = html.escape(t or "").replace("\n", "<br>")
    cls = "hl-cor" if (escuro or not marca_texto) else "hl-marca"
    return re.sub(r"\*(.+?)\*", rf'<span class="{cls}">\1</span>', t)


def palavras(t):
    return len(re.sub(r"[*]", "", t or "").split())


# ---------- validação ----------
def validar(dados, base):
    erros, avisos = [], []
    m = dados.get("marca", {})
    c = m.get("cores", {})
    for k in ("fundo", "escuro", "texto", "texto_suave", "destaque"):
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", c.get(k, "")):
            erros.append(f"marca.cores.{k} ausente ou inválida (use #RRGGBB)")
    if erros:
        return erros, avisos
    c.setdefault("destaque_2", c["destaque"])
    c.setdefault("fundo_alt", c["fundo"])
    c.setdefault("escuro_2", c["escuro"])
    c.setdefault("linha", c["texto_suave"])
    pares = [("texto sobre fundo claro", c["texto"], c["fundo"], 4.5),
             ("texto suave sobre fundo claro", c["texto_suave"], c["fundo"], 4.5),
             ("branco sobre fundo escuro", "#FFFFFF", c["escuro"], 4.5),
             ("destaque sobre fundo escuro", c["destaque_2"], c["escuro"], 3.0)]
    for nome, a, b, minimo in pares:
        r = contraste(a, b)
        if r < minimo:
            avisos.append(f"Contraste baixo: {nome} = {r}:1 (mínimo {minimo}:1)")
    r = contraste(c["destaque"], c["fundo"])
    m["_marca_texto"] = r < 3.0
    if r < 3.0:
        avisos.append(f"Destaque sobre fundo claro = {r}:1 (abaixo de 3:1). Em fundo claro, o destaque vira marca-texto "
                      f"e os rótulos usam a cor do texto com um traço de destaque.")
    for chave in ("logo", "logo_claro", "marca_dagua"):
        if m.get(chave) and not os.path.exists(caminho(base, m[chave])):
            erros.append(f"Arquivo não encontrado: marca.{chave} = {m[chave]}")
    lam = dados.get("laminas", [])
    if not 2 <= len(lam) <= 20:
        erros.append(f"O carrossel precisa ter de 2 a 20 lâminas (tem {len(lam)}).")
    tipos = {"capa", "conteudo", "acao", "lista", "numero", "citacao", "comparacao", "cta"}
    for i, l in enumerate(lam, 1):
        if l.get("tipo") not in tipos:
            erros.append(f"Lâmina {i}: tipo '{l.get('tipo')}' inválido. Use: {sorted(tipos)}")
            continue
        if l.get("foto") and not os.path.exists(caminho(base, l["foto"])):
            erros.append(f"Lâmina {i}: foto não encontrada: {l['foto']}")
        total = sum(palavras(l.get(k, "")) for k in ("titulo", "texto", "subtitulo", "exemplo")) + \
            sum(palavras(x) for k in ("itens", "antes", "depois", "passos") for x in l.get(k, []))
        limite = 70 if l["tipo"] == "acao" else 45
        if l["tipo"] == "acao" and not 2 <= len(l.get("passos", [])) <= 4:
            avisos.append(f"Lâmina {i}: ação com {len(l.get('passos', []))} passos (use de 2 a 4).")
        if total > limite:
            avisos.append(f"Lâmina {i}: {total} palavras (recomendado até {limite - 10}). Considere dividir.")
        if l["tipo"] == "capa" and palavras(l.get("titulo", "")) > 10:
            avisos.append(f"Lâmina {i}: título da capa com {palavras(l['titulo'])} palavras (recomendado até 8).")
        if l["tipo"] == "lista" and len(l.get("itens", [])) > 5:
            avisos.append(f"Lâmina {i}: {len(l['itens'])} itens (recomendado até 5).")
    if lam and lam[0].get("tipo") != "capa":
        avisos.append("A primeira lâmina não é uma capa.")
    if lam and lam[-1].get("tipo") != "cta":
        avisos.append("A última lâmina não é de chamada para ação (cta).")
    return erros, avisos


def caminho(base, p):
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))


def url(base, p):
    return "file://" + caminho(base, p)


# ---------- HTML ----------
def css(m, base):
    c = m["cores"]
    fonte = m.get("fonte", "Montserrat")
    faces = ""
    for peso, arq in (m.get("fonte_arquivos") or {}).items():
        faces += f"@font-face{{font-family:'{fonte}';font-weight:{peso};src:url('{url(base, arq)}') format('woff2');}}\n"
    imp = "" if faces or not m.get("fonte_url") else f"@import url('{m['fonte_url']}');\n"
    num = c["texto"] if m.get("numeros_cor", "texto") == "texto" else c["destaque"]
    return imp + faces + f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{LARG}px;height:{ALT}px}}
body{{font-family:'{fonte}',sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}}
.l{{position:relative;width:{LARG}px;height:{ALT}px;overflow:hidden;padding:120px 96px 150px;display:flex;flex-direction:column}}
.claro{{background:{c['fundo']};color:{c['texto']}}}
.alt{{background:{c['fundo_alt']};color:{c['texto']}}}
.escuro{{background:linear-gradient(150deg,{c['escuro']} 0%,{c['escuro']} 55%,{c['escuro_2']} 100%);color:#fff}}
.dagua{{position:absolute;right:-300px;bottom:-260px;width:880px;opacity:.045;pointer-events:none}}
.escuro .dagua{{opacity:.07}}
.regua{{width:72px;height:6px;border-radius:3px;background:linear-gradient(90deg,{c['destaque']},{c['destaque_2']});margin-bottom:36px}}
.rotulo{{font-weight:700;font-size:24px;letter-spacing:5px;text-transform:uppercase;margin-bottom:28px;color:{c['destaque'] if not m['_marca_texto'] else c['texto']}}}
.escuro .rotulo{{color:{c['destaque_2']}}}
h1{{font-weight:700;font-size:100px;line-height:1.03;letter-spacing:-2.5px}}
h2{{font-weight:700;font-size:72px;line-height:1.08;letter-spacing:-1.5px}}
.sub{{font-weight:500;font-size:40px;line-height:1.4;margin-top:44px;color:{c['texto_suave']}}}
.escuro .sub{{color:rgba(255,255,255,.78)}}
.txt{{font-weight:400;font-size:40px;line-height:1.5;margin-top:44px;color:{c['texto_suave']}}}
.escuro .txt{{color:rgba(255,255,255,.82)}}
.hl-cor{{color:{c['destaque_2']}}}
.claro .hl-cor,.alt .hl-cor{{color:{c['destaque']}}}
.hl-marca{{background:linear-gradient(transparent 60%,{rgba(c['destaque'], .38)} 60%,{rgba(c['destaque'], .38)} 92%,transparent 92%);padding:0 4px}}
.num{{font-weight:800;font-size:160px;line-height:.9;color:{num};margin-bottom:36px;letter-spacing:-4px}}
.escuro .num{{color:#fff}}
.num-mini{{font-weight:800;font-size:30px;letter-spacing:4px;color:{c['destaque'] if not m['_marca_texto'] else c['texto']};margin-bottom:24px}}
.escuro .num-mini{{color:{c['destaque_2']}}}
.valor{{font-weight:800;font-size:230px;line-height:.9;letter-spacing:-6px;color:{num}}}
.escuro .valor{{color:#fff}}
.fonte-dado{{font-size:22px;margin-top:28px;color:{c['texto_suave']}}}
.escuro .fonte-dado{{color:rgba(255,255,255,.6)}}
.itens{{list-style:none;margin-top:48px;display:flex;flex-direction:column;gap:34px}}
.itens li{{display:flex;gap:28px;align-items:flex-start;font-size:40px;line-height:1.4;font-weight:500}}
.itens .b{{flex:0 0 46px;height:46px;border-radius:50%;background:linear-gradient(135deg,{c['destaque']},{c['destaque_2']});color:#fff;font-weight:800;font-size:22px;display:flex;align-items:center;justify-content:center;margin-top:2px}}
.cit{{display:flex;gap:40px}}
.cit .bar{{flex:0 0 8px;border-radius:4px;background:linear-gradient(180deg,{c['destaque']},{c['destaque_2']})}}
.cit p{{font-weight:600;font-size:56px;line-height:1.25;letter-spacing:-.5px}}
.cit .aut{{font-weight:600;font-size:26px;letter-spacing:3px;text-transform:uppercase;margin-top:40px;opacity:.75}}
.comp{{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:56px}}
.col{{border-radius:8px;padding:40px 36px}}
.col h3{{font-weight:700;font-size:26px;letter-spacing:4px;text-transform:uppercase;margin-bottom:28px}}
.col li{{font-size:34px;line-height:1.4;margin-bottom:20px;list-style:none}}
.antes{{background:{c['fundo_alt']};border:2px solid {c['linha']};color:{c['texto_suave']}}}
.depois{{background:{c['escuro']};color:#fff}}
.depois h3{{color:{c['destaque_2']}}}
.escuro .antes{{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.15);color:rgba(255,255,255,.75)}}
.escuro .depois{{background:#fff;color:{c['texto']}}}
.escuro .depois h3{{color:{c['texto']}}}
.cta-acao{{display:inline-flex;align-items:center;gap:18px;margin-top:56px;padding:26px 40px;border-radius:999px;background:linear-gradient(90deg,{c['destaque']},{c['destaque_2']});color:#fff;font-weight:700;font-size:32px;align-self:flex-start}}
.cta-acao.marca{{background:{c['escuro']}}}
.assin{{margin-top:48px;font-weight:600;font-size:28px;letter-spacing:1px;color:{c['texto_suave']}}}
.escuro .assin{{color:rgba(255,255,255,.7)}}
.z.meio{{flex:0 0 auto;margin-top:auto;margin-bottom:auto;padding-bottom:40px}}
.rodape{{position:absolute;left:96px;right:96px;bottom:56px;display:flex;align-items:center;justify-content:space-between}}
.pag{{font-weight:600;font-size:22px;letter-spacing:3px;color:{c['texto_suave']}}}
.escuro .pag{{color:rgba(255,255,255,.6)}}
.rodape img{{height:92px;margin-right:-14px}}
.arraste{{font-weight:700;font-size:24px;letter-spacing:3px;text-transform:uppercase;display:flex;align-items:center;gap:14px}}
.arraste span{{font-size:34px;line-height:1}}
.foto{{position:absolute;inset:0;background-size:cover;background-position:center}}
.foto-base{{position:absolute;left:0;right:0;bottom:0;height:62%;background-size:cover;background-position:center 20%}}
.foto-base::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(0deg,{rgba(c['escuro'], .85)} 0%,{rgba(c['escuro'], 0)} 100%)}}
.claro .foto-base::after{{background:linear-gradient(0deg,{rgba(c['fundo'], .9)} 0%,{rgba(c['fundo'], 0)} 100%)}}
.foto-base::before{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,{c['escuro']} 0%,{rgba(c['escuro'], .0)} 45%)}}
.claro .foto-base::before{{background:linear-gradient(180deg,{c['fundo']} 0%,{rgba(c['fundo'], 0)} 45%)}}
.z{{position:relative;z-index:2;display:flex;flex-direction:column;flex:1}}
.acao-top{{display:flex;align-items:baseline;gap:22px;margin-bottom:26px}}
.acao-top .n{{font-weight:800;font-size:96px;line-height:.9;letter-spacing:-3px;color:{num}}}
.escuro .acao-top .n{{color:#fff}}
.acao-top .r{{font-weight:700;font-size:24px;letter-spacing:5px;text-transform:uppercase;color:{c['destaque'] if not m['_marca_texto'] else c['texto_suave']}}}
.escuro .acao-top .r{{color:{c['destaque_2']}}}
h2.m{{font-size:60px;line-height:1.1}}
.passos{{list-style:none;margin-top:36px;display:flex;flex-direction:column;gap:22px}}
.passos li{{display:flex;gap:22px;font-size:35px;line-height:1.38;font-weight:500}}
.passos li::before{{content:"";flex:0 0 14px;height:14px;border-radius:3px;margin-top:16px;background:linear-gradient(135deg,{c['destaque']},{c['destaque_2']})}}
.pratica{{margin-top:40px;padding:30px 34px;border-left:6px solid {c['destaque']};background:{c['fundo_alt']};border-radius:0 8px 8px 0}}
.escuro .pratica{{background:rgba(255,255,255,.07);border-left-color:{c['destaque_2']}}}
.pratica .k{{font-weight:700;font-size:21px;letter-spacing:4px;text-transform:uppercase;margin-bottom:12px;color:{c['texto_suave']}}}
.escuro .pratica .k{{color:rgba(255,255,255,.65)}}
.pratica p{{font-size:32px;line-height:1.42;color:{c['texto']}}}
.escuro .pratica p{{color:#fff}}
"""


def corpo(l, m, base, i, n):
    tema = l.get("tema", "claro")
    escuro = tema == "escuro"
    mt = m["_marca_texto"]
    f = lambda t: fmt(t, escuro, mt)
    t = l["tipo"]
    partes = []
    if t == "capa":
        if l.get("foto"):
            pos = l.get("foto_posicao", "center 20%")
            partes.append(f'<div class="foto-base" style="background-image:url(\'{url(base, l["foto"])}\');background-position:{html.escape(pos)}"></div>')
        z = '<div class="regua"></div>'
        if l.get("rotulo"):
            z += f'<div class="rotulo">{html.escape(l["rotulo"])}</div>'
        z += f'<h1>{f(l.get("titulo"))}</h1>'
        if l.get("subtitulo"):
            z += f'<div class="sub">{f(l["subtitulo"])}</div>'
        partes.append(f'<div class="z">{z}</div>')
    elif t == "conteudo":
        z = ""
        if l.get("numero"):
            z += f'<div class="num">{html.escape(l["numero"])}</div>'
        elif l.get("rotulo"):
            z += f'<div class="regua"></div><div class="rotulo">{html.escape(l["rotulo"])}</div>'
        else:
            z += '<div class="regua"></div>'
        z += f'<h2>{f(l.get("titulo"))}</h2>'
        if l.get("texto"):
            z += f'<div class="txt">{f(l["texto"])}</div>'
        partes.append(f'<div class="z meio">{z}</div>')
    elif t == "acao":
        z = '<div class="acao-top">'
        if l.get("numero"):
            z += f'<span class="n">{html.escape(l["numero"])}</span>'
        z += f'<span class="r">{html.escape(l.get("rotulo", "Ação"))}</span></div>'
        z += f'<h2 class="m">{f(l.get("titulo"))}</h2><ul class="passos">'
        z += "".join(f"<li><span>{f(x)}</span></li>" for x in l.get("passos", []))
        z += "</ul>"
        if l.get("exemplo"):
            z += f'<div class="pratica"><div class="k">{html.escape(l.get("exemplo_rotulo", "Na prática"))}</div><p>{f(l["exemplo"])}</p></div>'
        partes.append(f'<div class="z meio">{z}</div>')
    elif t == "lista":
        z = '<div class="regua"></div>'
        if l.get("rotulo"):
            z += f'<div class="rotulo">{html.escape(l["rotulo"])}</div>'
        z += f'<h2>{f(l.get("titulo"))}</h2><ul class="itens">'
        for k, it in enumerate(l.get("itens", []), 1):
            z += f'<li><span class="b">{k}</span><span>{f(it)}</span></li>'
        z += "</ul>"
        partes.append(f'<div class="z meio">{z}</div>')
    elif t == "numero":
        z = ""
        if l.get("rotulo"):
            z += f'<div class="regua"></div><div class="rotulo">{html.escape(l["rotulo"])}</div>'
        z += f'<div class="valor">{html.escape(l.get("valor", ""))}</div>'
        if l.get("titulo"):
            z += f'<h2 style="margin-top:40px">{f(l["titulo"])}</h2>'
        if l.get("texto"):
            z += f'<div class="txt">{f(l["texto"])}</div>'
        if l.get("fonte"):
            z += f'<div class="fonte-dado">Fonte: {html.escape(l["fonte"])}</div>'
        partes.append(f'<div class="z meio">{z}</div>')
    elif t == "citacao":
        z = f'<div class="cit"><div class="bar"></div><div><p>{f(l.get("texto"))}</p>'
        if l.get("autor"):
            z += f'<div class="aut">{html.escape(l["autor"])}</div>'
        z += "</div></div>"
        partes.append(f'<div class="z meio">{z}</div>')
    elif t == "comparacao":
        z = '<div class="regua"></div>'
        if l.get("rotulo"):
            z += f'<div class="rotulo">{html.escape(l["rotulo"])}</div>'
        z += f'<h2>{f(l.get("titulo"))}</h2><div class="comp">'
        z += f'<div class="col antes"><h3>{html.escape(l.get("antes_titulo", "Antes"))}</h3><ul>' + \
            "".join(f"<li>{f(x)}</li>" for x in l.get("antes", [])) + "</ul></div>"
        z += f'<div class="col depois"><h3>{html.escape(l.get("depois_titulo", "Depois"))}</h3><ul>' + \
            "".join(f"<li>{f(x)}</li>" for x in l.get("depois", [])) + "</ul></div></div>"
        partes.append(f'<div class="z meio">{z}</div>')
    elif t == "cta":
        z = '<div class="regua"></div>'
        if l.get("rotulo"):
            z += f'<div class="rotulo">{html.escape(l["rotulo"])}</div>'
        z += f'<h2>{f(l.get("titulo"))}</h2>'
        if l.get("texto"):
            z += f'<div class="txt">{f(l["texto"])}</div>'
        if l.get("acao"):
            z += f'<div class="cta-acao">{html.escape(l["acao"])} <span>→</span></div>'
        if m.get("assinatura"):
            z += f'<div class="assin">{html.escape(m["assinatura"])}</div>'
        partes.append(f'<div class="z meio" style="margin-bottom:0">{z}</div>')

    if m.get("marca_dagua") and not l.get("foto") and l.get("dagua", True):
        partes.insert(0, f'<img class="dagua" src="{url(base, m["marca_dagua"])}">')
    logo = m.get("logo_claro") if escuro else m.get("logo")
    esq = '<div class="arraste">Arraste <span>→</span></div>' if (i == 1 and n > 1) else f'<div class="pag">{i:02d} / {n:02d}</div>'
    rod = f'<div class="rodape">{esq}' + (f'<img src="{url(base, logo)}">' if logo else "<div></div>") + "</div>"
    classe = {"claro": "claro", "alt": "alt", "escuro": "escuro"}.get(tema, "claro")
    return f'<div class="l {classe}">{"".join(partes)}{rod}</div>'


def renderizar(arq, saida=None, pdf=True, so_validar=False, so=None):
    base = os.path.dirname(os.path.abspath(arq))
    with open(arq, encoding="utf-8") as fh:
        dados = json.load(fh)
    if "marca_arquivo" in dados and "marca" not in dados:
        marq = caminho(base, dados["marca_arquivo"])
        if not os.path.exists(marq):
            sys.exit(f"ERRO: marca_arquivo não encontrado: {marq}")
        with open(marq, encoding="utf-8") as fh:
            dados["marca"] = json.load(fh)
        base_marca = os.path.dirname(marq)
        for k in ("logo", "logo_claro", "marca_dagua"):  # caminhos da marca são relativos ao arquivo da marca
            if dados["marca"].get(k):
                dados["marca"][k] = caminho(base_marca, dados["marca"][k])
        for peso, f in list((dados["marca"].get("fonte_arquivos") or {}).items()):
            dados["marca"]["fonte_arquivos"][peso] = caminho(base_marca, f)
    erros, avisos = validar(dados, base)
    for a in avisos:
        print("AVISO:", a)
    if erros:
        for e in erros:
            print("ERRO:", e)
        sys.exit(1)
    if so_validar:
        print("Validação concluída.")
        return
    from playwright.sync_api import sync_playwright
    saida = saida or base
    os.makedirs(saida, exist_ok=True)
    m = dados["marca"]
    estilo = css(m, base)
    lams = dados["laminas"]
    n = len(lams)
    arquivos = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={"width": LARG, "height": ALT}, device_scale_factor=1)
        for i, l in enumerate(lams, 1):
            if so and i not in so:
                continue
            doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{estilo}</style></head><body>{corpo(l, m, base, i, n)}</body></html>'
            with tempfile.NamedTemporaryFile("w", suffix=".html", dir=base, delete=False, encoding="utf-8") as tf:
                tf.write(doc)
                tmp = tf.name
            try:
                pg.goto("file://" + tmp)
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(150)
                transb = pg.evaluate("""() => [...document.querySelectorAll('h1,h2,.txt,.sub,.itens,.comp,.cit')]
                    .some(e => e.getBoundingClientRect().bottom > 1350 - 140)""")
                if transb:
                    print(f"AVISO: lâmina {i}: o texto encosta no rodapé ou passa da área segura. Reduza o texto.")
                fam = pg.evaluate("() => document.fonts.check('700 40px " + m.get('fonte', 'Montserrat') + "')")
                if not fam:
                    print(f"AVISO: a fonte {m.get('fonte')} não carregou; usando fonte do sistema. Verifique internet ou fonte_arquivos.")
                dest = os.path.join(saida, f"{i:02d}.png")
                pg.screenshot(path=dest, clip={"x": 0, "y": 0, "width": LARG, "height": ALT})
                arquivos.append(dest)
            finally:
                os.remove(tmp)
        nav.close()
    print(f"{len(arquivos)} lâminas geradas em {saida}")
    folha(arquivos, os.path.join(saida, "folha-revisao.jpg"))
    if so:
        pdf = False
    if pdf:
        try:
            from PIL import Image
            imgs = [Image.open(a).convert("RGB") for a in arquivos]
            destpdf = os.path.join(saida, "carrossel-linkedin.pdf")
            imgs[0].save(destpdf, save_all=True, append_images=imgs[1:], resolution=144)
            print("PDF para LinkedIn:", destpdf)
        except ImportError:
            print("AVISO: Pillow não instalado; PDF não gerado (pip install pillow).")


def folha(arquivos, destino, larg=360, por_linha=5):
    """Uma imagem única e leve com todas as lâminas lado a lado (para revisar sem abrir cada PNG)."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    if not arquivos:
        return
    alt = int(larg * ALT / LARG)
    por_linha = min(por_linha, len(arquivos))
    linhas = (len(arquivos) + por_linha - 1) // por_linha
    m = 16
    W = por_linha * larg + (por_linha + 1) * m
    H = linhas * (alt + 28) + (linhas + 1) * m
    f = Image.new("RGB", (W, H), "#E9ECF2")
    d = ImageDraw.Draw(f)
    for i, a in enumerate(arquivos):
        im = Image.open(a).convert("RGB").resize((larg, alt))
        x = m + (i % por_linha) * (larg + m)
        y = m + (i // por_linha) * (alt + 28 + m)
        f.paste(im, (x, y + 28))
        d.text((x, y + 6), os.path.splitext(os.path.basename(a))[0], fill="#14213D")
    f.save(destino, quality=82)
    print("Folha de revisão (use esta para revisar):", destino)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    saida = a[a.index("--saida") + 1] if "--saida" in a else None
    so = {int(x) for x in a[a.index("--laminas") + 1].split(",")} if "--laminas" in a else None
    renderizar(a[0], saida, pdf="--sem-pdf" not in a, so_validar="--so-validar" in a, so=so)
