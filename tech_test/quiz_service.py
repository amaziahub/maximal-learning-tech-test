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

    def ask_score(self, id, text):
        return ""