# LegalEase

AI-Powered Legal Document Generator

LegalEase is a FastAPI + Streamlit application for generating,
editing and exporting AI-assisted legal documents.

## Features

- AI legal document generation
- Google Gemini integration
- Employment contracts
- NDAs
- Lease agreements
- Freelance contracts
- Custom document types
- Editable document preview
- TXT export
- DOCX export
- PDF export
- Document branding
- Terms table in DOCX
- PDF header/footer
- FastAPI backend
- Streamlit frontend
- Mock AI mode
- Automated tests
- Docker support
- VS Code debugging

---

# Architecture

```text
                    ┌─────────────────────┐
                    │     Streamlit UI    │
                    │                     │
                    │ Document Inputs     │
                    │ Editor              │
                    │ Downloads           │
                    └──────────┬──────────┘
                               │
                               │ POST /generate
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │                     │
                    │ Validation          │
                    │ API Routes          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Gemini Generator    │
                    │                     │
                    │ Structured Prompt   │
                    │ Gemini API          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Generated Document  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
             TXT              DOCX             PDF