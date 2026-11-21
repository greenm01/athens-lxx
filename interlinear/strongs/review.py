"""Print pending Athens lemmas in descending order of occurrence count."""
import argparse
import csv
from collections import defaultdict
from pathlib import Path
import sqlite3
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path)
    args = parser.parse_args()
    candidates = defaultdict(set)
    forms = defaultdict(set)
    for path, key, value, dest in (
        (ROOT / "inventory.tsv", "headword", "strong", candidates),
        (ROOT.parent / "planning/berean-candidates.tsv", "athens_form", "strong_candidate", forms),
    ):
        with path.open(encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                dest[unicodedata.normalize("NFC", row[key])].add(row[value])
    db = sqlite3.connect(args.database.resolve().as_uri() + "?mode=ro", uri=True)
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("lemma", "pending", "grammar", "example", "headword_candidates", "berean_surface_candidates"))
    for lemma, count in db.execute("""SELECT lemma,count(*) FROM analysis WHERE strong_status='pending'
                                      GROUP BY lemma ORDER BY count(*) DESC,lemma"""):
        categories, evidence = set(), set()
        example = None
        for grammar, ref, occurrence, position, surface in db.execute("""
                SELECT grammar,ref,occurrence,position,surface FROM analysis
                JOIN word USING(verse_id,position) JOIN verse ON verse.id=verse_id
                WHERE lemma=? AND strong_status='pending' ORDER BY verse_id,position""", (lemma,)):
            categories.add(grammar.split(",")[0])
            evidence.update(forms.get(unicodedata.normalize("NFC", surface), ()))
            if example is None:
                example = f"{ref} #{occurrence} word {position}"
        writer.writerow((lemma,count," / ".join(sorted(categories)),example,
                         " ".join(sorted(candidates[unicodedata.normalize("NFC",lemma)])),
                         " ".join(sorted(evidence))))


if __name__ == "__main__":
    main()
