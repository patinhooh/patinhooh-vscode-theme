#!/usr/bin/env python3
"""Invert a palette file (Python port of invert-palette.js).

Usage:
  ./scripts/invert_palette.py \
    --input palettes/palette-dark.txt \
    --output palettes/palette-inverted.txt
"""
import argparse
import os
import sys

from lib import Palette


def main():
    ap = argparse.ArgumentParser(description="Invert palette file")
    ap.add_argument("--input", "-i", default="palettes/palette-dark.txt", help="input palette file")
    ap.add_argument("--output", "-o", default="palettes/palette-inverted.map", help="output palette file")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}", file=sys.stderr)
        raise SystemExit(1)

    with open(args.input, "r", encoding="utf8") as f:
        palette_map = f.read()

    out_lines = Palette.invert(palette_map)

    with open(args.output, "w", encoding="utf8") as f:
        f.write("\n".join(out_lines) + ("\n" if out_lines else ""))

    print(f"Inverted {len(out_lines)} colors.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
