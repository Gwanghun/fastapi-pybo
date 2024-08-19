from fastapi import APIRouter
from starlette import status
from domain.telegram_bot import parking_check_bot as BOT

router = APIRouter(
    prefix="/api/telegram_bot",
)


@router.get("/get_check_id", status_code=status.HTTP_200_OK)
async def check_id():
    bot = BOT.parking_check_bot()
    await bot.get_check_id()
