"""Keep word citations stable across rebuilds of the same edition."""

import hashlib
import sqlite3
import unittest

from build import build


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
            "2311fa6dcb76a73cf84dc104afd4efd247137122e4f9201b95150ebc4fac02b7",
        )
        self.assertEqual(
            db.execute(
                "SELECT count(DISTINCT occurrence) FROM verse WHERE ref='SIR 30:24b'"
            ).fetchone()[0],
            2,
        )
        self.assertEqual(
            db.execute(
                "SELECT count(*) FROM interlinear WHERE ref LIKE 'PSA 22:%' "
                "AND (preference=1 OR preference IS NULL) AND english IS NULL"
            ).fetchone()[0],
            0,
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
