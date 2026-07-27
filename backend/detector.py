from typing import List, Dict


class Detector:
    LEVEL_INFO = "INFO"
    LEVEL_WARNING = "WARNING"
    LEVEL_ERROR = "ERROR"
    LEVEL_CRITICAL = "CRITICAL"

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self.info = 0
        self.warning = 0
        self.error = 0
        self.critical = 0

        self.incident = False
        self.severity = self.LEVEL_INFO
        self.messages = []

    def detect(self, logs: List[Dict]) -> Dict:

        self.reset()

        for log in logs:
            self._process_log(log)

        return self._build_response()

    def _process_log(self, log: Dict) -> None:

        level = log["level"].upper()
        message = log["message"]

        if level == self.LEVEL_INFO:
            self.info += 1

        elif level == self.LEVEL_WARNING:
            self.warning += 1
            self.messages.append(message)

            if self.severity not in (
                self.LEVEL_ERROR,
                self.LEVEL_CRITICAL,
            ):  
                self.severity = self.LEVEL_WARNING

        elif level == self.LEVEL_ERROR:
            self.error += 1
            self.incident = True
            self.messages.append(message)

            if self.severity != self.LEVEL_CRITICAL:
                self.severity = self.LEVEL_ERROR

        elif level == self.LEVEL_CRITICAL:
            self.critical += 1
            self.incident = True
            self.messages.append(message)
            self.severity = self.LEVEL_CRITICAL

    def _build_response(self) -> Dict:

        return {
            "incident": self.incident,
            "severity": self.severity,
            "counts": {
                self.LEVEL_INFO: self.info,
                self.LEVEL_WARNING: self.warning,
                self.LEVEL_ERROR: self.error,
                self.LEVEL_CRITICAL: self.critical,
            },
            "messages": self.messages,
        }