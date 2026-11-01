#!/usr/bin/env python3
"""Tiene solo i canali di uno o piu' macro gruppi (default: IT).
Uso: python3 filtra_it.py sorgente.m3u playlist-IT.m3u IT
Legge il file riga per riga, quindi regge anche playlist da centinaia di MB."""
import re
import sys

SEP = re.compile(r'\s*[|:»>/\\•·]\s*|\s+[-–—]\s+')
GT = re.compile(r'group-title="([^"]*)"', re.I)


def macro(g):
    if not g:
        return "Senza gruppo"
    s = SEP.split(g)[0].strip() or g
    if s == g and " " in g and len(g) > 14:
        s = g.split()[0]
    return s


def main(src, dst, keep):
    keep = {k.strip().lower() for k in keep.split(",") if k.strip()}
    tot = out_n = 0
    pend = None
    with open(src, encoding="utf-8", errors="replace") as f, \
         open(dst, "w", encoding="utf-8", newline="\n") as out:
        out.write("#EXTM3U\n")
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):
                if line.startswith("#EXTINF"):
                    pend = line
                elif pend is not None and not line.startswith("#EXTM3U"):
                    pend += "\n" + line
                continue
            tot += 1
            if pend is not None:
                m = GT.search(pend)
                if macro(m.group(1).strip() if m else "").lower() in keep:
                    out.write(pend + "\n" + line + "\n")
                    out_n += 1
            pend = None
    print(f"Canali letti: {tot} - tenuti: {out_n}")
    if out_n == 0:
        sys.exit("Nessun canale trovato: non aggiorno la playlist.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "IT")
