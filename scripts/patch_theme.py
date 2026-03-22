#!/usr/bin/env python3
"""Create Light theme JSON by patching the Dark theme JSON using a palette mapping file.

Usage:
  ./patch_theme_from_palette.py \
    --map palettes/palette-light.patch \
    --overrides palettes/overrides.json \
    --input themes/patinhooh-dark-theme.json \
    --output themes/patinhooh-light-theme-patched.json

"""
import argparse
import json
import os

from lib import Overrides, Patch, Palette, strip_jsonc


def main():
    ap = argparse.ArgumentParser(
        description="Patch a VS Code theme JSON using a palette mapping and optional overrides"
    )
    ap.add_argument(
        "--map",
        "-m",
        default="palettes/palette-light.map",
        help="palette mapping file",
    )
    ap.add_argument(
        "--input",
        "-i",
        default="themes/patinhooh-dark-theme.json",
        help="input theme JSON",
    )
    ap.add_argument(
        "--overrides",
        "-v",
        default="palettes/overrides.json",
        help="overrides JSON file mapping dot-keys to exact colors",
    )
    ap.add_argument(
        "--output",
        "-o",
        default="themes/patinhooh-light-theme.json",
        help="output theme JSON",
    )
    args = ap.parse_args()

    if not os.path.exists(args.map):
        print(f"Mapping file not found: {args.map}")
        raise SystemExit(1)

    if not os.path.exists(args.input):
        print(f"Input JSON file not found: {args.input}")
        raise SystemExit(1)

    if not os.path.exists(args.overrides):
        print(f"Overrides JSON file not found: {args.overrides}")
        raise SystemExit(1)
        a = 1
        asdf
        a = 1
        a = 1
        asdf
        a = 1

    with open(args.map, "r", encoding="utf8") as f:
        map_text = f.read()

    with open(args.input, "r", encoding="utf8") as f:
        theme_txt = f.read()

    color_map = Palette.load(map_text, args.map)
    overrides = Overrides.load(args.overrides) if args.overrides else {}

    theme_txt = strip_jsonc(theme_txt)
    theme_json = json.loads(theme_txt)
    patched, replaced_count, overridden_count = Patch.patch_json(
        theme_json, color_map, overrides, input_file=args.input
    )

    with open(args.output, "w", encoding="utf8") as f:
        json.dump(patched, f, ensure_ascii=False, indent=2)

    print(f"Loaded mappings: {len(color_map)}")
    print(f"Overrides applied: {len(overrides)} (explicit keys)")
    print(f"Replacements made: {replaced_count}")
    print(f"Overrides applied during traversal: {overridden_count}")
    print(f"Input JSON: {args.input}")
    print(f"Output JSON: {args.output}")


if __name__ == "__main__":
    main()
