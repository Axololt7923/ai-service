import json
import fitz
from app.config import gemini_model as model


def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join(page.get_text() for page in doc)


def parse_cv(raw_text: str) -> dict:
    prompt = f"""
    Analyze the following CV and extract the following information,
    NOTHING ELSE. Return the result as a JSON object:
    {{
        "skills": ["skill1", "skill2"],
        "experience_years": 0.0,
        "education_level": "bachelor|master|phd|other",
        "languages": ["Vietnamese", "English"],
        "summary": "this is a summary of the CV for embedding",
    }}

    CV:
    {raw_text[:3000]}
    """

    response = model.generate_content(prompt)

    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    return json.loads(text.strip())
