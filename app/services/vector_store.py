import uuid
from typing import Any

from fastapi import HTTPException

from app.config import cv_collection, job_collection
from app.schemas.cv import CVResponse, CVParsedResponse
from app.schemas.job import JobResponse, JobMatch
from app.services.cv_parser import extract_text_from_pdf, parse_cv
from app.services.embedder import embed


SEPARATE_TEXT = "."


def upsert_cv(chroma_id: str, document: str, embedding: list[float], metadata: dict):
    cv_collection.upsert(
        ids=[chroma_id],
        embeddings=[embedding],
        documents=[document],
        metadatas=[metadata]
    )



def upsert_job(job_id: str, title: str, description: str, requirements: str, company: str) -> str:
    document = f"{title}{SEPARATE_TEXT}{description}{SEPARATE_TEXT}{requirements}"
    chroma_id = f"job_{job_id}"
    embedding = embed(document)
    metadata = {"title": title, "company": company} if company \
        else {"title": title, "company": "unknown"}

    job_collection.upsert(
        ids=[chroma_id],
        embeddings=[embedding],
        documents=[document],
        metadatas=[metadata]
    )

    return chroma_id


def get_job(chroma_id: str) -> JobResponse:
    job = job_collection.get(
        ids=[f"job_{chroma_id}"],
        include=["metadatas"]
    )
    if len(job["ids"]) == 0:
        raise HTTPException(status_code=404, detail="Job is not exist")
    return JobResponse(
        job_id=job["ids"][0][4:],
        title=job["metadatas"][0]["title"],
        company=job["metadatas"][0]["company"],
    )


def get_cv_embedding(chroma_id: str) -> list[float] | None:
    result = cv_collection.get(
        ids=[chroma_id],
        include=["embeddings"]
    )
    if len(result["ids"]) == 0:
        raise HTTPException(status_code=404, detail="Cv is not exist")

    return result["embeddings"][0]


def find_matching_jobs_help(cv_embedding: list[float], top_k: int = 10) -> list[dict]:
    results = job_collection.query(
        query_embeddings=[cv_embedding],
        n_results=top_k,
        include=["metadatas", "distances"]
    )
    matches = []

    for job_id, dist in zip(results["ids"][0], results["distances"][0]):
        matches.append({
            "job_id": job_id,
            "similarity": round(1 - dist, 4)
        })

    return matches


def find_matching_jobs(chroma_id: str, top_k: int = 10) -> list[JobMatch]:
    cv_embedding = get_cv_embedding(f"cv_{chroma_id}")
    if cv_embedding is None:
        raise HTTPException(status_code=404, detail="CV is not exist")
    if top_k > 10:
        raise HTTPException(status_code=400, detail="Top k must be less or equal 10")
    matches = find_matching_jobs_help(cv_embedding, top_k=top_k)
    return [
        # return the id you put in the chroma_id
        JobMatch(job_id=m["job_id"][4:], similarity=m["similarity"])
        for m in matches
    ]


def get_all_cv_info(limit: int, offset: int) -> list[CVResponse]:
    begin_idx, range_return, all_cv = get_collection_object(cv_collection, limit, offset)

    return [CVResponse(
        chroma_id=all_cv["ids"][i][3:],
        user_id=all_cv["metadatas"][i]["user_id"])
        for i in range(begin_idx, range_return)
    ]


def get_all_job(limit: int, offset: int) -> list[JobResponse]:
    begin_idx, range_return, all_jobs = get_collection_object(job_collection, limit, offset)

    return [JobResponse(
        job_id=all_jobs["ids"][i][4:],
        title=all_jobs["metadatas"][i]["title"],
        company=all_jobs["metadatas"][i]["company"])
        for i in range(begin_idx, range_return)
    ]


def delete_cv(chroma_id: str) -> None:
    try:
        cv_collection.delete(ids=[f"cv_{chroma_id}"])
    except:
        raise HTTPException(status_code=404, detail="CV is not exist")


def delete_job(chroma_id: str) -> None:
    try:
        job_collection.delete(ids=[f"job_{chroma_id}"])
    except :
        raise HTTPException(status_code=404, detail="Job is not exist")


def get_collection_object(collection, limit: int, offset: int) -> tuple[int, int, Any]:
    if limit > 25 or limit < 0:
        raise HTTPException(status_code=403, detail="Not valid limit must be between 0 and 25")
    if offset < -1:
        raise HTTPException(status_code=403, detail="Not valid offset must be greater than -1")

    result = collection.get(include=["metadatas"])

    begin_idx = offset if offset < len(result["ids"]) else len(result["ids"]) - 1
    range_return = offset + limit if offset + limit < len(result["ids"]) else len(result["ids"])

    return begin_idx, range_return, result


def process_and_store_cv(file_bytes: bytes, user_id: str) -> CVParsedResponse:

    raw_text = extract_text_from_pdf(file_bytes)
    parsed   = parse_cv(raw_text)

    summary   = parsed.get("summary", raw_text[:500])
    chroma_id = f"cv_{uuid.uuid4().hex}"
    vector    = embed(summary)

    upsert_cv(
        chroma_id=chroma_id,
        document=summary,
        embedding=vector,
        metadata={"user_id": user_id}
    )

    return CVParsedResponse(
        chroma_id=chroma_id[3:],
        skills=parsed.get("skills", []),
        experience_years=parsed.get("experience_years", 0),
        education_level=parsed.get("education_level", "other"),
        languages=parsed.get("languages", []),
        summary=summary
    )