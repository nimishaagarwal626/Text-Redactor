import spacy
import project1.main as project1

nlp = spacy.load("en_core_web_md")

def test_names():
    data = "Bob and John Doe work at AB Corp."
    result = "\u2588\u2588\u2588 and \u2588\u2588\u2588\u2588 \u2588\u2588\u2588 work at \u2588\u2588 \u2588\u2588\u2588\u2588\u2588"
    redactedData, namesDict, count = project1.nameRedaction(data)
    assert namesDict == {"Bob": "PERSON", "John Doe": "PERSON", "AB Corp.": "ORG"}
    assert redactedData == result
    assert count == 3
