#!/usr/bin/env python3
"""Extract a normalized palette from a theme JSON or any text file.

Usage:
  ./scripts/extract_palette.py \
    --input themes/patinhooh-dark-theme.json \
    --output scripts/palettes/palette-dark.txt
"""
import argparse
import os
from typing import Optional

from lib import Palette


def main():
    ap = argparse.ArgumentParser(
        description="Extract normalized color palette from a file"
    )
    ap.add_argument("--input", "-i", required=True, help="input file to scan")
    ap.add_argument("--output", "-o", required=True, help="output palette file")

    args = ap.parse_args()

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
        raise SystemExit(1)

    with open(args.input, "r", encoding="utf8") as f:
        theme_txt = f.read()

    palette = Palette.extract_from_theme(theme_txt, args.input)

    with open(args.output, "w", encoding="utf8") as f:
        for c in palette:
            f.write(c + "\n")

    print(f"Extracted {len(palette)} colors.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
