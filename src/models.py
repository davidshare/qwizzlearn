from .authorisation.models import Role, Permission, RolePermissions, UserRoles
from .authentication.models import User
from .difficulty.models import Difficulty
from .questions.models import Question, QuizQuestion
from .quiz.models import Quiz, QuizAttempt, QuizFeedback, QuizReports, QuizSettings
from .tags.models import Tag
from .categories.models import Category


# Update forward references
User.model_rebuild()
Role.model_rebuild()
Permission.model_rebuild()
Difficulty.model_rebuild()
Question.model_rebuild()
Quiz.model_rebuild()
QuizAttempt.model_rebuild()
QuizFeedback.model_rebuild()
QuizReports.model_rebuild()
QuizSettings.model_rebuild()
Tag.model_rebuild()
Category.model_rebuild()
QuizQuestion.model_rebuild()


# This ensures all models are imported and can be referenced
__all__ = [
    "User", "UserRoles", "RolePermissions", "Role", "Permission",
    "Difficulty", "Question", "Quiz", "QuizAttempt", "QuizFeedback",
    "QuizReports", "QuizSettings", "Tag", "Category", "QuizQuestion"
]
