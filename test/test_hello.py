from selective_editor import hello


def test_hello():
    res = hello()
    assert res == "World"
