from selective_editor import hello_fn


def test_hello():
    res = hello_fn()
    assert res == "World"
