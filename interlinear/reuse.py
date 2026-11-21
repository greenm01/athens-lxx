"""List reviewed readings of the printed forms found in an Athens chapter."""

import argparse
import csv
import sqlite3
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


def form_key(surface):
    return unicodedata.normalize("NFC", surface.lower())


def list_candidates(db, chapter, output):
    chapter_rows = db.execute(
        "SELECT v.ref, v.occurrence, w.position, w.surface "
        "FROM verse v JOIN word w ON w.verse_id = v.id "
        "WHERE substr(v.ref, 1, instr(v.ref, ':') - 1) = ? ORDER BY v.id, w.position",
        (chapter,),
    )
    forms = {}
    counts = Counter()
    for ref, occurrence, position, surface in chapter_rows:
        key = form_key(surface)
        forms.setdefault(key, (surface, ref, occurrence, position))
        counts[key] += 1
    if not forms:
        raise ValueError(f"No indexed words in {chapter!r}")

    prior = db.execute(
        "SELECT w.surface, a.lemma, a.grammar, g.english, v.ref, v.occurrence, w.position "
        "FROM analysis a JOIN gloss g USING (verse_id, position) "
        "JOIN word w USING (verse_id, position) JOIN verse v ON v.id = w.verse_id "
        "WHERE g.preference = 1 AND substr(v.ref, 1, instr(v.ref, ':') - 1) <> ? "
        "ORDER BY v.id, w.position",
        (chapter,),
    )
    readings = defaultdict(Counter)
    examples = {}
    for surface, lemma, grammar, english, ref, occurrence, position in prior:
        key = form_key(surface)
        if key in forms:
            reading = (lemma, grammar, english)
            readings[key][reading] += 1
            examples.setdefault((key, reading), (ref, occurrence, position))

    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(("surface", "first_ref", "occurrence", "position", "in_chapter",
                     "prior_uses", "lemma", "grammar", "preferred_english",
                     "example_ref", "example_occurrence", "example_position"))
    for key, first in forms.items():
        if not readings[key]:
            writer.writerow((*first, counts[key], 0, "", "", "", "", "", ""))
        for reading, uses in readings[key].most_common():
            writer.writerow((*first, counts[key], uses, *reading, *examples[key, reading]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path)
    parser.add_argument("chapter", help="printed book code and chapter, e.g. 'GEN 4'")
    args = parser.parse_args()
    db = sqlite3.connect(args.database.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        list_candidates(db, args.chapter, sys.stdout)
    except ValueError as error:
        parser.error(str(error))
    finally:
        db.close()


if __name__ == "__main__":
    main()
