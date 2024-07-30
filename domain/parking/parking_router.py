from fastapi import APIRouter
from starlette import status
from domain.parking import parking_control as PC

router = APIRouter(
    prefix="/api/parking",
)


@router.post("/register", status_code=status.HTTP_200_OK)
def parking_register(car_number: str):
    print(car_number)
    bot = PC.parking_control(car_number)
    return_data = bot.run()
    return return_data
