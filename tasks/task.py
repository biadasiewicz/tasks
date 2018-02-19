
DEFAULT_MINUTES = 15
DEFAULT_DESCRIPTION = "<no description>"


class Task:
    def __init__(self, minutes=DEFAULT_MINUTES, description=None):
        self.minutes = minutes
        self.description = description if description else DEFAULT_DESCRIPTION

    def __str__(self):
        return str(self.minutes) + ": " + self.description
