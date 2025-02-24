import uuid
from time import time

from tech_test.quiz_service import QuizService


class SessionService:
    def __init__(self):
        self.current_session = {}
        self.sessions = []

    def init_session(self):
        session_id = str(uuid.uuid4())

        quiz_service = QuizService()
        question_id, question = quiz_service.get_question()

        new_session = {
            "session_id": session_id,
            "question_id": question_id,
            "question": question,
            "timestamp": time()
        }

        if self.current_session:
            self.sessions.append(self.current_session)

        self.current_session = new_session

        self.sessions.append(self.current_session)

        return self.current_session

    def refresh_session(self):
        return self.init_session()
