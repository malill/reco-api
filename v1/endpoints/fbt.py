from fastapi import APIRouter

router = APIRouter()


@router.get("/a")
def hello_a():
    return {"message": "Hello A RECO-REST API..."}


@router.get("/b")
def hello_b():
    return {"message": "Hello B RECO-REST API..."}
