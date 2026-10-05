from __future__ import annotations

from backend.config import Settings
from backend.schemas import DocumentRequest
from backend.utils.sanitize import sanitize_text


SYSTEM_INSTRUCTION = """
You are LegalEase, an AI assistant for drafting legal documents.

Draft a professional, editable legal document from the user's supplied facts.

IMPORTANT RULES:

1. Do not invent names.
2. Do not invent dates.
3. Do not invent monetary amounts.
4. Do not invent addresses.
5. Do not invent jurisdictions.
6. Do not invent obligations that the user did not provide.
7. If an important legal fact is missing, use a placeholder such as:
   [JURISDICTION TO BE CONFIRMED]

Use professional legal drafting language.

Adapt the structure according to the requested document type.

Use this general structure when applicable:

# DOCUMENT TITLE

## 1. PARTIES

## 2. EFFECTIVE DATE

## 3. PURPOSE / SCOPE

## 4. TERMS AND CONDITIONS

## 5. CONFIDENTIALITY

## 6. TERMINATION

## 7. GOVERNING LAW

## 8. GENERAL PROVISIONS

## 9. SIGNATURES

Not every document needs every section.

Use numbered clauses when useful.

Preserve the user's supplied terms.

Do not claim that the document is guaranteed to be legally valid.

This is an AI-assisted drafting tool and the final document should be
reviewed by an appropriately qualified legal professional.

Return only the legal document.
Do not provide an introduction.
Do not provide explanations outside the document.
"""


class GeminiDocumentGenerator:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = None

        if settings.mock_ai:
            return

        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Add it to .env or set MOCK_AI=true."
            )

        try:
            from google import genai

        except ImportError as exc:
            raise RuntimeError(
                "The google-genai package is missing. "
                "Run: pip install -r requirements.txt"
            ) from exc

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def _build_prompt(
        self,
        request: DocumentRequest,
    ) -> str:

        return f"""
{SYSTEM_INSTRUCTION}

USER INPUTS

Document type:
{request.document_type}

Parties:
{request.parties}

Effective date:
{request.effective_date}

Terms and conditions:
{request.terms}

Generate the final editable legal document now.
"""

    def _mock_document(
        self,
        request: DocumentRequest,
    ) -> str:

        terms = [
            item.strip()
            for item in request.terms.split(";")
            if item.strip()
        ]

        if terms:
            term_lines = "\n".join(
                f"{index}. {term}"
                for index, term in enumerate(terms, start=1)
            )
        else:
            term_lines = "1. [TERMS TO BE CONFIRMED]"

        return f"""
# {request.document_type.upper()}

## 1. PARTIES

{request.parties}

## 2. EFFECTIVE DATE

{request.effective_date}

## 3. PURPOSE / SCOPE

This agreement records the terms agreed between the parties identified above.

## 4. TERMS AND CONDITIONS

{term_lines}

## 5. GENERAL PROVISIONS

The parties agree to act in accordance with the terms stated in this document.

Any missing jurisdiction-specific requirements should be reviewed before signing.

## 6. SIGNATURES

Party 1: ______________________________

Name: ________________________________

Signature: ____________________________

Date: _________________________________


Party 2: ______________________________

Name: ________________________________

Signature: ____________________________

Date: _________________________________
"""

    def generate_document(
        self,
        request: DocumentRequest,
    ) -> str:

        if self.settings.mock_ai:
            return sanitize_text(
                self._mock_document(request)
            )

        prompt = self._build_prompt(request)

        try:

            response = self.client.models.generate_content(
                model=self.settings.gemini_model,
                contents=prompt,
            )

        except Exception as exc:

            raise RuntimeError(
                f"Gemini generation failed: {exc}"
            ) from exc

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return sanitize_text(text)