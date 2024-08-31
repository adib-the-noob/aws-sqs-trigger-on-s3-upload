from fastapi.routing import APIRouter

router = APIRouter()

@router.get('/')
def upload_video():
    return {
        "message" : "hacker"
    }