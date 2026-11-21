# The Athens Septuagint, 1843–1850

*Ἡ Παλαιὰ Διαθήκη κατὰ τοὺς Ἑβδομήκοντα* is the Greek Old Testament printed in Athens in four volumes between 1843 and 1850. This public-domain transcription lets you read, search, and quote the Greek of those volumes. You can start with [Genesis](text/01-GEN.txt), open [the Psalter](text/21-PSA.txt), or [download the whole edition](https://github.com/greenm01/athens-lxx/releases/download/v0.3.0/athens-lxx-0.3.0.zip).

## The word-by-word interlinear

Genesis 1–14 and Psalms 21, 22 and 50 have a literal English gloss and grammatical analysis for every indexed word. These are Psalms 22, 23 and 51 in the King James Bible. In the shepherd psalm, for instance, *ποιμαίνει* means “shepherds” or “tends.” The [v0.3.0 database](https://github.com/greenm01/athens-lxx/releases/download/v0.3.0/athens.sqlite) indexes all four volumes and includes Genesis 1 and the three psalms. Genesis 2–14 are available as TSV files and in a fresh local build.

[Genesis chapter index](interlinear/README.md#reading-the-athens-interlinear) · [Psalm 21](interlinear/PSA-021.tsv) · [Psalm 22](interlinear/PSA-022.tsv) · [Psalm 50](interlinear/PSA-050.tsv) · [Query or build the database](interlinear/README.md)

The print sometimes tells readers how to find their place. In Sirach 30 a Latin notice points ahead to chapter 33, where a passage continues in a different order. The database records the notice as it appears on the page. It also identifies Sirach’s eleven section titles, the closing account in Job, and the parentheses around “all” in Psalm 2:10. [See the marked passages](interlinear/print/passages.tsv)

## How a Greek Bible came from Moscow to Athens

The Athens title page tells readers where the printers got their Greek. They followed a Bible printed in Moscow in 1821. Its Old Testament went back, through Johann Jakob Breitinger’s Zürich edition (1730–1732), to the Oxford Septuagint of Johann Ernst Grabe (1707–1720). Grabe began with Codex Alexandrinus, a fifth-century manuscript. Where he added or substituted words from another source, he used smaller type so that readers could see his hand in the text. The Greek passed from one printed edition to the next without an intervening translation. [Athens, volume I](https://books.google.com/books?id=rio7AAAAcAAJ) · [Swete on Grabe’s edition](https://ccel.org/ccel/swete/greekot/greekot.iii.vi.html) · [Mikhail Seleznev on the Moscow edition, pp. 116–117](https://ccat.sas.upenn.edu/ioscs/bulletin/volumes/jscs50.pdf#page=116)

Greeks living in the Russian Empire undertook the Moscow printing with the Russian Bible Society. The editors favored Alexandrinus because its readings were familiar from late Byzantine manuscripts and the Church Slavonic Bible. Most copies went to Constantinople and cities in Greece. Russian Orthodox parishes continued to worship in Church Slavonic. [Seleznev, pp. 116–117](https://ccat.sas.upenn.edu/ioscs/bulletin/volumes/jscs50.pdf#page=116) · [Lénart de Regt on Scripture in Russian worship](https://translation.bible/wp-content/uploads/2024/07/de-regt-2016-canon-and-biblical-text-in-the-slavonic-tradition-in-russia.pdf)

In Greece, the Holy Synod supported the Athens printing for free distribution to the clergy. Seleznev describes it as the Greek Church’s official text until the early twentieth century. Greek service books also preserve the wording appointed for particular feasts and services. The Church of Greece’s publisher, Apostoliki Diakonia, later issued a different edition, which readers can find on Myriobiblos. [Athens title page](https://books.google.com/books?id=rio7AAAAcAAJ) · [Seleznev, p. 116](https://ccat.sas.upenn.edu/ioscs/bulletin/volumes/jscs50.pdf#page=116) · [Church of Greece on the 1939 edition, p. 64](https://ecclesiagreece.gr/greek/press/ekklisia/material/1939_02_8.pdf#page=8) · [Myriobiblos edition credit](https://www.myriobiblos.gr/bible/ot/default.html)

## Where Swete differs

Henry Barclay Swete chose the fourth-century Codex Vaticanus for his Cambridge Septuagint (1887–1894). He printed its wording wherever the manuscript survived, filled gaps from Alexandrinus or another early manuscript, and recorded other readings at the foot of the page. You can hear the difference a single letter makes in Psalm 22:5, numbered 23:5 in the King James Bible. Athens reads *τὸ ποτήριόν μου*, “my cup.” Swete reads *τὸ ποτήριόν σου*, “your cup.” [Swete’s preface](https://www.katapi.org.uk/OTInGreek/SweteIntro1.htm) · [Athens, volume III, p. 952](https://vatopedi.api.repo.vatopedianheritage.gr/media/vatopedi/digital_presentation_of_cultural_heritage_object/image_media/74f2b721-284a-4cd2-a934-2266459cf1a4/00000022.jpg) · [Swete’s Greek psalm](https://biblehub.com/sepd/psalms/23.htm)

## Reading and checking the draft

The four Athens volumes govern the transcription and the word-by-word English. A reading from Grabe, a service book, or another edition can point a proofreader to a line worth checking. A correction to the Greek needs evidence from the Athens print. At Psalm 22:5, for example, Athens prints *τὸ ποτήριόν μου*, “my cup.” The interlinear follows it. [Athens III, printed p. 952](https://vatopedi.api.repo.vatopedianheritage.gr/media/vatopedi/digital_presentation_of_cultural_heritage_object/image_media/74f2b721-284a-4cd2-a934-2266459cf1a4/00000022.jpg)

The [53 text files](text/) hold 28,732 verse records in UTF-8. Each line starts with a reference, followed by a tab and the Greek. The Psalter uses Septuagint numbering. The [Odes](text/21a-ODA.txt) have their own file. A few references occur more than once. If you import the text, keep those lines in file order.

Three [transcription notes](notes/) record damaged or missing print, supplied verse numbers, and the headings of Daniel’s visions. At Genesis 1:29, release v0.3.0 restores *σπόριμον*, “fit for sowing.” The word breaks across printed pages 2 and 3. The Vatopedi copy also confirms the letters obscured by a hole at Isaiah 30:18–21. Four Psalm pages missing from one scan (pp. 937–938 and 951–952) were transcribed from another copy of the same Athens volume, held at Vatopedi Monastery. If you spot a transcription error, please [open an issue](https://github.com/greenm01/athens-lxx/issues) with the verse, volume, and printed page.

| Printed volume | Contents |
| --- | --- |
| [I · Google Books](https://books.google.com/books?id=rio7AAAAcAAJ) | Genesis through Ruth |
| [II · Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Η_Παλαιὰ_Διαθήκη_Τόμος_Β'.pdf) | 1 Kingdoms through Job |
| [III · Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Η_Παλαιὰ_Διαθήκη_Τόμος_Γ'.pdf) · [Vatopedi copy](https://viewer.app.repo.vatopedianheritage.gr/el/cultural-heritage-object/vatopedi/60) | Psalms through the Twelve Prophets |
| [IV · Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Η_Παλαιὰ_Διαθήκη_Τόμος_Δ'.pdf) | Tobit through Sirach |

## Public domain

The nineteenth-century Greek text is in the public domain. We dedicate our transcription and notes to the public domain under CC0 1.0. You may copy, correct, translate, and redistribute them. If you cite the transcription, please give the release number so readers can find the text you used. [CC0 dedication](LICENSE)
