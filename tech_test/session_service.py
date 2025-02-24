import uuid
from time import time

from tech_test.quiz_service import QuizService


class SessionService:
    def __init__(self):
        self.current_session = {}
        self.sessions = []
        self.user_scores = {}

    def init_session(self):

        if self.current_session:
            return self.current_session

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

    def answer_question(self, session_id, user_id, answer):
        if not self.current_session or self.current_session['session_id'] != session_id:
            raise InvalidSessionError("Session not found or expired")

        question_id = self.current_session["question_id"]
        quiz_service = QuizService()
        score = quiz_service.check_answer(question_id, answer)

        if user_id not in self.user_scores or score > self.user_scores[user_id]:
            self.user_scores[user_id] = score

        return score

    def refresh_session(self):
        if self.current_session:
            self.sessions.append(self.current_session)
        self.current_session = None
        return self.init_session()

    def keep_alive(self, session_id, user_id):
        pass


class InvalidSessionError(Exception):
    def __init__(self, message="Invalid session ID"):
        self.message = message
        super().__init__(self.message)
