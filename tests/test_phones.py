import project1.main as project1

def test_phonesRedaction_multiple_phones():
    # Test case where there are multiple phone numbers to redact
    data = "Please call me at 123-456-7890"
    result = "Please call me at \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588"
    redactedData, phones, count = project1.phonesRedaction(data)
    assert phones == ["123-456-7890"]
    assert redactedData == result
    assert count == 1
