#!/usr/bin/env python3
"""csv2md: convert CSV into a GitHub-flavored Markdown table."""

import argparse
import csv
import io
import re
import sys

__all__ = ["convert"]

_NEWLINES = re.compile(r"\r\n|\r|\n")


def _cell(value):
    value = value.strip()
    value = value.replace("|", "\\|")
    return _NEWLINES.sub("<br>", value)


def _line(cells):
    return "| " + " | ".join(cells) + " |"


def convert(text, delimiter=","):
    """Return a Markdown table for CSV text, with a trailing newline, or "" for no rows."""
    if text.startswith("﻿"):
        text = text[1:]
    rows = [row for row in csv.reader(io.StringIO(text, newline=""), delimiter=delimiter) if row]
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    padded = [[_cell(c) for c in row] + [""] * (width - len(row)) for row in rows]
    lines = [_line(padded[0]), _line(["---"] * width)]
    lines.extend(_line(row) for row in padded[1:])
    return "\n".join(lines) + "\n"


def _delimiter(value):
    if len(value) != 1:
        raise argparse.ArgumentTypeError("delimiter must be a single character")
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(prog="csv2md", description="Convert CSV to a GitHub-flavored Markdown table.")
    parser.add_argument("file", nargs="?", default="-", help="CSV file to read, or - for stdin (default)")
    parser.add_argument("--delimiter", type=_delimiter, default=",", help="field delimiter, a single character (default ,)")
    args = parser.parse_args(argv)
    try:
        if args.file == "-":
            raw = sys.stdin.buffer.read()
        else:
            with open(args.file, "rb") as handle:
                raw = handle.read()
        text = raw.decode("utf-8")
    except OSError as err:
        print(f"csv2md: cannot read {args.file}: {err.strerror or err}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(f"csv2md: {args.file} is not valid UTF-8", file=sys.stderr)
        return 1
    sys.stdout.write(convert(text, args.delimiter))
    return 0


if __name__ == "__main__":
    sys.exit(main())
