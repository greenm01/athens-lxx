"""Ask a local Perseus Morpheus checkout for candidate parses of an Athens verse."""

import argparse
import csv
import os
import re
import sqlite3
import subprocess
import sys
import unicodedata
from pathlib import Path

LETTERS = dict(zip("αβγδεζηθικλμνξοπρστυφχψω", "abgdezhqiklmncoprstufxyw", strict=True))
MARKS = {
    "\u0300": "/",
    "\u0301": "/",
    "\u0342": "=",
    "\u0313": ")",
    "\u0314": "(",
    "\u0345": "|",
    "\u0308": "+",
    "\u0304": "_",
    "\u0306": "^",
    "᾽": "'",
    "᾿": "'",
    "’": "'",
    "῎": ")/",
}


def beta_code(word):
    greek = unicodedata.normalize("NFD", word.lower().replace("ς", "σ"))
    return "".join(LETTERS.get(c, MARKS.get(c, c)) for c in greek)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path)
    parser.add_argument(
        "morpheus", type=Path, help="checkout containing bin/cruncher and stemlib"
    )
    parser.add_argument(
        "ref", nargs="+", help='one or more quoted references, e.g. "PSA 22:1"'
    )
    args = parser.parse_args()
    root = args.morpheus.resolve()
    env = dict(os.environ, MORPHLIB=str(root / "stemlib"))
    db = sqlite3.connect(args.database.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        out = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
        out.writerow(
            [
                "ref",
                "occurrence",
                "position",
                "surface",
                "Morpheus candidate (Beta Code)",
            ]
        )
        cache = {}
        for ref in args.ref:
            words = db.execute(
                "SELECT occurrence,position,surface FROM word JOIN verse ON verse_id=id "
                "WHERE ref=? ORDER BY occurrence,position",
                (ref,),
            ).fetchall()
            if not words:
                parser.error(f"unknown verse: {ref}")
            for occurrence, position, form in words:
                query = beta_code(form)
                if query not in cache:
                    result = subprocess.run(
                        [root / "bin/cruncher", "-S"],
                        input=query + "\n",
                        text=True,
                        capture_output=True,
                        env=env,
                        check=True,
                    )
                    cache[query] = [
                        " ".join(x.split())
                        for x in re.findall(r"<NL>(.*?)</NL>", result.stdout, re.DOTALL)
                    ]
                for candidate in cache[query] or [""]:
                    out.writerow([ref, occurrence, position, form, candidate])
    finally:
        db.close()


if __name__ == "__main__":
    main()
