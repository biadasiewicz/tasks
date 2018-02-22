from datetime import datetime, timedelta


class TasksSuite:
    def __init__(self, start=None):
        self._start = start if start else datetime.now()
        self._tasks = []

    def __eq__(self, x):
        return self._tasks == x._tasks and self._start == x._start

    def __str__(self):
        s = self._start.strftime("%H:%M: start")
        minutes = 0
        for t in self._tasks:
            minutes += t.minutes
            end_time = self.start + timedelta(minutes=minutes)
            s += '\n' + end_time.strftime("%H:%M: ") + t.description
        return s

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    def append(self, task):
        self._tasks.append(task)

    def extend(self, tasks):
        self._tasks.extend(tasks)

    def pop(self, index):
        self._tasks.pop(index)

    def shift(self, minutes):
        self._start = self._start + timedelta(minutes=minutes)
