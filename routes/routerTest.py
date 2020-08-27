from fastapi import APIRouter
from utils import utils

router = APIRouter()

@router.get('/test/router')
@utils.sleep()
async def test_router():
    return {
        'result': True
    }