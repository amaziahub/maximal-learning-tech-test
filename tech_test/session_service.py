import uuid
from time import time
from tech_test.quiz_service import QuizService


class SessionService:

    def __init__(self):
        self.sessions = {}

    def init_session_for_user(self, user_id):
        session_id = str(uuid.uuid4())

        quiz_service = QuizService()
        question_id, question = quiz_service.get_question()

        session_data = {
            "user_id": user_id,
            "session_id": session_id,
            "question_id": question_id,
            "question": question,
            "timestamp": time()
        }

        self.sessions[user_id] = session_data

        return session_data

    def get_question_by_session_id(self, session_id):
        session_data = self.sessions.get(session_id)
        return session_data if session_data["question_id"] else None

