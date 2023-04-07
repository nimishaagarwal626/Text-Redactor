import project1.main as project1 

def test_genderRedaction():
    data = 'She is a doctor.'
    result = '\u2588\u2588\u2588 is a doctor.'
    redactedData, gender_list, count = project1.genderRedaction(data)
    assert gender_list == ["She"]
    assert redactedData == result
    assert count == 1