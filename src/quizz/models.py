# from typing import Optional
# from datetime import datetime
# from sqlmodel import SQLModel, Field, Column
# import sqlalchemy.dialects.postgresql as pg


# class Quiz(SQLModel):
#     __tablename__ = "quizzes"

#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int
#     title: str
#     description: Optional[str] = None
#     slug: str
#     max_scores: int
#     max_questions: int
#     difficulty: int
#     time_limit: int
#     published: bool = False
#     published_at: datetime = Field(sa_column=Column(
#         pg.TIMESTAMP, default=datetime.now()))
#     created_at: datetime = Field(sa_column=Column(
#         pg.TIMESTAMP, default=datetime.now()))
#     updated_at: datetime = Field(sa_column=Column(
#         pg.TIMESTAMP, default=datetime.now()))
