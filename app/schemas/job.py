from pydantic import BaseModel


class JobUpsertRequest(BaseModel):
    job_id: str
    title: str
    description: str
    requirements: str
    company: str


class JobMatch(BaseModel):
    job_id: str
    similarity: float


class JobResponse(BaseModel):
    job_id : str
    title: str
    company: str