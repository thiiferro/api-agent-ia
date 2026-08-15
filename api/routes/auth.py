from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(
    prefix="/auth",
    tags=["Acesso"],
    responses={404: {"description": "Not Found"}}
)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    pass


@router.post("/register")
async def register():
    pass