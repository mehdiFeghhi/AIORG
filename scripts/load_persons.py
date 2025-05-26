import pandas as pd
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import Column, BigInteger, Integer, String
from app.database import Base

class Person(Base):
    __tablename__ = "people"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    rank = Column(String, nullable=False)

# خواندن CSV
df = pd.read_csv("output_csv/person_info.csv")

# گرفتن session
db: Session = next(get_db())

# افزودن رکوردها با ID مشخص
for _, row in df.iterrows():
    person = Person(
        id=int(row["ID"]),               # دقت کن به lowercase
        name=row["نام"],
        age=int(row["سن"]),
        gender=row["جنسیت"],
        rank=row["رتبه"]
    )
    db.merge(person)  # اگر ID موجود بود، بروزرسانی می‌کنه
db.commit()

print("✅ افراد با موفقیت وارد دیتابیس شدند.")
