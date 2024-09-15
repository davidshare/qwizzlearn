from fastapi import APIRouter

from .quiz_attempt_router import quiz_attempt_router
from .quiz_feedback_router import quiz_feedback_router
from .quiz_progress_router import quiz_progress_router
from .quiz_report_router import quiz_report_router
from .quiz_schedule_router import quiz_schedule_router
from .quiz_settings_router import quiz_settings_router
from .quiz_router import quiz_router

quizzes_router = APIRouter()

# Include individual routers
quizzes_router.include_router(quiz_router, tags=["Quizzes"])
quizzes_router.include_router(quiz_attempt_router,
                              prefix="/quiz-attempts", tags=["Quiz Attempts"])
quizzes_router.include_router(quiz_feedback_router,
                              prefix="/quiz-feedback", tags=["Quiz Feedback"])
quizzes_router.include_router(quiz_progress_router,
                              prefix="/quiz-progress", tags=["Quiz Progress"])
quizzes_router.include_router(quiz_report_router,
                              prefix="/quiz-reports", tags=["Quiz Reports"])
quizzes_router.include_router(quiz_schedule_router,
                              prefix="/quiz-schedule", tags=["Quiz Schedule"])
quizzes_router.include_router(quiz_settings_router,
                              prefix="/quiz-settings", tags=["Quiz Settings"])
