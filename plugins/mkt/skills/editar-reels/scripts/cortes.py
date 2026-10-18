#!/usr/bin/env python3
"""Corta os takes escolhidos, encurta silêncios e monta o a-roll de cada versão com A/V exato.

Uso:
  python3 cortes.py <cortes.json> --palavras <pasta com TAKE.words.json e TAKE.wav> [--saida <pasta>]

cortes.json:
{
  "src": "/pasta/dos/takes",
  "fps": 30, "largura": 1080, "altura": 1920,
  "cor": "original",                 # "original" (padrão: não mexe na cor) | "neutra" (conversão HDR→SDR neutra, só com OK)
  "versoes": {
    "principal": [
      ["IMG_0001", 5.80, 11.30, "gancho", ["manter_inicio"]],   # take, início, fim (s), nome, opções
      ["IMG_0002", 77.95, 86.00, "explica"],
      ["IMG_0003", 206.80, 210.62, "cta", ["congelar_fim"]]
    ]
  }
}
Opções por trecho: "manter_inicio" (não corta o silêncio inicial — ex.: movimento do gancho),
"congelar_fim" (segura o último quadro ~0,5 s), "sem_cortes_internos" (não encurta pausas no meio).

Regras aplicadas (ver SKILL.md, etapa 2):
- limite de fala = ruído de fundo do take + 20 dB (entre −42 e −35 dBFS), janelas de 10 ms;
- início de cada palavra transcrita é protegido (palavras baixas não somem);
- pausas no meio da frase viram ~0,20 s, entre frases ~0,35 s; folgas 50 ms antes / 60 ms depois (160 ms fim de frase);
- todo corte em quadro inteiro; cada pedaço com áudio e vídeo de duração idêntica (sem deriva acumulada).

Saída em <saida>/<versao>/: aroll.mp4, segments.json (trechos e pedaços), words.json (palavras no tempo final).
"""
import argparse, json, math, os, re, struct, subprocess

PAUSA_FRASE, PAUSA_MEIO = 0.35, 0.20
FOLGA_ANTES, FOLGA_DEPOIS, FOLGA_FIM_FRASE = 0.05, 0.06, 0.16
JANELA = 0.01


def run(cmd):
    subprocess.run(cmd, check=True)


def envelope(wav, a, b):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a}", "-t", f"{b - a}", "-i", wav, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True).stdout
    n = len(raw) // 2
    x = struct.unpack(f"<{n}h", raw[: n * 2])
    w = int(16000 * JANELA)
    out = []
    for i in range(0, n - w, w):
        s = x[i:i + w]
        out.append((a + i / 16000, 20 * math.log10(math.sqrt(sum(v * v for v in s) / w) / 32768 + 1e-9)))
    return out


_limites = {}


def limite(wav):
    if wav not in _limites:
        env = sorted(d for _, d in envelope(wav, 0, 600))
        piso = env[int(len(env) * 0.1)] if env else -60
        _limites[wav] = max(-42.0, min(-35.0, piso + 20))
    return _limites[wav]


def fim_de_frase(t, words):
    antes = [w for w in words if w["start"] < t]
    return bool(antes) and bool(re.search(r"[.?!…]$", antes[-1]["text"].strip()))


def pedacos(wav, words, a, b, opts, fps):
    thr = limite(wav)
    prot = [(w["start"] - 0.04, w["start"] + min(0.28, w["end"] - w["start"])) for w in words if w["end"] > a and w["start"] < b]
    # protege palavras baixas, mas só onde há algum som (a transcrição às vezes marca o início cedo demais)
    fala = [t for t, d in envelope(wav, a, b) if d > thr or (d > thr - 12 and any(x <= t <= y for x, y in prot))]
    if not fala:
        return [(a, b)]
    iv, s0, last = [], fala[0], fala[0]
    for t in fala[1:]:
        if t - last > 0.12:
            iv.append((s0, last + JANELA)); s0 = t
        last = t
    iv.append((s0, last + JANELA))
    out = []
    ini = a if "manter_inicio" in opts else max(a, iv[0][0] - FOLGA_ANTES)
    cur = ini
    for (s, e), (ns, _) in zip(iv, iv[1:]):
        gap = ns - e
        keep = PAUSA_FRASE if fim_de_frase(ns, words) else PAUSA_MEIO
        if "sem_cortes_internos" in opts or gap <= keep:
            continue
        out.append((cur, e + keep / 2)); cur = ns - keep / 2
    last_end = iv[-1][1] + (FOLGA_FIM_FRASE if fim_de_frase(b, words) else FOLGA_DEPOIS)
    out.append((cur, min(b, last_end)))
    q = lambda t: round(t * fps) / fps
    res = []
    for pa, pb in out:
        pa, pb = q(pa), q(pb)
        if res and pa - res[-1][1] < 1.5 / fps:
            res[-1] = (res[-1][0], pb)
        elif pb - pa >= 2 / fps:
            res.append((pa, pb))
    return res


def cortar(src_file, a, b, congelar, cfg, out):
    if os.path.exists(out):
        return
    fps, W, H = cfg["fps"], cfg["largura"], cfg["altura"]
    d = b - a
    n = int(round((d + (0.5 if congelar else 0)) * fps))
    T = n / fps
    if cfg.get("cor", "original") == "neutra":
        vf = (f"zscale=w={W}:h={H}:tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,"
              f"zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,fps={fps}")
        tags = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]
    else:
        vf = f"scale={W}:{H}:flags=lanczos,fps={fps}"
        tags = []  # mantém as marcações de cor da origem
    vf += ",tpad=stop_mode=clone:stop_duration=0.5" if congelar else ",tpad=stop_mode=clone:stop=3"
    af = (f"aresample=48000,afade=t=in:d=0.009,afade=t=out:st={max(d - 0.01, 0):.3f}:d=0.009,"
          f"apad=whole_dur={T:.6f},atrim=end={T:.6f}")
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-t", f"{d:.4f}", "-i", src_file, "-vf", vf, "-af", af,
         "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", *tags,
         "-c:a", "pcm_s16le", "-ac", "2", out])


def dur(p, s):
    """Duração do stream (v/a). Usa ffprobe; sem ffprobe, decodifica com ffmpeg e lê o último time=."""
    from shutil import which
    if which("ffprobe"):
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", f"{s}:0", "-show_entries", "stream=duration", "-of", "csv=p=0", p],
                           capture_output=True, text=True).stdout.strip()
        if r:
            return float(r)
    t = re.findall(r"time=(\d+):(\d+):([\d.]+)", subprocess.run(["ffmpeg", "-i", p, "-map", f"0:{s}", "-f", "null", "-"],
                                                                  capture_output=True, text=True).stderr)
    return int(t[-1][0]) * 3600 + int(t[-1][1]) * 60 + float(t[-1][2]) if t else None


def achar_take(src, take):
    for f in os.listdir(src):
        if os.path.splitext(f)[0] == take:
            return os.path.join(src, f)
    raise FileNotFoundError(take)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cortes")
    ap.add_argument("--palavras", required=True)
    ap.add_argument("--saida")
    a = ap.parse_args()
    cfg = json.load(open(a.cortes))
    cfg.setdefault("fps", 30); cfg.setdefault("largura", 1080); cfg.setdefault("altura", 1920)
    base = a.saida or os.path.join(os.path.dirname(os.path.abspath(a.cortes)), "aroll")
    cache = os.path.join(base, ".pedacos"); os.makedirs(cache, exist_ok=True)
    fps = cfg["fps"]
    for ver, linhas in cfg["versoes"].items():
        outdir = os.path.join(base, ver); os.makedirs(outdir, exist_ok=True)
        t, segs, lst = 0.0, [], os.path.join(cache, f"{ver}.txt")
        with open(lst, "w") as f:
            for row in linhas:
                take, ini, fim, nome = row[:4]
                opts = row[4] if len(row) > 4 else []
                words = json.load(open(os.path.join(a.palavras, f"{take}.words.json")))
                wav = os.path.join(a.palavras, f"{take}.wav")
                ps = pedacos(wav, words, ini, fim, opts, fps)
                seg = {"name": nome, "take": take, "range": [ini, fim], "start": round(t, 4), "pieces": []}
                for j, (pa, pb) in enumerate(ps):
                    cong = "congelar_fim" in opts and j == len(ps) - 1
                    out = os.path.join(cache, f"{take}_{pa:.3f}_{pb:.3f}{'_c' if cong else ''}_{cfg.get('cor', 'original')}.mov")
                    cortar(achar_take(cfg["src"], take), pa, pb, cong, cfg, out)
                    d = round((pb - pa + (0.5 if cong else 0)) * fps) / fps
                    seg["pieces"].append({"src_in": pa, "src_out": pb, "start": round(t, 4), "dur": round(d, 4)})
                    f.write(f"file '{out}'\n")
                    t += d
                seg["dur"] = round(t - seg["start"], 4)
                segs.append(seg)
        aroll = os.path.join(outdir, "aroll.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-af", "highpass=f=75,loudnorm=I=-15:TP=-1.5:LRA=9",
             "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(fps),
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", aroll])
        json.dump({"total": round(t, 4), "segments": segs}, open(os.path.join(outdir, "segments.json"), "w"), indent=1)
        words_out = []
        for i, s in enumerate(segs):
            ws = json.load(open(os.path.join(a.palavras, f"{s['take']}.words.json")))
            usadas = set()
            for j, p in enumerate(s["pieces"]):
                for k, w in enumerate(ws):
                    # palavra marcada cedo demais, antes do primeiro som do trecho: encaixa no início do 1º pedaço
                    if j == 0 and k not in usadas and s["range"][0] - 0.02 <= w["start"] and w["end"] <= p["src_in"] + 0.02:
                        usadas.add(k)
                        words_out.append({"t": w["text"], "s": round(p["start"], 3), "e": round(p["start"] + 0.15, 3), "seg": i})
                        continue
                    # a palavra entra no primeiro pedaço com que se sobrepõe (o início marcado pode vir cedo demais)
                    if k in usadas or not (w["end"] > p["src_in"] + 0.02 and w["start"] < p["src_out"] - 0.03):
                        continue
                    usadas.add(k)
                    st = p["start"] + max(w["start"], p["src_in"]) - p["src_in"]
                    en = min(p["start"] + w["end"] - p["src_in"], p["start"] + p["dur"])
                    words_out.append({"t": w["text"], "s": round(st, 3), "e": round(en, 3), "seg": i})
        json.dump(words_out, open(os.path.join(outdir, "words.json"), "w"), ensure_ascii=False)
        # verificação de sincronia
        deriva = sum((dur(l, "a") or 0) - (dur(l, "v") or 0) for l in re.findall(r"file '(.*)'", open(lst).read()))
        print(f"\n== {ver}: {t:.2f}s | deriva A/V acumulada {deriva * 1000:+.0f} ms | aroll v/a {dur(aroll, 'v')}/{dur(aroll, 'a')}")
        for i, s in enumerate(segs):
            print(f"[{i}] {s['name']:14s} {s['start']:6.2f}+{s['dur']:5.2f} ({len(s['pieces'])} pedaços): "
                  + " ".join(f"{w['t']}@{w['s']:.2f}" for w in words_out if w["seg"] == i))


if __name__ == "__main__":
    main()
