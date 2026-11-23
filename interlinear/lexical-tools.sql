-- Verified against the ABP Genesis 1 interlinear, verses 1–4.
-- https://biblehub.com/interlinear/apostolic/genesis/1.htm
CREATE TABLE ab_strong_assignment (
    ref TEXT NOT NULL, occurrence INTEGER NOT NULL, position INTEGER NOT NULL,
    surface TEXT NOT NULL, ab_strong TEXT NOT NULL,
    PRIMARY KEY (ref, occurrence, position)
) WITHOUT ROWID;
INSERT INTO ab_strong_assignment VALUES
('GEN 1:1',1,1,'ΕΝ','1722'),
('GEN 1:1',1,2,'ἀρχῇ','746'),
('GEN 1:1',1,3,'ἐποίησεν','4160'),
('GEN 1:1',1,4,'ὁ','3588'),
('GEN 1:1',1,5,'Θεὸς','2316'),
('GEN 1:1',1,6,'τὸν','3588'),
('GEN 1:1',1,7,'οὐρανὸν','3772'),
('GEN 1:1',1,8,'καὶ','2532'),
('GEN 1:1',1,9,'τὴν','3588'),
('GEN 1:1',1,10,'γῆν','1093'),
('GEN 1:2',1,1,'Ἡ','3588'),
('GEN 1:2',1,2,'δὲ','1161'),
('GEN 1:2',1,3,'γῆ','1093'),
('GEN 1:2',1,4,'ἦν','1510.7.3'),
('GEN 1:2',1,5,'ἀόρατος','517'),
('GEN 1:2',1,6,'καὶ','2532'),
('GEN 1:2',1,7,'ἀκατασκεύαστος','180.2'),
('GEN 1:2',1,8,'καὶ','2532'),
('GEN 1:2',1,9,'σκότος','4655'),
('GEN 1:2',1,10,'ἐπάνω','1883'),
('GEN 1:2',1,11,'τῆς','3588'),
('GEN 1:2',1,12,'ἀβύσσου','12'),
('GEN 1:2',1,13,'καὶ','2532'),
('GEN 1:2',1,14,'πνεῦμα','4151'),
('GEN 1:2',1,15,'Θεοῦ','2316'),
('GEN 1:2',1,16,'ἐπεφέρετο','2018'),
('GEN 1:2',1,17,'ἐπάνω','1883'),
('GEN 1:2',1,18,'τοῦ','3588'),
('GEN 1:2',1,19,'ὕδατος','5204'),
('GEN 1:3', 1, 1, 'Καὶ', '2532'),
('GEN 1:3', 1, 2, 'εἶπεν', '2036'),
('GEN 1:3', 1, 3, 'ὁ', '3588'),
('GEN 1:3', 1, 4, 'Θεός', '2316'),
('GEN 1:3', 1, 5, 'γενηθήτω', '1096'),
('GEN 1:3', 1, 6, 'φῶς', '5457'),
('GEN 1:3', 1, 7, 'καὶ', '2532'),
('GEN 1:3', 1, 8, 'ἐγένετο', '1096'),
('GEN 1:3', 1, 9, 'φῶς', '5457'),
('GEN 1:4', 1, 1, 'Καὶ', '2532'),
('GEN 1:4', 1, 2, 'ἴδεν', '1492'),
('GEN 1:4', 1, 3, 'ὁ', '3588'),
('GEN 1:4', 1, 4, 'Θεὸς', '2316'),
('GEN 1:4', 1, 5, 'τὸ', '3588'),
('GEN 1:4', 1, 6, 'φῶς', '5457'),
('GEN 1:4', 1, 7, 'ὅτι', '3754'),
('GEN 1:4', 1, 8, 'καλόν', '2570'),
('GEN 1:4', 1, 9, 'καὶ', '2532'),
('GEN 1:4', 1, 10, 'διεχώρισεν', '1316'),
('GEN 1:4', 1, 11, 'ὁ', '3588'),
('GEN 1:4', 1, 12, 'Θεὸς', '2316'),
('GEN 1:4', 1, 15, 'τοῦ', '3588'),
('GEN 1:4', 1, 16, 'φωτὸς', '5457'),
('GEN 1:4', 1, 17, 'καὶ', '2532'),
('GEN 1:4', 1, 20, 'τοῦ', '3588'),
('GEN 1:4', 1, 21, 'σκότους', '4655');

CREATE VIEW lexical_concordance AS
SELECT i.ref,i.occurrence,i.position,i.surface,i.lemma,i.grammar,i.english,a.ab_strong
FROM interlinear i LEFT JOIN ab_strong_assignment a USING(ref,occurrence,position,surface)
WHERE i.preference=1 OR i.preference IS NULL;
CREATE VIEW english_greek_index AS
SELECT english,lemma,surface,ref,occurrence,position,preference
FROM interlinear WHERE english IS NOT NULL;

CREATE INDEX ab_strong_lookup ON ab_strong_assignment(ab_strong);
CREATE VIEW analytical_lexicon AS
SELECT surface,lemma,grammar,count(*) AS occurrences
FROM lexical_concordance WHERE nullif(lemma,'') IS NOT NULL
GROUP BY surface,lemma,grammar;

-- Fail the staged build if an assignment no longer matches the edition's word.
CREATE TEMP TABLE lexical_check (valid INTEGER CHECK(valid=1));
INSERT INTO lexical_check
SELECT NOT EXISTS (
    SELECT 1 FROM ab_strong_assignment a WHERE NOT EXISTS (
        SELECT 1 FROM lexical_concordance c
        WHERE c.ref=a.ref AND c.occurrence=a.occurrence AND c.position=a.position
          AND c.surface=a.surface AND c.ab_strong=a.ab_strong
    )
);
DROP TABLE lexical_check;

-- Index each distinct gloss once. Occurrence and preference stay edition-specific.
CREATE VIRTUAL TABLE gloss_search USING fts5(english);
INSERT INTO gloss_search SELECT DISTINCT english FROM english_greek_index WHERE english <> '';
CREATE VIEW english_greek_context AS
SELECT e.*, v.text AS greek_verse
FROM english_greek_index e JOIN verse v ON v.ref=e.ref AND v.occurrence=e.occurrence;

CREATE TABLE governed_phrase (
    ref TEXT NOT NULL, occurrence INTEGER NOT NULL, governor_position INTEGER NOT NULL,
    complement_position INTEGER NOT NULL, governed_case TEXT NOT NULL,
    first_surface TEXT NOT NULL, last_surface TEXT NOT NULL,
    PRIMARY KEY(ref, occurrence, governor_position, complement_position)
) WITHOUT ROWID;
INSERT INTO governed_phrase VALUES
('GEN 1:1',1,1,2,'dative','ΕΝ','ἀρχῇ'),
('GEN 1:2',1,10,12,'genitive','ἐπάνω','ἀβύσσου'),
('GEN 1:2',1,17,19,'genitive','ἐπάνω','ὕδατος');

-- ABP prints one identifier for each two-word expression in these editions.
CREATE TABLE ab_strong_phrase (
    ref TEXT NOT NULL, occurrence INTEGER NOT NULL, first_position INTEGER NOT NULL,
    last_position INTEGER NOT NULL CHECK(last_position >= first_position), ab_strong TEXT NOT NULL,
    first_surface TEXT NOT NULL, last_surface TEXT NOT NULL,
    PRIMARY KEY(ref, occurrence, first_position, last_position)
) WITHOUT ROWID;
INSERT INTO ab_strong_phrase VALUES
('GEN 1:4',1,13,14,'303.1','ἀνὰ','μέσον'),
('GEN 1:4',1,18,19,'303.1','ἀνὰ','μέσον');

CREATE TEMP TABLE check_governed_phrase (valid INTEGER NOT NULL CHECK(valid=1));
INSERT INTO check_governed_phrase
SELECT NOT EXISTS (
    SELECT 1 FROM governed_phrase p
    LEFT JOIN lexical_concordance a ON a.ref=p.ref AND a.occurrence=p.occurrence AND a.position=p.governor_position
    LEFT JOIN lexical_concordance b ON b.ref=p.ref AND b.occurrence=p.occurrence AND b.position=p.complement_position
    WHERE a.surface IS NOT p.first_surface OR b.surface IS NOT p.last_surface
);
DROP TABLE check_governed_phrase;

CREATE TEMP TABLE check_ab_strong_phrase (valid INTEGER NOT NULL CHECK(valid=1));
INSERT INTO check_ab_strong_phrase
SELECT NOT EXISTS (
    SELECT 1 FROM ab_strong_phrase p
    LEFT JOIN lexical_concordance a ON a.ref=p.ref AND a.occurrence=p.occurrence AND a.position=p.first_position
    LEFT JOIN lexical_concordance b ON b.ref=p.ref AND b.occurrence=p.occurrence AND b.position=p.last_position
    WHERE a.surface IS NOT p.first_surface OR b.surface IS NOT p.last_surface
);
DROP TABLE check_ab_strong_phrase;
