#!/usr/bin/env python


def perc(progress, precision=1):
    """Returns a percentage string, with custom precision

    Args:
        progress (float): Current progress value, between 0.0 and 1.0
        precision (int): Number of visible decimal in percentage. Defaults to 1.

    Returns:
        str: Percentage string, of type " 67.4%"
    """
    up = 10**(precision+2)
    down = 10**precision
    return "{:{}.{}f}%".format(int(progress * up)/down, precision+4, precision)


class ProgressTracker:
    """Allows you to track a progression over an iteration

    Args:
        max_val ([type]): [description]
        current_val (int, optional): [description]. Defaults to 0.
        precision (int, optional): [description]. Defaults to 1.
    """

    def __init__(self, name, max_val=None, precision=1, current_val=0):
        self.max_val = max_val
        self.current_val = current_val
        self.progress = current_val/max_val
        self.precision = precision
        self.name = name

    def update(self, progress=None):
        if progress == None:
            self.progress = self.current_val/self.max_val
        else:
            self.progress = progress

    def incr(self):
        self.current_val += 1
        self.update()

    def set_current(self, current_val):
        self.current_val

    def set_parent(self, parent):
        self.parent = parent

    def __str__(self):
        return "{}~{}".format(self.name, perc(self.progress, self.precision))


class ProgressBar:
    """Manages multiple `ProgressTracker` objects

    Args:
        printer (function): Function to use to print the status. Uses print() if None. Defaults to None.
    """

    def __init__(self, printer=None):
        self.printer = printer
        self.trackers = []

    def print(self):
        msg = ""

        if self.printer == None:
            print(msg)
        else:
            self.printer(msg)

    def add_tracker(self, tracker):
        self.trackers.append(tracker)
        tracker.set_parent(self)


if __name__ == '__main__':
    tracker = ProgressTracker("test", max_val=10)
    while(True):
        tracker.incr()
        print(tracker)
        input()
