# QuizWise

QuizWise is a function-based quiz system that manages quiz sessions, user answers, and scoring.

----

## Requirements
Create and app that will do the following:
1. every 60 min there will be a question presented to clients
2. user should be able to answer the question - **free text style**
3. in the end of the 60 sec user will get indication if his score is the highest
4. all users see the same question in that 60 sec window


## Installation
Clone the repository:

```
git clone git@github.com:amaziahub/maximal-learning-tech-test.git
cd maximal-learning-tech-test
pip install -r requirements.txt
```

Create venv and install the required dependencies:
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
The main interface for QuizWise is as follows:

```python
from tech_test.session_service import SessionService

class QuizWise:
    session_service = SessionService()

    def init_session(self):
        return self.session_service.init_session()

    def submit_answer(self, session_id, user_id, answer):
        self.session_service.answer_question(session_id, user_id, answer)

    def get_score(self, session_id, user_id):
        return self.session_service.get_score(session_id, user_id)
```

---

### Session Lifecycle

`init_session()`: Initializes a new quiz session. Only one session runs at a time.

`submit_answer(session_id, user_id, answer)`: Submits an answer for the current session.

`get_score(session_id, user_id)`: Retrieves the user's score once the session is closed. client should poll/long poll
to get the status of the score.

---

### Timer Service

The Timer Service automatically refreshes the session every 60 seconds by calling session_service.refresh_session(). 
Before a new session starts, the previous session is closed to determine the top scorer.

---

### Running Tests
```shell
make test
```
