class TimeSimulator:

    def __init__(self, start_time):
        self.timestamp = start_time
        self.date = start_time.date()
        self.first = True

    # maybe skip day if time tick is not in data
    def time_tick(self, interval):
        self.timestamp += interval
        if self.timestamp.date() != self.date:
            self.first = True
            self.date = self.timestamp.date()
        else:
            self.first = False
