import uuid
from time import time

from tech_test.quiz_service import QuizService


class SessionService:
    def __init__(self):
        self.current_session = {}
        self.sessions = []
        self.user_scores = {}
        self.session_closed = False

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
        self.session_closed = False

        return self.current_session

    def answer_question(self, session_id, user_id, answer):
        if not self.current_session or self.current_session['session_id'] != session_id:
            raise InvalidSessionError("Session not found or expired")

        question_id = self.current_session["question_id"]
        quiz_service = QuizService()
        score = quiz_service.check_answer(question_id, answer)

        current_top_score, current_top_user = self.user_scores.get(session_id, (0, None))
        if score > current_top_score:
            self.user_scores[user_id] = (score, session_id)

        return score

    def refresh_session(self):
        if self.current_session and not self.session_closed:
            self.close_session()

        self.current_session = None
        return self.init_session()

    def get_score(self, session_id, user_id):
        if self.session_closed:
            top_score, top_user_id = self.user_scores.get(session_id, (None, None))

            if top_user_id is None:
                return "No scores submitted yet."
            elif top_user_id == user_id:
                return f"You won! you scored: {top_score}"
            else:
                return f"You lost! The top scorer is {top_user_id} with a score of {top_score}"
        else:
            return "Session is still ongoing, please wait."

    def close_session(self):
        self.session_closed = True
        return "Session closed and finalized."


class InvalidSessionError(Exception):
    def __init__(self, message="Invalid session ID"):
        self.message = message
        super().__init__(self.message)
