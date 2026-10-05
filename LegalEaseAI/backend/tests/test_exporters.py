from backend.services.exporters import (
    format_docx,
    format_pdf,
    format_txt,
)


SAMPLE = """
# EMPLOYMENT CONTRACT

## 1. PARTIES

Alice (Employee), Example Corp (Employer)

## 2. EFFECTIVE DATE

2026-10-04

## 4. TERMS AND CONDITIONS

1. Salary is paid monthly.

2. Confidentiality applies.

"""


def test_txt_export():

    result = format_txt(
        SAMPLE
    )

    assert (
        b"EMPLOYMENT CONTRACT"
        in result
    )


def test_docx_export():

    result = format_docx(
        SAMPLE,
        "Employment Contract",
    )

    # DOCX files are ZIP containers.
    assert result.startswith(
        b"PK"
    )


def test_pdf_export():

    result = format_pdf(
        SAMPLE,
        "Employment Contract",
    )

    assert result.startswith(
        b"%PDF"
    )