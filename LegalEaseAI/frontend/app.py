import sys
import html
from pathlib import Path
from datetime import date

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import requests

from backend.services.exporters import (
    create_txt,
    create_docx,
    create_pdf,
)


ROOT = Path(__file__).resolve().parents[1]

LOGO = ROOT / "assets" / "logo.png"

DEFAULT_BACKEND = "http://localhost:8000"


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
    }

    .hero {
        text-align: center;
        padding: 1rem 0 1.5rem;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: .2rem;
    }

    .hero p {
        color: #7d8590;
        font-size: 1.05rem;
    }

    .preview {
        background: #111827;
        color: #f3f4f6;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 24px;
        min-height: 520px;
        max-height: 650px;
        overflow: auto;
        white-space: pre-wrap;
        font-family: Georgia, serif;
        line-height: 1.65;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    if LOGO.exists():
        st.image(
            str(LOGO),
            width=120,
        )

    st.header("Configuration")

    backend_url = st.text_input(
        "Backend URL",
        DEFAULT_BACKEND,
    ).rstrip("/")

    st.caption(
        "Start the FastAPI backend before generating."
    )

    st.divider()

    st.markdown(
        """
        **LegalEase**

        AI-assisted legal document drafting,
        editing and exporting.
        """
    )

    st.warning(
        "AI-generated legal documents should be "
        "reviewed by a qualified legal professional."
    )


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">

        <h1>⚖️ LegalEase</h1>

        <p>
            AI-powered legal document drafting,
            editing and export.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Layout
# --------------------------------------------------

left, right = st.columns(
    [0.9, 1.1],
    gap="large",
)


# --------------------------------------------------
# Input section
# --------------------------------------------------

with left:

    st.subheader(
        "1. Document details"
    )

    document_type = st.text_input(
        "Document type",
        placeholder=(
            "e.g. Freelance Work Contract"
        ),
    )

    parties = st.text_area(
        "Parties involved",
        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),
        height=120,
    )

    terms = st.text_area(
        "Terms & conditions",
        placeholder=(
            "Payment within 30 days of invoice; "
            "Provider delivers work by agreed deadline; "
            "Confidentiality must be maintained"
        ),
        height=180,
        help=(
            "Separate each clause using a semicolon (;)."
        ),
    )

    effective_date = st.date_input(
        "Effective date",
        value=date.today(),
    )

    generate = st.button(
        "✨ Generate Document",
        type="primary",
        use_container_width=True,
    )

    if generate:

        if not document_type.strip():

            st.error(
                "Please enter the document type."
            )

        elif not parties.strip():

            st.error(
                "Please enter the parties."
            )

        elif not terms.strip():

            st.error(
                "Please enter the terms."
            )

        else:

            payload = {
                "document_type": document_type,
                "parties": parties,
                "terms": terms,
                "effective_date": effective_date.isoformat(),
            }

            with st.spinner(
                "Drafting your legal document..."
            ):

                try:

                    response = requests.post(
                        f"{backend_url}/generate",
                        json=payload,
                        timeout=120,
                    )

                    response.raise_for_status()

                    result = response.json()

                    st.session_state.document = (
                        result["document"]
                    )

                    st.session_state.model = (
                        result.get(
                            "model",
                            "",
                        )
                    )

                    st.session_state.mock = (
                        result.get(
                            "mock",
                            False,
                        )
                    )

                    st.success(
                        "Document generated successfully."
                    )

                except requests.RequestException as exc:

                    detail = ""

                    if getattr(
                        exc.response,
                        "text",
                        None,
                    ):

                        detail = (
                            f" — {exc.response.text}"
                        )

                    st.error(
                        "Could not connect to the "
                        f"backend{detail}"
                    )


# --------------------------------------------------
# Preview / editor
# --------------------------------------------------

with right:

    st.subheader(
        "2. Preview & edit"
    )

    if "document" not in st.session_state:

        st.info(
            "Your generated document will appear here."
        )

    else:

        if st.session_state.get(
            "mock",
            False,
        ):

            st.warning(
                "MOCK_AI is enabled. "
                "This output is for testing only."
            )

        edited = st.text_area(
            "Editable document",
            value=st.session_state.document,
            height=560,
            label_visibility="collapsed",
        )

        st.session_state.document = edited

        st.caption(
            f"Model: "
            f"{st.session_state.get('model', 'configured model')}"
        )

        # --------------------------------------------------
        # Download buttons
        # --------------------------------------------------

        c1, c2, c3 = st.columns(3)

        base_name = "".join(
            character
            if character.isalnum()
            or character in "-_"
            else "_"
            for character in document_type.lower().strip()
        ) or "legalease_document"

        with c1:

            st.download_button(
                "⬇️ TXT",

                data=create_txt(
                    edited
                ),

                file_name=(
                    f"{base_name}.txt"
                ),

                mime="text/plain",

                use_container_width=True,
            )

        with c2:

            st.download_button(
                "⬇️ DOCX",

                data=create_docx(
                    edited,
                    document_type,
                ),

                file_name=(
                    f"{base_name}.docx"
                ),

                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),

                use_container_width=True,
            )

        with c3:

            st.download_button(
                "⬇️ PDF",

                data=create_pdf(
                    edited,
                    document_type,
                ),

                file_name=(
                    f"{base_name}.pdf"
                ),

                mime="application/pdf",

                use_container_width=True,
            )

        # --------------------------------------------------
        # HTML preview
        # --------------------------------------------------

        st.markdown(
            "### Rendered preview"
        )

        safe_document = html.escape(
            edited
        )

        st.markdown(
            f"""
            <div class="preview">
                {safe_document}
            </div>
            """,
            unsafe_allow_html=True,
        )