"""Keep word citations stable across rebuilds of the same edition."""

import csv
import hashlib
import io
import sqlite3
import unittest

from build import build
from reuse import list_candidates


class WordCitations(unittest.TestCase):
    def test_released_positions_and_pilot(self):
        db = sqlite3.connect(":memory:")
        self.addCleanup(db.close)
        build(db)
        positions = hashlib.sha256()
        for verse_id, position, start, end in db.execute(
            "SELECT verse_id,position,start,end FROM word ORDER BY verse_id,position"
        ):
            positions.update(f"{verse_id} {position} {start} {end}\n".encode())
        self.assertEqual(
            positions.hexdigest(),
            "a870c5721b85903f0ee445d2193e58999f81e3c8dfda83a296efccd2dfa402f5",
        )
        self.assertEqual(
            db.execute(
                "SELECT count(DISTINCT occurrence) FROM verse WHERE ref='SIR 30:24b'"
            ).fetchone()[0],
            2,
        )
        self.assertEqual(
            db.execute(
                "SELECT substr(ref,1,instr(ref,':')-1) AS passage, count(*), count(english) "
                "FROM interlinear WHERE (preference=1 OR preference IS NULL) AND "
                "substr(ref,1,instr(ref,':')-1) IN ('GEN 1','GEN 2','GEN 3','GEN 4','GEN 5','GEN 6','GEN 7','GEN 8','GEN 9','PSA 21','PSA 22','PSA 50') "
                "GROUP BY passage ORDER BY passage"
            ).fetchall(),
            [
                ("GEN 1", 754, 754), ("GEN 2", 534, 534), ("GEN 3", 587, 587),
                ("GEN 4", 533, 533), ("GEN 5", 476, 476),
                ("GEN 6", 507, 507), ("GEN 7", 531, 531),
                ("GEN 8", 525, 525), ("GEN 9", 573, 573),
                ("PSA 21", 451, 451), ("PSA 22", 103, 103), ("PSA 50", 282, 282),
            ],
        )
        output = io.StringIO()
        list_candidates(db, "GEN 3", output)
        candidates = list(csv.DictReader(io.StringIO(output.getvalue()), delimiter="\t"))
        forms = {row["surface"]: int(row["in_chapter"]) for row in candidates}
        self.assertEqual(sum(forms.values()), 587)
        self.assertFalse(any(row["example_ref"].startswith("GEN 3:") for row in candidates))
        self.assertIn("ὅ", forms)
        self.assertIn("Ὁ", forms)
        self.assertEqual(
            db.execute(
                "SELECT surface,english FROM interlinear WHERE ref='GEN 1:29' "
                "AND position=10 AND preference=1"
            ).fetchone(),
            ("σπόριμον", "fit for sowing"),
        )
        self.assertEqual(
            db.execute(
                "SELECT english FROM interlinear WHERE ref='PSA 22:1' AND position=5 ORDER BY preference"
            ).fetchall(),
            [("shepherds",), ("tends",)],
        )
        self.assertEqual(
            db.execute(
                "SELECT count(*) FROM word JOIN verse ON verse_id=id "
                "WHERE substr(text,start+1,end-start) != surface"
            ).fetchone()[0],
            0,
        )
        self.assertEqual(
            db.execute(
                "SELECT occurrence, greek FROM printed_passages WHERE ref='SIR 30:24b'"
            ).fetchall(),
            [(1, "Περὶ δούλων")],
        )
        self.assertEqual(
            db.execute(
                "SELECT greek,first_word,last_word FROM printed_passages WHERE ref='PSA 2:10'"
            ).fetchone(),
            ("πάντες", 6, 6),
        )
        self.assertEqual(
            db.execute(
                "SELECT ref,greek,pages FROM printed_passages WHERE kind='notice' ORDER BY ref"
            ).fetchall(),
            [("SIR 30:24", None, "1825"), ("SIR 33:11", None, "1829")],
        )
        self.assertEqual(
            db.execute(
                "SELECT ref,greek,printed_notice FROM printed_passages WHERE kind='subscription'"
            ).fetchall(),
            [("PSA 151:7", None, "Ψαλμοὶ ρνʹ καὶ ἰδιόγραφος.")],
        )
