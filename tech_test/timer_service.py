import time


class TimerService:

    def __init__(self, session_service):
        self.session_service = session_service
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.session_service.refresh_session()
            print("Session refreshed!")
            time.sleep(60)

    def stop(self):
        self.running = False
