#!/usr/bin/env python3
"""Revisão técnica de um vídeo editado (rode no arquivo final e olhe as folhas de quadros).

Uso:
  python3 revisar.py <video.mp4> [--texto roteiro.txt | --palavras words.json] [--lang pt]

Relata:
- duração de vídeo e áudio (devem ser iguais) e volume integrado (LUFS);
- pausas mortas (> 0,35 s abaixo de −38 dB) e trechos congelados (> 0,3 s);
- nova transcrição do áudio final e % de palavras que batem com o texto esperado (alvo ≥ 95%);
- folhas de quadros a 2 fps em <video>_revisao/ para olhar quadro a quadro.
O olhar humano continua obrigatório: texto sobre o rosto, telas ilegíveis no celular,
elementos antes da fala, transições semitransparentes, final com olhar desviado.
"""
import argparse, difflib, json, os, re, subprocess, unicodedata


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def dur(p, s):
    """Duração do stream (v/a). Usa ffprobe; sem ffprobe, decodifica com ffmpeg e lê o último time=."""
    r = sh(["ffprobe", "-v", "error", "-select_streams", f"{s}:0", "-show_entries", "stream=duration", "-of", "csv=p=0", p]) if _has_ffprobe() else None
    if r and r.stdout.strip():
        return r.stdout.strip()
    t = re.findall(r"time=(\d+):(\d+):([\d.]+)", sh(["ffmpeg", "-i", p, "-map", f"0:{s}", "-f", "null", "-"]).stderr)
    return f"{int(t[-1][0]) * 3600 + int(t[-1][1]) * 60 + float(t[-1][2]):.3f}" if t else "?"


def _has_ffprobe():
    from shutil import which
    return which("ffprobe") is not None


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--texto")
    ap.add_argument("--palavras")
    ap.add_argument("--lang", default="pt")
    a = ap.parse_args()
    v = a.video
    d = {s: dur(v, s) for s in "va"}
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", sh(["ffmpeg", "-hide_banner", "-i", v, "-af", "ebur128", "-f", "null", "-"]).stderr)
    print(f"duração vídeo/áudio: {d['v']} / {d['a']}  |  volume: {lufs[-1] if lufs else '?'} LUFS")
    sil = re.findall(r"silence_start: ([\d.]+).*?silence_end: ([\d.]+)", sh(["ffmpeg", "-hide_banner", "-i", v, "-af", "silencedetect=n=-38dB:d=0.35", "-f", "null", "-"]).stderr, re.S)
    print("pausas > 0,35 s:", ", ".join(f"{float(x):.2f}–{float(y):.2f}" for x, y in sil) or "nenhuma")
    fr = re.findall(r"freeze_start: ([\d.]+).*?freeze_end: ([\d.]+)", sh(["ffmpeg", "-hide_banner", "-i", v, "-vf", "freezedetect=n=0.002:d=0.3", "-map", "0:v", "-f", "null", "-"]).stderr, re.S)
    print("trechos congelados > 0,3 s:", ", ".join(f"{float(x):.2f}–{float(y):.2f}" for x, y in fr) or "nenhum")
    outdir = os.path.splitext(v)[0] + "_revisao"
    os.makedirs(outdir, exist_ok=True)
    sh(["ffmpeg", "-v", "error", "-y", "-i", v, "-vf", "fps=2,scale=180:-2,tile=10x4", os.path.join(outdir, "folha-%02d.jpg")])
    print("folhas de quadros:", outdir)
    if a.texto or a.palavras:
        wav = os.path.join(outdir, "a.wav")
        sh(["ffmpeg", "-v", "error", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", wav])
        subprocess.run(["npx", "-y", "hyperframes", "transcribe", "a.wav", "-e", "parakeet", "-l", a.lang, "--json"], cwd=outdir, capture_output=True)
        got = norm(" ".join(w["text"] for w in json.load(open(os.path.join(outdir, "transcript.json")))))
        exp = norm(open(a.texto).read()) if a.texto else norm(" ".join(w["t"] for w in json.load(open(a.palavras))))
        sm = difflib.SequenceMatcher(None, exp, got)
        ok = sum(b.size for b in sm.get_matching_blocks())
        print(f"palavras que batem: {ok}/{len(exp)} ({100 * ok / max(len(exp), 1):.0f}%)")
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "equal":
                print(f"  {tag}: esperado «{' '.join(exp[i1:i2])}» → ouvido «{' '.join(got[j1:j2])}»")


if __name__ == "__main__":
    main()
