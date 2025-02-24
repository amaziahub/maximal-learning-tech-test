from tech_test.session_service import SessionService


class QuizWise:
    session_service = SessionService()

    def init_session(self):
        return self.session_service.init_session()

    def submit_answer(self, session_id, user_id, answer):
        self.session_service.answer_question(session_id, user_id, answer)

    def keep_alive(self, session_id, user_id):
        return self.session_service.keep_alive(session_id, user_id)
