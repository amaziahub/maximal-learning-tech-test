import uuid
from time import time  # Correct the import for time

from tech_test.quiz_service import QuizService


class SessionService:

    def __init__(self):
        self.sessions = {}

    def init_session_for_user(self, user_id):
        session_id = str(uuid.uuid4())

        # Get a question from the QuizService
        quiz_service = QuizService()
        question_id, question = quiz_service.get_question()

        session_data = {
            "user_id": user_id,
            "session_id": session_id,
            "question_id": question_id,
            "question" : question,
            "timestamp": time()  # Correct timestamp usage
        }

        self.sessions[user_id] = session_data

        return session_data
