"""Build an independent SQLite interlinear from the published Athens transcription."""

import argparse
import csv
import hashlib
import sqlite3
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITION = "v0.1.0"
DIGEST = "37a40e44d43b30237c91ac60b7b5f4f7e8ee709f7ea0f6664ffc51f0c7cd197f"
APOSTROPHES = "᾽᾿’'"
GREEK_PREFIX = "῎"
WORD_ID_VERSION = 1

SCHEMA = """
CREATE TABLE edition (text_release TEXT PRIMARY KEY, text_sha256 TEXT NOT NULL, word_id_version INTEGER NOT NULL);
CREATE TABLE edition_note (file TEXT, line INTEGER, label TEXT, detail TEXT, PRIMARY KEY(file,line)) WITHOUT ROWID;
CREATE TABLE verse (id INTEGER PRIMARY KEY, ref TEXT NOT NULL, occurrence INTEGER NOT NULL,
    text TEXT NOT NULL, UNIQUE(ref, occurrence));
CREATE TABLE word (verse_id INTEGER REFERENCES verse, position INTEGER NOT NULL,
    surface TEXT NOT NULL, start INTEGER NOT NULL, end INTEGER NOT NULL, search_key TEXT NOT NULL,
    PRIMARY KEY(verse_id, position)) WITHOUT ROWID;
CREATE TABLE analysis (verse_id INTEGER, position INTEGER, lemma TEXT NOT NULL, grammar TEXT NOT NULL,
    PRIMARY KEY(verse_id, position), FOREIGN KEY(verse_id,position) REFERENCES word) WITHOUT ROWID;
CREATE TABLE gloss (verse_id INTEGER, position INTEGER, preference INTEGER CHECK(preference >= 1),
    english TEXT NOT NULL, PRIMARY KEY(verse_id,position,preference),
    UNIQUE(verse_id,position,english), FOREIGN KEY(verse_id,position) REFERENCES analysis) WITHOUT ROWID;
CREATE TABLE print_feature (
    feature TEXT PRIMARY KEY, verse_id INTEGER NOT NULL, first_word INTEGER NOT NULL,
    last_word INTEGER NOT NULL CHECK(last_word >= first_word), kind TEXT NOT NULL,
    volume INTEGER NOT NULL, pages TEXT NOT NULL, printed_notice TEXT, scan TEXT NOT NULL,
    observation TEXT NOT NULL,
    FOREIGN KEY(verse_id,first_word) REFERENCES word, FOREIGN KEY(verse_id,last_word) REFERENCES word);
CREATE VIEW printed_passages AS
    SELECT f.feature,v.ref,v.occurrence,f.first_word,f.last_word,f.kind,
           CASE WHEN f.printed_notice IS NULL THEN substr(v.text,a.start+1,b.end-a.start) END AS greek,
           f.printed_notice,f.volume,f.pages,f.scan,f.observation
    FROM print_feature f JOIN verse v ON v.id=f.verse_id
    JOIN word a ON a.verse_id=v.id AND a.position=f.first_word
    JOIN word b ON b.verse_id=v.id AND b.position=f.last_word;
CREATE VIEW interlinear AS
    SELECT v.ref, v.occurrence, w.position, w.surface, a.lemma, a.grammar, g.english, g.preference
    FROM verse v JOIN word w ON v.id=w.verse_id LEFT JOIN analysis a USING(verse_id,position)
    LEFT JOIN gloss g USING(verse_id,position);
"""


def word_spans(line):
    i = 0
    while i < len(line):
        start = i
        if line[i] in GREEK_PREFIX and i + 1 < len(line) and line[i + 1].isalpha():
            i += 1
        if not line[i].isalpha():
            i += 1
            continue
        i += 1
        while i < len(line) and (
            line[i].isalpha() or unicodedata.category(line[i]).startswith("M")
        ):
            i += 1
        if i < len(line) and line[i] in APOSTROPHES:
            i += 1
        yield start, i


def search_key(word):
    return "".join(
        c
        for c in unicodedata.normalize("NFD", word).casefold()
        if unicodedata.category(c)[0] != "M" and c not in APOSTROPHES + GREEK_PREFIX
    )


def add_notes(db):
    for path in sorted((ROOT / "notes").glob("*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            for n, row in enumerate(csv.reader(f, delimiter="\t"), 1):
                if n == 1 and row[0] in ("ref", "label"):
                    continue
                db.execute(
                    "INSERT INTO edition_note VALUES(?,?,?,?)",
                    (path.name, n, row[0], "\t".join(row[1:])),
                )


def add_print_features(db):
    with (ROOT / "interlinear/print/passages.tsv").open(
        encoding="utf-8", newline=""
    ) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            ref, occurrence = row["ref"], int(row["occurrence"])
            positions = (int(row["first_word"]), int(row["last_word"]))
            words = db.execute(
                "SELECT v.id,a.surface,b.surface FROM verse v JOIN word a ON a.verse_id=v.id "
                "JOIN word b ON b.verse_id=v.id WHERE v.ref=? AND v.occurrence=? "
                "AND a.position=? AND b.position=?",
                (ref, occurrence, *positions),
            ).fetchone()
            if not words or words[1:] != (row["first_form"], row["last_form"]):
                raise ValueError(f"Greek anchor changed for {row['feature']}")
            notice = row["printed_notice"] or None
            if (row["kind"] == "notice") != bool(notice) or (
                notice and positions[0] != positions[1]
            ):
                raise ValueError(f"Invalid notice anchor for {row['feature']}")
            db.execute(
                "INSERT INTO print_feature VALUES(?,?,?,?,?,?,?,?,?,?)",
                (
                    row["feature"],
                    words[0],
                    *positions,
                    row["kind"],
                    int(row["volume"]),
                    row["pages"],
                    notice,
                    row["scan"],
                    row["observation"],
                ),
            )


def build(db):
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript(SCHEMA)
    h = hashlib.sha256()
    counts = Counter()
    for path in sorted((ROOT / "text").glob("*.txt")):
        data = path.read_bytes()
        h.update(path.name.encode() + b"\0" + data + b"\0")
        for line in data.decode("utf-8").splitlines():
            ref, greek = line.split("\t")
            counts[ref] += 1
            vid = db.execute(
                "INSERT INTO verse(ref,occurrence,text) VALUES(?,?,?)",
                (ref, counts[ref], greek),
            ).lastrowid
            words = (
                (vid, pos, greek[s:e], s, e, search_key(greek[s:e]))
                for pos, (s, e) in enumerate(word_spans(greek), 1)
            )
            db.executemany("INSERT INTO word VALUES(?,?,?,?,?,?)", words)
    if h.hexdigest() != DIGEST:
        raise ValueError(
            "The Greek differs from the pinned text release. Check word IDs before repinning."
        )
    db.execute("INSERT INTO edition VALUES(?,?,?)", (EDITION, DIGEST, WORD_ID_VERSION))
    for path in sorted((ROOT / "interlinear").glob("*.tsv")):
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                key = (row["ref"], int(row["occurrence"]), int(row["position"]))
                found = db.execute(
                    "SELECT v.id,w.surface FROM verse v JOIN word w ON w.verse_id=v.id "
                    "WHERE v.ref=? AND v.occurrence=? AND w.position=?",
                    key,
                ).fetchone()
                if not found or found[1] != row["surface"]:
                    raise ValueError(f"{path.name}: Greek differs at {key}: {found}")
                wid = (found[0], key[2])
                if int(row["preference"]) == 1:
                    if not (row["lemma"] and row["grammar"]):
                        raise ValueError(f"Missing analysis at {key}")
                    db.execute(
                        "INSERT INTO analysis VALUES(?,?,?,?)",
                        (*wid, row["lemma"], row["grammar"]),
                    )
                elif row["lemma"] or row["grammar"]:
                    raise ValueError(f"Alternative repeats analysis at {key}")
                if not row["english"].strip():
                    raise ValueError(f"Empty gloss at {key}")
                db.execute(
                    "INSERT INTO gloss VALUES(?,?,?,?)",
                    (*wid, int(row["preference"]), row["english"]),
                )
    add_notes(db)
    add_print_features(db)
    db.execute("CREATE INDEX word_search ON word(search_key)")
    db.execute("CREATE INDEX analysis_lemma ON analysis(lemma)")
    db.execute("CREATE INDEX gloss_english ON gloss(english)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output", type=Path, nargs="?", default=ROOT / "build/athens.sqlite"
    )
    out = parser.parse_args().output.resolve()
    if out.suffix != ".sqlite":
        parser.error("output must be a .sqlite file")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        stage = Path(tmp) / "athens.sqlite"
        db = sqlite3.connect(stage)
        try:
            with db:
                build(db)
        finally:
            db.close()
        stage.replace(out)


if __name__ == "__main__":
    main()
