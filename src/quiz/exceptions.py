class QuizNotFoundException(Exception):
    """ Exception raised when a quiz is not found"""

class QuizAttemptNotFoundException(Exception):
    """ Exception raised when a quiz attempt is not found"""
class DuplicateQuizAttemptException(Exception):
    """Exception raised when trying to create duplicate quize attempt."""
