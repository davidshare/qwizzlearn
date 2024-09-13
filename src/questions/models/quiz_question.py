from sqlmodel import SQLModel, Field, Relationship


class QuizQuestion(SQLModel, table=True):
    __tablename__ = "quiz_questions"

    quiz_id: int = Field(foreign_key="quizzes.id", primary_key=True)
    question_id: int = Field(foreign_key="questions.id", primary_key=True)

    quiz: "Quiz" = Relationship(back_populates="questions")
    question: "Question" = Relationship(back_populates="quizzes")
