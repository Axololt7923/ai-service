from app.security.security import get_authorize
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from app.services.vector_store import get_all_cv_info, delete_cv, process_and_store_cv
from app.schemas.cv import CVParsedResponse, CVResponse

router = APIRouter(prefix="/cv_parsed", tags=["CV"])

@router.post(path="", response_model=CVParsedResponse)
async def parse_and_embed_cv_process(file: UploadFile = File(...),
                             user_id: str = Form(...),
                             api_key: str = Depends(get_authorize)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF")

    file_bytes = await file.read()

    try:
        response_data = process_and_store_cv(file_bytes, user_id)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# for test only
@router.get("", response_model=list[CVResponse])
async def cv_parsed(api_key: str = Depends(get_authorize), limit: int =25, offset: int = 50):
    return get_all_cv_info(limit, offset)


@router.delete("/{chroma_id}")
async def cv_parsed(chroma_id: str, api_key: str = Depends(get_authorize)):
    delete_cv(chroma_id)
    return {"message": f"Cv have been deleted", "chroma_id": chroma_id}

