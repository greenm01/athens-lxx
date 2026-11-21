import sqlite3
import tempfile
import unittest
from pathlib import Path

from build import SCHEMA, apply_strongs


class StrongDecisions(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.executescript(SCHEMA)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.folder = Path(tmp.name)
        self.write("inventory", "strong\theadword\n1\tx\n2\ty\n")
        self.write("lemmas", "lemma\tstrong\nx\t1\n")
        self.header = "ref\toccurrence\tposition\tsurface\tlemma\tstrong\n"
        self.write("occurrences", self.header)
        for i, lemma in enumerate(("x", "x", "x", "z"), start=1):
            self.db.execute("INSERT INTO verse VALUES(?,?,?,?)", (i, "SIR 1:1", i, "a"))
            self.db.execute("INSERT INTO word VALUES(?,1,'a',0,1,'a')", (i,))
            self.db.execute("INSERT INTO analysis(verse_id,position,lemma,grammar) VALUES(?,1,?,'noun')", (i, lemma))
            for rank in (1, 2):
                self.db.execute("INSERT INTO gloss VALUES(?,1,?,?)", (i, rank, str(rank)))

    def write(self, name, value):
        (self.folder / (name + ".tsv")).write_text(value)

    def test_override_and_explicit_absence(self):
        self.write("occurrences", self.header + "SIR 1:1\t2\t1\ta\tx\t2\nSIR 1:1\t3\t1\ta\tx\t\n")
        apply_strongs(self.db, self.folder)
        self.assertEqual(self.db.execute("SELECT strong,strong_status FROM analysis ORDER BY verse_id").fetchall(),
                         [("1", "assigned"), ("2", "assigned"), (None, "no_number"), (None, "pending")])
        self.assertEqual(self.db.execute("SELECT strong FROM interlinear WHERE occurrence=2").fetchall(), [("2",), ("2",)])

    def test_invalid_decisions(self):
        for body in ("SIR 1:1\t2\t1\ta\tx\t99\n", "SIR 1:1\t2\t1\tb\tx\t2\n",
                     "SIR 1:1\t2\t1\ta\tz\t2\n", "SIR 1:1\t2\t1\ta\tx\t2\n" * 2):
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.write("occurrences", self.header + body)
                apply_strongs(self.db, self.folder)
