"""Index explicit features in the edition's grammatical descriptions."""
import re

FEATURES = {
    "part_of_speech": "noun article adjective pronoun preposition conjunction adverb particle numeral interjection verb",
    "grammatical_case": "nominative genitive dative accusative vocative",
    "gender": "masculine feminine neuter",
    "grammatical_number": "singular plural dual",
    "tense": "present imperfect future aorist perfect pluperfect",
    "voice": "active middle passive",
    "mood": "indicative subjunctive optative imperative",
    "verb_form": "participle infinitive",
    "person": "first second third",
}


def build_morphology(db):
    columns = ", ".join(FEATURES)
    db.execute(f"CREATE TABLE morphology_features (grammar TEXT PRIMARY KEY, {columns}) WITHOUT ROWID")
    descriptors = set("proper personal name indeclinable possessive demonstrative relative reflexive indefinite interrogative cardinal ordinal postpositive negative coordinating subordinating comparative superlative definite".split())
    vocabulary_words = descriptors.union(*(v.split() for v in FEATURES.values()))
    rows = []
    for grammar, in db.execute("SELECT DISTINCT grammar FROM lexical_concordance WHERE grammar IS NOT NULL"):
        words = set(re.findall(r"[a-z]+", grammar.lower()))
        values = {}
        for field, vocabulary in FEATURES.items():
            matches = words.intersection(vocabulary.split())
            values[field] = matches.pop() if len(matches) == 1 else None
        if values["part_of_speech"] in {"adverb", "preposition"}:
            values["grammatical_case"] = None
        if not values["part_of_speech"] and (values["mood"] or values["verb_form"]):
            values["part_of_speech"] = "verb"
        # A governor's stated case describes its complement.
        governor = re.fullmatch(r"(?:improper )?(preposition|adverb) (?:with (?:the )?)?(?:dative|genitive|accusative)", grammar.lower())
        if governor:
            values = dict.fromkeys(FEATURES)
            values["part_of_speech"] = governor.group(1)
        elif words - vocabulary_words or not re.fullmatch(r"[a-z ,]+", grammar.lower()):
            values = dict.fromkeys(FEATURES)
        rows.append((grammar, *values.values()))
    parameters = ", ".join("?" for _ in range(len(FEATURES) + 1))
    db.executemany(f"INSERT INTO morphology_features VALUES ({parameters})", rows)
    db.execute(f"""CREATE VIEW morphological_concordance AS
                  SELECT c.*, {columns} FROM lexical_concordance c
                  LEFT JOIN morphology_features f USING(grammar)""")
