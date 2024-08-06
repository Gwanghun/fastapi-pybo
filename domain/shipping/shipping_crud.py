from fastapi import HTTPException
from sqlalchemy.orm import Session




def get_shipping_list(db: Session):
    query = "SELECT * FROM `shipping_check` ORDER BY `idx` DESC limit 10"
    print(query)
    result = db.fetch_all(query=query)
    if not result:
        raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
    print(result)
    return result
