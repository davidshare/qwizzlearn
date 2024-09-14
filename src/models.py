from .authorisation.models import Role, Permission, RolePermissions, UserRoles
from .authentication.models import User
from .difficulty.models import Difficulty
from .quiz.models import Quiz, QuizAttempt, QuizFeedback, QuizReports, QuizSettings, QuizSchedule

from .categories.models import Category
from .groups.models import Group
from .questions.models import Question, QuizQuestion, QuestionTimeTracking

from .tags.models.tags import Tag
from .tags.models.quiz_tag_link import QuizTagLink
from .tags.models.question_tag_link import QuestionTagLink


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
QuizSchedule.model_rebuild()  # Added this line
Tag.model_rebuild()
Category.model_rebuild()
QuizQuestion.model_rebuild()
Group.model_rebuild()
QuestionTagLink.model_rebuild()
QuizTagLink.model_rebuild()
QuestionTimeTracking.model_rebuild()


# This ensures all models are imported and can be referenced
__all__ = [
    "User", "UserRoles", "RolePermissions", "Role", "Permission",
    "Difficulty", "Question", "Quiz", "QuizAttempt", "QuizFeedback",
    "QuizReports", "QuizSettings", "Tag", "Category", "QuizQuestion",
    "QuizSchedule", "QuizTagLink", "QuestionTagLink", "Group", "QuestionTimeTracking"
]
