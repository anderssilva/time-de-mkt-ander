#!/usr/bin/env python3
"""Gera as artes do perfil na identidade da empresa: capas dos destaques do Instagram e banner do LinkedIn.

Uso:
  python3 artes-perfil.py <artes.json> [--saida <pasta>]

artes.json:
{
  "marca_arquivo": "../../00-contexto/carrossel-marca.json",   (o mesmo arquivo de marca dos carrosséis)
  "destaques": [ {"titulo": "Cases", "icone": "★"}, {"titulo": "Método", "icone": "01"}, ... ],
  "destaques_tema": "escuro",          ("escuro", "claro" ou "destaque": cor de fundo das capas)
  "banner": {"titulo": "Frase de posicionamento", "subtitulo": "o que a empresa faz e para quem", "assinatura": "site ou @"}
}

Saídas (na pasta do artes.json ou em --saida):
  destaque-01-<titulo>.png …  1080 × 1920; o conteúdo fica no círculo central de 600 px (é o que aparece no perfil)
  banner-linkedin.png         1584 × 396; texto à direita, longe da foto de perfil (que cobre a esquerda embaixo)
  folha-perfil.jpg            todas as artes lado a lado, para revisar sem abrir cada uma
"""
import json, os, re, sys, tempfile, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "carrossel", "scripts"))
import renderizar as R  # noqa: E402  (reaproveita fontes e caminhos do gerador de carrossel)


def slug(t):
    t = "".join(ch for ch in unicodedata.normalize("NFKD", t) if not unicodedata.combining(ch))
    t = re.sub(r"[^\w]+", "-", t.lower(), flags=re.U).strip("-")
    return t[:30] or "destaque"


def carregar(arq):
    base = os.path.dirname(os.path.abspath(arq))
    with open(arq, encoding="utf-8") as f:
        d = json.load(f)
    if "marca_arquivo" in d and "marca" not in d:
        marq = R.caminho(base, d["marca_arquivo"])
        if not os.path.exists(marq):
            sys.exit(f"ERRO: marca_arquivo não encontrado: {marq}")
        with open(marq, encoding="utf-8") as f:
            d["marca"] = json.load(f)
        bm = os.path.dirname(marq)
        for k in ("logo", "logo_claro", "marca_dagua"):
            if d["marca"].get(k):
                d["marca"][k] = R.caminho(bm, d["marca"][k])
        for p, f in list((d["marca"].get("fonte_arquivos") or {}).items()):
            d["marca"]["fonte_arquivos"][p] = R.caminho(bm, f)
    if "marca" not in d:
        sys.exit("ERRO: informe 'marca' ou 'marca_arquivo'.")
    return d, base


def estilo_base(m, base):
    c = m["cores"]
    fonte = m.get("fonte", "Montserrat")
    faces = ""
    for peso, arq in (m.get("fonte_arquivos") or {}).items():
        faces += f"@font-face{{font-family:'{fonte}';font-weight:{peso};src:url('{R.url(base, arq)}');}}\n"
    imp = "" if faces or not m.get("fonte_url") else f"@import url('{m['fonte_url']}');\n"
    return imp + faces + f"""*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'{fonte}',sans-serif;color:{c['texto']}}}"""


def html_destaque(item, m, tema):
    c = m["cores"]
    fundo = {"escuro": c["escuro"], "claro": c["fundo"], "destaque": c["destaque"]}.get(tema, c["escuro"])
    cor = c["fundo"] if tema in ("escuro", "destaque") else c["escuro"]
    anel = c["destaque"] if tema != "destaque" else c["fundo"]
    icone = item.get("icone") or item["titulo"][:1].upper()
    tam_ic = 230 if len(icone) <= 2 else 150
    return f"""<div style="width:1080px;height:1920px;background:{fundo};display:flex;align-items:center;justify-content:center">
<div style="width:600px;height:600px;border-radius:50%;border:10px solid {anel};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px">
<div style="font-size:{tam_ic}px;font-weight:800;line-height:1;color:{cor}">{icone}</div>
<div style="font-size:54px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:{cor};max-width:470px;text-align:center;line-height:1.05">{item['titulo']}</div>
</div></div>"""


def html_banner(b, m, base):
    c = m["cores"]
    logo = m.get("logo_claro")
    img = f'<img src="{R.url(base, logo)}" style="height:64px;margin-bottom:22px">' if logo and os.path.exists(logo) else ""
    ass = b.get("assinatura") or m.get("assinatura") or ""
    return f"""<div style="width:1584px;height:396px;background:linear-gradient(110deg,{c['escuro']} 0%,{c['escuro_2']} 100%);position:relative;overflow:hidden">
<div style="position:absolute;left:0;top:0;width:12px;height:100%;background:{c['destaque']}"></div>
<div style="position:absolute;right:96px;top:50%;transform:translateY(-50%);width:880px;text-align:right">
{img}
<div style="font-size:52px;font-weight:800;line-height:1.08;color:{c['fundo']}">{b.get('titulo','')}</div>
<div style="font-size:26px;font-weight:500;margin-top:16px;color:{c['fundo']};opacity:.85">{b.get('subtitulo','')}</div>
<div style="font-size:20px;font-weight:700;margin-top:18px;letter-spacing:.06em;color:{c['destaque_2']}">{ass}</div>
</div></div>"""


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    d, base = carregar(a[0])
    saida = a[a.index("--saida") + 1] if "--saida" in a else base
    os.makedirs(saida, exist_ok=True)
    m = d["marca"]
    est = estilo_base(m, base)
    trabalhos = []
    for i, it in enumerate(d.get("destaques", []), 1):
        trabalhos.append((f"destaque-{i:02d}-{slug(it['titulo'])}.png", 1080, 1920, html_destaque(it, m, d.get("destaques_tema", "escuro"))))
    if d.get("banner"):
        trabalhos.append(("banner-linkedin.png", 1584, 396, html_banner(d["banner"], m, base)))
    if not trabalhos:
        sys.exit("Nada para gerar: informe 'destaques' e/ou 'banner'.")
    from playwright.sync_api import sync_playwright
    feitos = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for nome, w, h, corpo in trabalhos:
            pg = nav.new_page(viewport={"width": w, "height": h})
            doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{est}</style></head><body>{corpo}</body></html>'
            with tempfile.NamedTemporaryFile("w", suffix=".html", dir=base, delete=False, encoding="utf-8") as tf:
                tf.write(doc)
                tmp = tf.name
            try:
                pg.goto("file://" + tmp)
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(150)
                dest = os.path.join(saida, nome)
                pg.screenshot(path=dest, clip={"x": 0, "y": 0, "width": w, "height": h})
                feitos.append(dest)
            finally:
                os.remove(tmp)
                pg.close()
        nav.close()
    for f in feitos:
        print("Gerado:", f)
    try:
        from PIL import Image
        ims = [Image.open(f).convert("RGB") for f in feitos]
        alt = 480
        reds = [im.resize((int(im.width * alt / im.height), alt)) for im in ims]
        W = sum(r.width for r in reds) + 16 * (len(reds) + 1)
        folha = Image.new("RGB", (W, alt + 32), "#E9ECF2")
        x = 16
        for r in reds:
            folha.paste(r, (x, 16))
            x += r.width + 16
        fp = os.path.join(saida, "folha-perfil.jpg")
        folha.save(fp, quality=82)
        print("Folha de revisão (use esta para revisar):", fp)
    except ImportError:
        pass


if __name__ == "__main__":
    main()
