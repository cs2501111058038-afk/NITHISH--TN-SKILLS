from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator,
)

from backend.config import get_settings

from backend.schemas import (
    DocumentRequest,
    DocumentResponse,
)


router = APIRouter(
    prefix="",
    tags=["documents"],
)


@router.post(
    "/generate",
    response_model=DocumentResponse,
)
def generate_document(
    request: DocumentRequest,
) -> DocumentResponse:

    settings = get_settings()

    try:

        # Limit number of semicolon-separated terms.
        term_count = len(
            request.terms.split(";")
        )

        if term_count > settings.max_terms:

            raise HTTPException(
                status_code=422,
                detail=(
                    f"Too many terms. "
                    f"Maximum allowed is "
                    f"{settings.max_terms}."
                ),
            )

        generator = GeminiDocumentGenerator(
            settings
        )

        document = generator.generate_document(
            request
        )

        return DocumentResponse(
            document=document,
            model=settings.gemini_model,
            mock=settings.mock_ai,
        )

    except HTTPException:
        raise

    except RuntimeError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Unexpected generation error: {exc}"
            ),
        ) from exc