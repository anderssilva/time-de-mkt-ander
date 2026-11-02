#!/usr/bin/env python3
"""Folha de tempo do roteiro: quanto dura cada frase falada e onde o vídeo perde gente, antes de gravar.

Uso:
  python3 tempo-roteiro.py roteiro.txt [--alvo 40] [--ppm 155] [--json]
  (uma frase ou bloco por linha; linhas começando com # são ignoradas.
   Também aceita o roteiro.md da peça: lê a coluna "Fala" da tabela do roteiro.)

Avisos:
  - gancho (primeira linha) acima de 3 segundos;
  - trecho com mais de 4 segundos sem mudança de imagem (divida a frase ou mude o que aparece na tela);
  - 3 trechos seguidos sem nada concreto (número, nome, exemplo);
  - final que não retoma o gancho (retomar estimula a segunda visualização);
  - duração acima ou muito abaixo do alvo.

Ritmo padrão: 155 palavras por minuto (fala natural em português). Meça o seu e use --ppm.
Adaptado para português a partir da ideia do beats.py do projeto instagram-agent-skill
(Jake Schincariol, licença MIT).
"""
import json, re, sys, unicodedata

PALAVRA = re.compile(r"[\wÀ-ÿ$%]+", re.U)
CONCRETO = re.compile(r"\d|R\$|\b(?:exemplo|por exemplo|tipo assim|imagine|caso|cliente|empresa)\b|(?<!^)\b[A-ZÁÉÍÓÚ][a-záéíóúãõç]{2,}", re.U)
PARADAS = set("a o e de da do das dos em no na nos nas um uma para por com que se seu sua como mais não nao ou ao é".split())


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFKD", t.lower()) if not unicodedata.combining(c))


def ler(arq):
    with open(arq, encoding="utf-8") as f:
        txt = f.read()
    linhas = []
    if "| Fala" in txt or "|Fala" in txt:
        cab = None
        for l in txt.splitlines():
            if l.strip().startswith("|"):
                cel = [c.strip() for c in l.strip().strip("|").split("|")]
                if cab is None and any(c.lower().startswith("fala") for c in cel):
                    cab = [c.lower() for c in cel]
                    continue
                if cab and not set("".join(cel)) <= set("-: "):
                    i = next(k for k, c in enumerate(cab) if c.startswith("fala"))
                    if i < len(cel) and cel[i]:
                        linhas.append((cel[0], cel[i]))
            elif cab and l.strip() and not l.strip().startswith("|"):
                if linhas:
                    break
        if linhas:
            return linhas
    for l in txt.splitlines():
        l = l.strip()
        if l and not l.startswith("#"):
            linhas.append(("", l))
    return linhas


def analisar(linhas, ppm=155, alvo=None):
    pps = ppm / 60.0
    t, beats, avisos = 0.0, [], []
    for i, (rot, frase) in enumerate(linhas):
        n = len(PALAVRA.findall(frase))
        dur = max(0.8, n / pps + (0.25 if frase.rstrip().endswith((".", "!", "?")) else 0.1))
        beats.append({"inicio": round(t, 1), "duracao": round(dur, 1), "rotulo": rot or ("GANCHO" if i == 0 else ("CTA" if i == len(linhas) - 1 else "")),
                      "fala": frase, "palavras": n, "concreto": bool(CONCRETO.search(frase))})
        t += dur
    total = round(t, 1)
    if beats and beats[0]["duracao"] > 3.0:
        avisos.append(f"O gancho dura {beats[0]['duracao']} s: precisa caber em 3 s. Corte palavras ou divida.")
    for b in beats[1:]:
        if b["duracao"] > 4.0:
            avisos.append(f"Trecho em {fmt(b['inicio'])} dura {b['duracao']} s: divida a frase ou mude o que aparece na tela no meio dele.")
    seq = 0
    for b in beats:
        seq = 0 if b["concreto"] else seq + 1
        if seq == 3:
            avisos.append(f"Três trechos seguidos sem nada concreto até {fmt(b['inicio'])}: coloque um número, nome ou exemplo.")
    if len(beats) >= 2:
        g = {sem_acento(w) for w in PALAVRA.findall(beats[0]["fala"])} - PARADAS
        f = {sem_acento(w) for w in PALAVRA.findall(beats[-1]["fala"] + " " + (beats[-2]["fala"] if len(beats) > 2 else ""))} - PARADAS
        comum = sorted(x for x in g & f if len(x) > 3)
        if comum:
            avisos.append(f"Bom: o final retoma o gancho ({', '.join(comum[:3])}), o que favorece assistir de novo.")
        else:
            avisos.append("O final não retoma o gancho. Repetir uma palavra ou ideia do começo estimula a segunda visualização.")
    if alvo:
        dif = total - alvo
        if dif > 2:
            avisos.append(f"Passa {round(dif, 1)} s do alvo de {alvo} s: corte cerca de {int(dif * pps)} palavras.")
        elif dif < -8:
            avisos.append(f"Fica {round(-dif, 1)} s abaixo do alvo: tudo bem se a ideia está completa; curto costuma reter mais.")
    return {"total_s": total, "palavras": sum(b["palavras"] for b in beats), "ppm": ppm, "alvo_s": alvo, "trechos": beats, "avisos": avisos}


def fmt(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    ppm = float(a[a.index("--ppm") + 1]) if "--ppm" in a else 155
    alvo = float(a[a.index("--alvo") + 1]) if "--alvo" in a else 40
    r = analisar(ler(a[0]), ppm, alvo)
    if "--json" in a:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    print(f"FOLHA DE TEMPO · {r['palavras']} palavras · ~{r['total_s']} s a {int(ppm)} palavras/min · alvo {int(alvo)} s")
    print("=" * 76)
    for b in r["trechos"]:
        marca = "  <- longo" if b["duracao"] > (3 if b["rotulo"] == "GANCHO" else 4) else ""
        print(f"  {fmt(b['inicio'])}  {b['duracao']:4.1f}s  {b['rotulo'][:10]:<10} {b['fala'][:48]}{marca}")
    print("-" * 76)
    for av in r["avisos"]:
        print(f"  - {av}")


if __name__ == "__main__":
    main()
