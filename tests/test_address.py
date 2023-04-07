import project1.main as project1

def test_addressRedaction_single_address():
    data = "My address is 456 Main St, CA, USA."
    result = "My address is 456 \u2588\u2588\u2588\u2588 \u2588\u2588, \u2588\u2588, \u2588\u2588\u2588."
    redacted_data, addresses, count = project1.addressRedaction(data)
    assert redacted_data == result
    assert addresses == {'CA': 'GPE', 'Main St': 'GPE', 'USA': 'GPE'}
    assert count == 3
