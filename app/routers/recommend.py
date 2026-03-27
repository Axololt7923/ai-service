from fastapi import APIRouter, Depends

from app.schemas.job import JobMatch, JobUpsertRequest, JobResponse
from app.security.security import get_authorize
from app.services.vector_store import upsert_job, get_job, delete_job, get_all_job, find_matching_jobs


router = APIRouter(prefix="/jobs", tags=["Job"])


@router.post(path="")
async def job(request: JobUpsertRequest, api_key: str = Depends(get_authorize)):
    chroma_id = upsert_job(
        job_id=request.job_id,
        title=request.title,
        description=request.description,
        requirements=request.requirements,
        company=request.company,
    )
    return {"message": "Job have been add", "chroma_id": chroma_id}


@router.get("/recommend/{cv_id}", response_model=list[JobMatch])
async def recommend_jobs(cv_id: str, top_k: int = 10, api_key: str = Depends(get_authorize)):
    return find_matching_jobs(cv_id, top_k)


@router.get(path="", response_model=list[JobResponse]|JobResponse)
async def job(job_id: str = None, limit: int =10, offset: int = 0, api_key: str = Depends(get_authorize)):
    if job_id is not None:
        return get_job(job_id)
    return get_all_job(limit, offset)


@router.delete("/{chroma_id}")
async def job(chroma_id: str, api_key: str = Depends(get_authorize)):
    delete_job(chroma_id)
    return {"message": f"Job have been deleted", "chroma_id": chroma_id}



