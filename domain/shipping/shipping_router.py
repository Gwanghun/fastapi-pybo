from fastapi import APIRouter, Depends
from starlette import status
from domain.shipping import shipping_crud
# from database import get_mysql_db

router = APIRouter(
    prefix="/api/shipping",
)

#
# @router.get("/check_list", status_code=status.HTTP_200_OK)
# async def shipping_check_list(db=Depends(get_mysql_db)):
#     result = await shipping_crud.get_shipping_list(db)
#     print(result)
#     return result
