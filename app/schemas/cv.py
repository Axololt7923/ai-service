from pydantic import BaseModel


class CVParsedResponse(BaseModel):
    chroma_id: str
    skills: list[str]
    experience_years: float
    education_level: str
    languages: list[str]
    summary: str


class RecommendRequest(BaseModel):
    chroma_id: str
    top_k: int = 10


class CVResponse(BaseModel):
    chroma_id: str
    user_id: str
