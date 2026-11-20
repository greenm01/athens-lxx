# Reading the Athens interlinear

The Greek comes from the 53 files in the [published transcription](../text/). All 600,497 word occurrences are indexed. The six verses of Psalm 22 have 103 words, including the title, and 149 English glosses. The glosses are a first editorial draft. Elsewhere, an empty gloss means the English is still to come.

Open the release’s `athens.sqlite` in any SQLite reader. This query shows the preferred English for each word in the first verse.

```sql
SELECT position, surface, lemma, grammar, english
FROM interlinear
WHERE ref = 'PSA 22:1' AND occurrence = 1 AND preference = 1
ORDER BY position;
```

To see every proposed rendering of *ποιμαίνω*, search for `lemma = 'ποιμαίνω'` and order by verse, position, and preference. Each alternative belongs to a particular word in a particular verse.

## How to cite a word

Give the Greek text release, the printed reference, the occurrence of that reference, and the word’s position. Within text release v0.1.0 and word numbering version 1, *ποιμαίνει* is Psalm 22:1, first occurrence, word 5. Both counts begin at one. Sirach repeats some verse numbers. Counting each occurrence preserves both lines. The numeric database key for a verse is internal.

The `verse.text` field preserves the whole line, including punctuation, parentheses, and headings. Each word points into that line with zero-based character offsets, the end offset excluded. Elision marks stay with the preceding word. A hyphen separates two indexed parts. The search key folds case and diacritics for lookup. Always quote the printed spelling in `surface`. The three transcription notes files are also available in the `edition_note` table.

## Building and editing

From the repository root, run `python3 -I interlinear/build.py`. This builds `build/athens.sqlite` using Python’s standard library. Each tab-separated row gives one English gloss. Preference 1 carries the lemma and grammar. A higher number gives an alternative. The builder checks every annotated spelling and the fingerprint of the entire Greek edition before replacing the database.

For a second opinion on a form, a reviewer can run the command below with a locally built copy of Perseus Morpheus. Its candidates use Beta Code. An empty candidate field means the parser returned no analysis. It can offer several parses for one spelling. The editor chooses the one that fits the verse. In Psalm 22:1 the subject *Κύριος* tells us that *ποιμαίνει* is third-person active. [Morpheus source and build instructions](https://github.com/perseids-tools/morpheus/tree/ab6898ffed335fc6169fa02c9940657a9b5a78e0)

```sh
python3 -I interlinear/suggest.py build/athens.sqlite /path/to/morpheus 'PSA 22:1'
```

The original English glosses and editorial analyses share the project’s [CC0 dedication](../LICENSE).
