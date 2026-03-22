"""Shared utilities for theme scripts: hex helpers, JSONC stripper, and parsers."""

import json
import os
import re
import sys
from typing import Any, Dict, Optional, Tuple

# Matches 8/6/4/3 digit hex tokens
HEX_RE = re.compile(
    r"(#[0-9a-fA-F]{8}|#[0-9a-fA-F]{6}|#[0-9a-fA-F]{4}|#[0-9a-fA-F]{3})\b"
)
SHORT_HEX_RE = re.compile(r"^#[0-9a-fA-F]{3,4}$")


def strip_jsonc(s: str) -> str:
    """Remove // and /* */ comments from JSONC while preserving string literals.

    This walks the input and skips comment sequences only when not inside a
    quoted string, so constructs like "vscode://schemas/..." are preserved.
    """
    out = []
    i = 0
    n = len(s)
    in_string = False
    string_quote = None
    escape = False

    while i < n:
        ch = s[i]
        if in_string:
            out.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == string_quote:
                in_string = False
                string_quote = None
            i += 1
            continue

        # not in string
        if ch == '"' or ch == "'":
            in_string = True
            string_quote = ch
            out.append(ch)
            i += 1
            continue

        # line comment
        if ch == "/" and i + 1 < n and s[i + 1] == "/":
            i += 2
            while i < n and s[i] != "\n":
                i += 1
            continue

        # block comment
        if ch == "/" and i + 1 < n and s[i + 1] == "*":
            i += 2
            while i + 1 < n and not (s[i] == "*" and s[i + 1] == "/"):
                i += 1
            i += 2 if i + 1 < n else 1
            continue

        out.append(ch)
        i += 1

    return "".join(out)


class Color:
    @staticmethod
    def normalize_hex(value: str) -> Optional[str]:
        if not isinstance(value, str):
            raise ValueError(f"Expected string value, got {type(value)}: {value}")

        v = value.strip().lower()
        if not v:
            return ""

        if not v.startswith("#"):
            v = "#" + v

        if re.fullmatch(r"#[0-9a-f]{3}", v) or re.fullmatch(r"#[0-9a-f]{4}", v):
            raise ValueError(f"Short-form hex color not allowed: {value}")

        if not re.fullmatch(r"#[0-9a-f]{6}", v) and not re.fullmatch(
            r"#[0-9a-f]{8}", v
        ):
            raise ValueError(f"Invalid hex color format: {value}")
        return v

    @staticmethod
    def invert_channel(hex2: str) -> str:
        n = int(hex2, 16)
        inv = 255 - n
        return f"{inv:02x}"

    @staticmethod
    def invert_hex_color(hex: str) -> Optional[str]:
        has_alpha = len(hex) == 9
        r = hex[1:3]
        g = hex[3:5]
        b = hex[5:7]
        a = hex[7:9] if has_alpha else ""

        inverted = (
            f"#{Color.invert_channel(r)}{Color.invert_channel(g)}{Color.invert_channel(b)}"
        )
        return f"{inverted}{a}"


class Palette:
    @staticmethod
    def parse_line(line: str) -> Optional[Tuple[str, str]]:
        t = line.strip()
        if not t or t.startswith("//"):
            return None

        m = re.match(r"^(#[0-9a-fA-F]{3,8})\s+(#[0-9a-fA-F]{3,8})$", t)
        if m:
            return m.group(1), m.group(2)

        return None

    @staticmethod
    def load(text: str, map_path: str = None) -> Dict[str, str]:
        out = {}
        for idx, line in enumerate(text.splitlines(), start=1):
            pair = Palette.parse_line(line)
            if not pair:
                continue

            left_raw, right_raw = pair
            a_ok = False
            try:
                a = Color.normalize_hex(left_raw)
                a_ok = True
                b = Color.normalize_hex(right_raw)
                if a and b:
                    out[a] = b

            except ValueError as e:
                loc = f" in {map_path}:" if map_path else ":"
                print(
                    f"Error: short-form hex color '{right_raw if a_ok else left_raw}' found{loc} line {idx}"
                )
                print(f"  {line.strip()}")
                raise SystemExit(2)

        return out

    @staticmethod
    def extract_from_theme(theme_text: str, path: str = None):
        """Extract palette, but error if any short-form hex (#rgb or #rgba) is found.

        Returns sorted list of normalized hex colors.
        """
        normalized = set()
        for idx, line in enumerate(theme_text.splitlines(), start=1):
            for m in HEX_RE.finditer(line):
                try:
                    token = m.group(0)
                    n = Color.normalize_hex(token)
                    if n:
                        normalized.add(n)

                except ValueError as e:
                    loc = f" in {path}:" if path else ":"
                    print(
                        f"Error: short-form hex color '{token}' found{loc} line {idx}"
                    )
                    print(f"  {line.strip()}")
                    raise SystemExit(2)

        return sorted(normalized)

    @staticmethod
    def invert(text: str, map_path: str = None) -> list[str]:
        out_lines = []
        for idx, line in enumerate(text.splitlines(), start=1):
            trimmed = line.strip()
            if not trimmed:
                continue

            try:
                normalized = Color.normalize_hex(trimmed)
                if not normalized:
                    continue
            except ValueError as e:
                loc = f" in {map_path}:" if map_path else ":"
                print(f"Error: short-form hex '{trimmed}' color found{loc} line {idx}")
                print(f"  {line.strip()}")
                raise SystemExit(2)

            inverted = Color.invert_hex_color(normalized)
            if not inverted:
                loc = f" in {map_path}:" if map_path else ":"
                print(
                    f"Error: could not generate inverted color from '{normalized}' found{loc} line {idx}"
                )
                print(f"  {line.strip()}")
                raise SystemExit(2)

            out_lines.append(f"{normalized} {inverted}")

        return out_lines


class Overrides:
    @staticmethod
    def load(path: str) -> Dict[str, str]:
        if not path:
            return {}
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        with open(path, "r", encoding="utf8") as f:
            data = json.load(f)
        normalized = {}
        for k, v in data.items():
            nv = Color.normalize_hex(v)
            if nv:
                normalized[k] = nv
        return normalized


class Patch:
    @staticmethod
    def replace_in_string(
        s: str,
        color_map: Dict[str, str],
        parent_key: str = None,
        input_file: str = None,
    ) -> Tuple[str, int]:
        count = 0

        def repl(m):
            nonlocal count
            token = m.group(0)

            n = Color.normalize_hex(token)
            if not n:
                return token
            if n in color_map:
                count += 1
                return color_map[n]

            return token

        try:
            out = HEX_RE.sub(repl, s)
        except ValueError as e:
            raise SystemExit(2, e.message)

        return out, count

    @staticmethod
    def patch_json(
        obj: Any,
        color_map: Dict[str, str],
        overrides: Dict[str, str],
        parent_key: str = "",
        input_file: str = None,
    ) -> Tuple[Any, int, int]:
        replaced = 0
        overridden = 0

        if isinstance(obj, dict):
            out = {}
            for k, v in obj.items():
                path = k if not parent_key else f"{parent_key}.{k}"
                # Support overrides specified as full dot-paths or as bare keys
                # (common for color keys inside the `colors` object).
                override_key = None
                if path in overrides:
                    override_key = path
                elif k in overrides:
                    override_key = k

                if override_key is not None:
                    out[k] = overrides[override_key]
                    overridden += 1
                    continue
                new_v, r, o = Patch.patch_json(
                    v, color_map, overrides, path, input_file
                )
                out[k] = new_v
                replaced += r
                overridden += o
            return out, replaced, overridden

        if isinstance(obj, list):
            out_list = []
            for idx, item in enumerate(obj):
                path = f"{parent_key}[{idx}]" if parent_key else f"[{idx}]"
                new_item, r, o = Patch.patch_json(
                    item, color_map, overrides, path, input_file
                )
                out_list.append(new_item)
                replaced += r
                overridden += o
            return out_list, replaced, overridden

        if isinstance(obj, str):
            # If the entire value is a hex and there's an override for this key,
            # the caller will have applied it. Here we just perform token replacements.
            new_s, c = Patch.replace_in_string(
                obj, color_map, parent_key=parent_key, input_file=input_file
            )
            replaced += c
            return new_s, replaced, overridden

        return obj, replaced, overridden
