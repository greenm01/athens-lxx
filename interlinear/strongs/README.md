# Greek Strong’s numbers

The SQLite database stores one optional decimal-text Strong’s identifier per Athens word analysis. The final column of the interlinear view exposes it for every English preference. Use the analysis table to count words once.

## First release

| Review state | Lemmas | Word positions |
| --- | ---: | ---: |
| Assigned | 49 | 351,091 |
| Pending | 14,739 | 249,406 |
| Reviewed without a number | 0 | 0 |

A decision identifies the reviewed Greek lemma, including its inflected occurrences. Historical concordances sometimes assign a separate identifier to an inflected form. Cross-edition searches match the identifiers each edition actually supplies.

## Review

Run `python3 -I interlinear/strongs/review.py build/athens.sqlite > review.tsv` to list pending lemmas by frequency, grammar, a sample citation, exact headword candidates, and Berean spelling candidates. Inspect the Athens passages and senses before recording a decision. A missing candidate leaves the lemma pending.

In `lemmas.tsv`, enter a decision once when it applies across the corpus. A row with an empty strong field records a reviewed lemma without a standard identifier. For ambiguous lemmas enter individual decisions in `occurrences.tsv`. The reference, occurrence, and position identify the word, and its exact surface and lemma guard against stale decisions. An occurrence decision takes precedence, including an explicit empty field. The database distinguishes pending from reviewed absence in `analysis.strong_status`.

## Provenance

The offline inventory contains the numeric entries from 1 through 5624 present in the pinned [Dodson XML](https://github.com/biblicalhumanities/Dodson-Greek-Lexicon/blob/74f70358d4acfaf2f980bf2feb58ab7115cbbcbc/dodson.xml), distributed under [CC0](https://github.com/biblicalhumanities/Dodson-Greek-Lexicon/blob/74f70358d4acfaf2f980bf2feb58ab7115cbbcbc/LICENSE). Each row takes the headword and decimal identifier from an entry’s n attribute, removing leading zeroes. The inventory omits some historical Strong’s entries. Extend it only from a documented public-domain source after verifying the identifier. Extended numbering belongs outside this field.

The existing [Berean planning data](../planning/) supplies additional spelling-based leads. Published assignments are Athens editorial decisions under the project’s CC0 dedication.
