from backend.utils.sanitize import sanitize_text


def test_sanitize_normalizes_typography():

    value = sanitize_text(
        "Hello\u2014world\u2019s\n\n\nnext"
    )

    assert value == (
        "Hello-world's\n\nnext"
    )