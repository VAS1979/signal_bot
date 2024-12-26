""" Маршруты FastAPI """

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """ Хэндлер стартовой страницы """
    return {"message": "Hi people"}
