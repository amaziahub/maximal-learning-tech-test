import difflib
import random


class QuizService:
    QUESTIONS = {
        1: {"question": "What is the capital of France?", "answer": "Paris"},
        2: {"question": "How many continents are there?", "answer": "7"},
        3: {"question": "What is the chemical symbol for gold?", "answer": "Au"},
        4: {"question": "Who wrote Hamlet?", "answer": "Shakespeare"},
        5: {"question": "What is 2 + 2?", "answer": "4"},
    }

    def get_question(self):
        question_id = random.choice(list(self.QUESTIONS.keys()))
        return question_id, self.QUESTIONS[question_id]["question"]

    def check_answer(self, question_id, answer):
        correct_answer = self.QUESTIONS.get(question_id, {}).get("answer")
        correct_answer = str(correct_answer).strip().lower()

        user_answer = str(answer).strip().lower()

        if user_answer == correct_answer:
            return 100  # Perfect match

        similarity = difflib.SequenceMatcher(None, user_answer, correct_answer).ratio()
        if similarity >= 0.8:
            return 80

        return 0
