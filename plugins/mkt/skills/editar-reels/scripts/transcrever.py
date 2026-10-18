#!/usr/bin/env python3
"""Transcreve takes com tempo por palavra (local, Parakeet via `hyperframes transcribe`).

Uso:
  python3 transcrever.py <pasta_dos_takes> <pasta_saida> [--lang pt] [TAKE ...]

Para cada vídeo (.mov/.mp4/.m4v) gera em <pasta_saida>:
  <take>.wav          áudio mono 16 kHz (reutilizado pelos outros scripts)
  <take>.words.json   [{"text", "start", "end"}] em segundos do take
e imprime a transcrição em blocos separados por pausas, para escolher takes.

Pré-requisito (uma vez): npx hyperframes models install parakeet
Atenção: a transcrição estica o fim da última palavra antes de uma pausa — use o
início das palavras como referência e refine cortes pelo volume do áudio (cortes.py faz isso).
"""
import json, os, subprocess, sys

EXTS = (".mov", ".mp4", ".m4v")


def main():
    args = [a for a in sys.argv[1:]]
    if len(args) < 2:
        sys.exit(__doc__)
    lang = "pt"
    if "--lang" in args:
        i = args.index("--lang"); lang = args[i + 1]; del args[i:i + 2]
    src, out, only = args[0], args[1], set(args[2:])
    os.makedirs(out, exist_ok=True)
    for f in sorted(os.listdir(src)):
        take, ext = os.path.splitext(f)
        if ext.lower() not in EXTS or (only and take not in only):
            continue
        wav = os.path.join(out, f"{take}.wav")
        if not os.path.exists(wav):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(src, f), "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
        dst = os.path.join(out, f"{take}.words.json")
        if not os.path.exists(dst):
            work = os.path.join(out, f".tx-{take}")
            os.makedirs(work, exist_ok=True)
            link = os.path.join(work, "a.wav")
            if not os.path.exists(link):
                os.symlink(os.path.abspath(wav), link)
            subprocess.run(["npx", "-y", "hyperframes", "transcribe", "a.wav", "-e", "parakeet", "-l", lang, "--json"],
                           cwd=work, check=True, capture_output=True)
            words = json.load(open(os.path.join(work, "transcript.json")))
            json.dump([{"text": w["text"], "start": w["start"], "end": w["end"]} for w in words], open(dst, "w"), ensure_ascii=False)
        words = json.load(open(dst))
        print(f"\n===== {take} ({len(words)} palavras)")
        seg, st, last = [], None, None
        for w in words:
            if last is not None and w["start"] - last > 0.7:
                print(f"[{st:7.2f}-{last:7.2f}] " + " ".join(seg)); seg = []
            if not seg:
                st = w["start"]
            seg.append(w["text"]); last = w["end"]
        if seg:
            print(f"[{st:7.2f}-{last:7.2f}] " + " ".join(seg))


if __name__ == "__main__":
    main()
