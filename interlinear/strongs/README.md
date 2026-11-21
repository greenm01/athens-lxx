# Greek Strong’s numbers

The SQLite database stores one optional decimal-text Strong’s identifier per Athens word analysis. The final column of the interlinear view exposes it for every English preference. Use the analysis table to count words once.

## Current source coverage

| Review state | Lemmas | Word positions |
| --- | ---: | ---: |
| Assigned | 4,080 | 558,759 |
| Pending | 5,805 | 13,326 |
| Reviewed without a number | 4,918 | 28,412 |

Lemma counts can overlap when different occurrences of a lemma have different outcomes. For example, Λίβανος receives G3030 in the four passages where it denotes frankincense. Its place-name occurrences are recorded without that identifier.

A decision identifies the reviewed Greek lemma, including its inflected occurrences. Historical concordances sometimes assign a separate identifier to an inflected form. Cross-edition searches match the identifiers each edition actually supplies.

## Review

Run `python3 -I interlinear/strongs/review.py build/athens.sqlite > review.tsv` to list pending lemmas by frequency, grammar, a sample citation, exact headword candidates, and Berean spelling candidates. Inspect the Athens passages and senses before recording a decision. A missing candidate leaves the lemma pending.

In `lemmas.tsv`, enter a decision once when it applies across the corpus. A row with an empty strong field records a reviewed lemma without a standard identifier. For ambiguous lemmas enter individual decisions in `occurrences.tsv`. The reference, occurrence, and position identify the word, and its exact surface and lemma guard against stale decisions. An occurrence decision takes precedence, including an explicit empty field. The database distinguishes pending from reviewed absence in `analysis.strong_status`.

## Provenance

The offline inventory contains the numeric entries from 1 through 5624 present in the pinned [Dodson XML](https://github.com/biblicalhumanities/Dodson-Greek-Lexicon/blob/74f70358d4acfaf2f980bf2feb58ab7115cbbcbc/dodson.xml), distributed under [CC0](https://github.com/biblicalhumanities/Dodson-Greek-Lexicon/blob/74f70358d4acfaf2f980bf2feb58ab7115cbbcbc/LICENSE). Each row takes the headword and decimal identifier from an entry’s n attribute, removing leading zeroes. The inventory omits some historical Strong’s entries. Extend it only from a documented public-domain source after verifying the identifier. Extended numbering belongs outside this field.

The existing [Berean planning data](../planning/) supplies additional spelling-based leads. Published assignments are Athens editorial decisions under the project’s CC0 dedication.

Three additional entries are attested in Maurice Robinson’s public-domain tagged texts. G1275 occurs as διαπαντός in the [Received Text distribution](https://github.com/byztxt/greektext-textus-receptus/tree/7fd4d02c3e5adebd379ebfbc824040820dde10fc). G1302 and G2444 occur as διατί and ἱνατί in the [Antoniades distribution](https://github.com/byztxt/greektext-antoniades/tree/0ed3c1fe2eb5e983a4729e255429a141dabf11ca). The inventory uses the accented Athens spellings.

For first- and second-person plural personal pronouns, Athens follows the RP2026 tagged text’s lemma-level convention of G1473 and G4771 across cases. The Greek surface, lemma, and grammatical analysis preserve number and case. Strong’s historical concordance also lists separate plural forms, including G2249 and G5210.

The [same Received Text distribution](https://github.com/byztxt/greektext-textus-receptus/tree/7fd4d02c3e5adebd379ebfbc824040820dde10fc/parsed) attests G1002 in Hebrews, G3390 in the subscription to 1 Timothy, G3720 in Revelation, and G3872 in 1 and 2 Timothy. The inventory records the corresponding accented Athens headwords.
