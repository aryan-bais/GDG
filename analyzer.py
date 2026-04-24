import spacy

nlp = spacy.load("en_core_web_sm")

def anonymize(text):
    doc = nlp(text)
    anonymized = text

    for ent in doc.ents:
        if ent.label_ in ["PERSON", "GPE", "ORG"]:
            anonymized = anonymized.replace(ent.text, f"[{ent.label_}]")

    return anonymized