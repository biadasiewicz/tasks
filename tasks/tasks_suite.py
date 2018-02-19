from datetime import datetime


class TasksSuite:
    def __init__(self, start=None):
        self._start = start if start else datetime.now()
        self._tasks = []

    def __eq__(self, x):
        return self._tasks == x._tasks and self._start == x._start

    def __str__(self):
        s = self._start.strftime("%H:%M")
        for t in self._tasks:
            s += str(t) + '\n'
        return s

    @property
    def start(self):
        return self._start

    def append(self, task):
        self._tasks.append(task)

    def extend(self, tasks):
        self._tasks.extend(tasks)

    def pop(self, index):
        self._tasks.pop(index)
