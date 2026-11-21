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
            ("1SA 1", 776),
            ("1SA 2", 923),
            ("1SA 3", 485),
            ("1SA 4", 648),
            ("1SA 5", 419),
            ("1SA 6", 624),
            ("AMO 1", 342),
            ("AMO 2", 365),
            ("AMO 3", 308),
            ("AMO 4", 338),
            ("AMO 5", 501),
            ("AMO 6", 290),
            ("AMO 7", 357),
            ("AMO 8", 297),
            ("AMO 9", 430),
            ("DEU 1", 1014),
            ("DEU 2", 840),
            ("EXO 1", 377),
            ("EXO 2", 552),
            ("EXO 3", 601),
            ("EXO 4", 754),
            ("EXO 5", 488),
            ("EXO 6", 570),
            ("EXO 7", 603),
            ("EXO 8", 841),
            ("EXO 9", 841),
            ("EXO 10", 741),
            ("EXO 11", 270),
            ("EXO 12", 1123),
            ("EXO 13", 507),
            ("EXO 14", 796),
            ("EXO 15", 517),
            ("EXO 16", 811),
            ("EXO 17", 377),
            ("EXO 18", 603),
            ("EXO 19", 569),
            ("EXO 20", 511),
            ("EXO 21", 679),
            ("EXO 22", 584),
            ("EXO 23", 722),
            ("EXO 24", 394),
            ("EXO 25", 733),
            ("EXO 26", 770),
            ("EXO 27", 441),
            ("EXO 28", 967),
            ("EXO 29", 1073),
            ("EXO 30", 735),
            ("EXO 31", 348),
            ("EXO 32", 832),
            ("EXO 33", 567),
            ("EXO 34", 832),
            ("EXO 35", 725),
            ("EXO 36", 771),
            ("EXO 37", 395),
            ("EXO 38", 544),
            ("EXO 39", 456),
            ("EXO 40", 675),
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
            ("GEN 24", 1559),
            ("GEN 25", 630),
            ("GEN 26", 759),
            ("GEN 27", 1062),
            ("GEN 28", 529),
            ("GEN 29", 752),
            ("GEN 30", 942),
            ("GEN 31", 1316),
            ("GEN 32", 704),
            ("GEN 33", 426),
            ("GEN 34", 723),
            ("GEN 35", 616),
            ("GEN 36", 692),
            ("GEN 37", 773),
            ("GEN 38", 683),
            ("GEN 39", 579),
            ("GEN 40", 481),
            ("GEN 41", 1166),
            ("GEN 42", 814),
            ("GEN 43", 798),
            ("GEN 44", 769),
            ("GEN 45", 629),
            ("GEN 46", 676),
            ("GEN 47", 861),
            ("GEN 48", 578),
            ("GEN 49", 573),
            ("GEN 50", 570),
            ("HAB 1", 339),
            ("HAB 2", 404),
            ("HAB 3", 372),
            ("HAG 1", 375),
            ("HAG 2", 601),
            ("HOS 1", 268),
            ("HOS 2", 579),
            ("HOS 3", 120),
            ("HOS 4", 366),
            ("HOS 5", 285),
            ("HOS 6", 169),
            ("HOS 7", 320),
            ("HOS 8", 234),
            ("HOS 9", 342),
            ("HOS 10", 295),
            ("HOS 11", 247),
            ("HOS 12", 234),
            ("HOS 13", 321),
            ("HOS 14", 180),
            ("JDG 1", 914),
            ("JDG 2", 609),
            ("JDG 3", 740),
            ("JDG 4", 670),
            ("JDG 5", 553),
            ("JDG 6", 1082),
            ("JDG 7", 824),
            ("JDG 8", 836),
            ("JDG 9", 1402),
            ("JDG 10", 404),
            ("JDG 11", 1058),
            ("JDG 12", 345),
            ("JDG 13", 629),
            ("JDG 14", 589),
            ("JDG 15", 548),
            ("JDG 16", 1003),
            ("JDG 17", 323),
            ("JOL 1", 364),
            ("JOL 2", 779),
            ("JOL 3", 451),
            ("JON 1", 407),
            ("JON 2", 188),
            ("JON 3", 239),
            ("JON 4", 272),
            ("JOS 1", 478),
            ("JOS 2", 673),
            ("JOS 3", 467),
            ("JOS 4", 588),
            ("JOS 5", 492),
            ("JOS 6", 777),
            ("JOS 7", 731),
            ("JOS 8", 1036),
            ("JOS 9", 702),
            ("JOS 10", 1221),
            ("JOS 11", 627),
            ("JOS 12", 375),
            ("JOS 13", 764),
            ("JOS 14", 401),
            ("JOS 15", 977),
            ("JOS 16", 261),
            ("JOS 17", 535),
            ("JOS 18", 630),
            ("JOS 19", 890),
            ("JOS 20", 293),
            ("JOS 21", 1112),
            ("JOS 22", 1094),
            ("JOS 23", 506),
            ("JOS 24", 1061),
            ("LEV 1", 409),
            ("LEV 2", 322),
            ("LEV 3", 404),
            ("LEV 4", 916),
            ("LEV 5", 520),
            ("LEV 6", 642),
            ("LEV 7", 783),
            ("LEV 8", 941),
            ("LEV 9", 527),
            ("LEV 10", 531),
            ("LEV 11", 949),
            ("LEV 12", 195),
            ("LEV 13", 1509),
            ("LEV 14", 1362),
            ("LEV 15", 807),
            ("LEV 16", 929),
            ("LEV 17", 457),
            ("LEV 18", 527),
            ("LEV 19", 705),
            ("LEV 20", 638),
            ("LEV 21", 472),
            ("LEV 22", 683),
            ("LEV 23", 881),
            ("LEV 24", 407),
            ("LEV 25", 1220),
            ("LEV 26", 1021),
            ("LEV 27", 700),
            ("MAL 1", 396),
            ("MAL 2", 434),
            ("MAL 3", 449),
            ("MAL 4", 139),
            ("MIC 1", 327),
            ("MIC 2", 290),
            ("MIC 3", 294),
            ("MIC 4", 353),
            ("MIC 5", 347),
            ("MIC 6", 341),
            ("MIC 7", 443),
            ("NAM 1", 245),
            ("NAM 2", 313),
            ("NAM 3", 387),
            ("NUM 1", 1013),
            ("NUM 2", 532),
            ("NUM 3", 994),
            ("NUM 4", 1173),
            ("NUM 5", 733),
            ("NUM 6", 571),
            ("NUM 7", 1405),
            ("NUM 8", 518),
            ("NUM 9", 540),
            ("NUM 10", 621),
            ("NUM 11", 835),
            ("NUM 12", 284),
            ("NUM 13", 589),
            ("NUM 14", 990),
            ("NUM 15", 808),
            ("NUM 16", 1059),
            ("NUM 17", 270),
            ("NUM 18", 840),
            ("NUM 19", 560),
            ("NUM 20", 651),
            ("NUM 21", 747),
            ("NUM 22", 972),
            ("NUM 23", 607),
            ("NUM 24", 470),
            ("NUM 25", 343),
            ("NUM 26", 1036),
            ("NUM 27", 510),
            ("NUM 28", 547),
            ("NUM 29", 755),
            ("NUM 30", 461),
            ("NUM 31", 1045),
            ("NUM 32", 881),
            ("NUM 33", 805),
            ("NUM 34", 444),
            ("NUM 35", 761),
            ("NUM 36", 339),
            ("OBA 1", 471),
            ("PSA 1", 111),
            ("PSA 2", 164),
            ("PSA 3", 111),
            ("PSA 4", 131),
            ("PSA 5", 201),
            ("PSA 6", 151),
            ("PSA 7", 257),
            ("PSA 8", 136),
            ("PSA 9", 575),
            ("PSA 10", 118),
            ("PSA 11", 128),
            ("PSA 12", 100),
            ("PSA 13", 120),
            ("PSA 14", 87),
            ("PSA 21", 451),
            ("PSA 22", 103),
            ("PSA 50", 282),
            ("PSA 116", 29),
            ("PSA 133", 48),
            ("RUT 1", 538),
            ("RUT 2", 618),
            ("RUT 3", 408),
            ("RUT 4", 541),
            ("ZEC 1", 524),
            ("ZEC 2", 250),
            ("ZEC 3", 249),
            ("ZEC 4", 290),
            ("ZEC 5", 256),
            ("ZEC 6", 330),
            ("ZEC 7", 300),
            ("ZEC 8", 535),
            ("ZEC 9", 358),
            ("ZEC 10", 289),
            ("ZEC 11", 401),
            ("ZEC 12", 363),
            ("ZEC 13", 267),
            ("ZEC 14", 608),
            ("ZEP 1", 423),
            ("ZEP 2", 342),
            ("ZEP 3", 461),
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
        # A reused analysis once assigned the lemma for “land” to Joseph’s name.
        self.assertEqual(
            db.execute(
                "SELECT lemma, count(*) FROM interlinear WHERE ref GLOB 'GEN *' "
                "AND surface IN ('Ἰωσήφ', 'Ἰωσὴφ', 'ΙΩΣΗΦ') AND preference=1 "
                "GROUP BY lemma"
            ).fetchall(),
            [("Ἰωσήφ", 169)],
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
