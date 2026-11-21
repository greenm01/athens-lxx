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
        expected_coverage = [
            ("GEN 1", 754),
            ("GEN 2", 534),
            ("GEN 3", 587),
            ("GEN 4", 533),
            ("GEN 5", 476),
            ("GEN 6", 507),
            ("GEN 7", 531),
            ("GEN 8", 525),
            ("GEN 9", 573),
            ("GEN 10", 456),
            ("GEN 11", 599),
            ("GEN 12", 434),
            ("GEN 13", 396),
            ("GEN 14", 523),
            ("GEN 15", 365),
            ("GEN 16", 355),
            ("GEN 17", 584),
            ("GEN 18", 651),
            ("GEN 19", 917),
            ("GEN 20", 427),
            ("GEN 21", 669),
            ("GEN 22", 546),
            ("GEN 23", 434),
            ("PSA 21", 451),
            ("PSA 22", 103),
            ("PSA 50", 282),
        ]
        self.assertEqual(
            db.execute(
                "SELECT substr(ref,1,instr(ref,':')-1) AS passage, count(*), count(english) "
                "FROM interlinear WHERE (preference=1 OR preference IS NULL) AND "
                "substr(ref,1,instr(ref,':')-1) IN (" + ",".join("?" for _ in expected_coverage) + ") "
                "GROUP BY passage ORDER BY substr(passage,1,3), CAST(substr(passage,5) AS INTEGER)",
                [ref for ref, _ in expected_coverage],
            ).fetchall(),
            [(ref, words, words) for ref, words in expected_coverage],
        )
        # These nouns were once assigned a verb parse when expanding a shorthand.
        self.assertEqual(
            db.execute(
                "SELECT ref, position, surface, grammar FROM interlinear WHERE preference=1 "
                "AND lemma IN ('πῆχυς','κατακλυσμός','ὑετός','κόραξ','ἀμπελών') "
                "AND grammar NOT LIKE '%noun%'"
            ).fetchall(),
            [],
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
