from typing import List
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.difficulty.service import Difficulty


class QuizValidator:
    @staticmethod
    async def difficulties_exist(quizzes: List[dict], session: AsyncSession):
        difficulty_list = list(set(quiz.difficulty for quiz in quizzes))

        result = await session.exec(select(Difficulty).where(Difficulty.id.in_(difficulty_list)))
        existing_difficulties = result.all()

        existing_difficulty_ids = [
            difficulty.id for difficulty in existing_difficulties]
        non_existing_difficulties = [
            difficulty for difficulty in difficulty_list if difficulty not in existing_difficulty_ids]

        if non_existing_difficulties:
            raise HTTPException(
                status_code=400,
                detail=f"These difficulties do not exist in the database: {
                    non_existing_difficulties}"
            )

        return existing_difficulty_ids
