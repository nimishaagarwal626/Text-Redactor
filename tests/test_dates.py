import spacy
import project1.main as project1

nlp = spacy.load("en_core_web_md")

def test_dates():
    data = "My Birthday is on 06th April 1997."
    result = "My Birthday is on \u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588."
    redactedData, dates, count = project1.dateRedaction(data)
    assert dates == ["06th April 1997"]
    assert redactedData == result
    assert count == 1
