# Reading the Athens interlinear

The Greek comes from the 53 files in the [published transcription](../text/). All 600,497 word occurrences are indexed. The four passages below have 1,590 words and 2,157 English glosses, counting alternatives. For a first reading, choose preference 1. Elsewhere an empty gloss means that the English is still to come.

| Athens passage | Greek words | English glosses |
| --- | ---: | ---: |
| [Genesis 1](GEN-001.tsv) | 754 | 951 |
| [Psalm 21](PSA-021.tsv) | 451 | 654 |
| [Psalm 22](PSA-022.tsv) | 103 | 150 |
| [Psalm 50](PSA-050.tsv) | 282 | 402 |

The glosses follow Greek word order. Two Greek words sometimes share an English rendering. At Genesis 1:4, *ἀνὰ μέσον* means “between.” The first row gives the English and the second points back to its partner. Psalm 50:18 does the same for *ἔδωκα ἄν*, “I would have given.” An ellipsis in an imperative leaves room for the noun that follows the verb.

Codex and Claude compared readings of these passages. The analyses are AI-assisted editorial drafts. In Genesis 1:21 the print accents *ζώων* on the first syllable. We take it as the noun “living creatures,” with *ἑρπετῶν* describing how they move. At Psalm 50:19 the scan clearly gives *ἐξουδενώσῃ*. We prefer “you will despise,” taking *ὁ Θεός* as an address. “Will despise” preserves the alternative reading with God as the subject. [Genesis 1:21 in the Greek reader, p. 27](https://williamaross.com/wp-content/uploads/2016/06/discovering-the-septuagint-sample.pdf) · [Psalm 50, Athens III, printed p. 975](https://commons.wikimedia.org/wiki/File:%CE%97_%CE%A0%CE%B1%CE%BB%CE%B1%CE%B9%E1%BD%B0_%CE%94%CE%B9%CE%B1%CE%B8%CE%AE%CE%BA%CE%B7_%CE%A4%CF%8C%CE%BC%CE%BF%CF%82_%CE%93%27.pdf?page=37)

Open the release’s `athens.sqlite` in any SQLite reader. This query shows the preferred English for each word in the first verse.

```sql
SELECT position, surface, lemma, grammar, english
FROM interlinear
WHERE ref = 'PSA 22:1' AND occurrence = 1 AND preference = 1
ORDER BY position;
```

To see every proposed rendering of *ποιμαίνω*, search for `lemma = 'ποιμαίνω'` and order by verse, position, and preference. Each alternative belongs to a particular word in a particular verse.

## How to cite a word

Give the Greek text release, the printed reference, the occurrence of that reference, and the word’s position. Within text release v0.3.0 and word numbering version 1, *ποιμαίνει* is Psalm 22:1, first occurrence, word 5. Both counts begin at one. Sirach repeats some verse numbers. Counting each occurrence preserves both lines. The numeric database key for a verse is internal. All 600,497 word positions from text release v0.1.0 also identify the same occurrences in v0.3.0. The spelling correction at Genesis 1:29, word 10, shifts the character offsets within that verse.

The `verse.text` field preserves the whole line, including punctuation, parentheses, and headings. Each word points into that line with zero-based character offsets, the end offset excluded. Elision marks stay with the preceding word. A hyphen separates two indexed parts. The search key folds case and diacritics for lookup. Always quote the printed spelling in `surface`. The three transcription notes files are also available in the `edition_note` table.

## What appears on the printed page

The `printed_passages` view gives the reference, occurrence, first and last word positions, printed page, and a link to the scan. For Greek text the positions include both ends. For a separately printed notice or subscription the position identifies the preceding Greek word. The printed material occupies its own field. In both Sirach notices the Greek numeral mark is transcribed as ʹ.

Twenty-four features have been checked against the scans. Esther’s colophon runs straight on in 10:3. The superscription to Psalm 151 runs into the psalm, but its closing subscription stands apart in two lines of italic Greek. The records also identify printed parentheses in Genesis 1, Psalm 21 and Isaiah 30. Job’s closing account runs on from the preceding sentence. Psalm 2:10 puts parentheses around *πάντες*. Eight of Sirach’s eleven titles stand on lines of their own. Three run on with the surrounding text (18:30, 20:27 and 23:7). Two Latin notices, after 30:24 and 33:11, point readers to corresponding passages in the Complutensian edition. [Records and page references](print/passages.tsv)

```sql
SELECT ref, occurrence, first_word, last_word, kind, greek, printed_notice, pages
FROM printed_passages WHERE ref = 'SIR 30:24';
```

## Building and editing

From the repository root, run `python3 -I interlinear/build.py`. This builds `build/athens.sqlite` using Python’s standard library. Each tab-separated row gives one English gloss. Preference 1 carries the lemma and grammar. A higher number gives an alternative. The builder checks every annotated spelling and the fingerprint of the entire Greek edition before replacing the database.

For a second opinion on a form, a reviewer can run the command below with a locally built copy of Perseus Morpheus. Its candidates use Beta Code. An empty candidate field means the parser returned no analysis. It can offer several parses for one spelling. The editor chooses the one that fits the verse. In Psalm 22:1 the subject *Κύριος* tells us that *ποιμαίνει* is third-person active. [Morpheus source and build instructions](https://github.com/perseids-tools/morpheus/tree/ab6898ffed335fc6169fa02c9940657a9b5a78e0)

```sh
python3 -I interlinear/suggest.py build/athens.sqlite /path/to/morpheus 'PSA 22:1'
```

The original English glosses and editorial analyses share the project’s [CC0 dedication](../LICENSE).
