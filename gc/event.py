import datetime


class Event:
    def __init__(self, id_, created, start, end, updated, summary):
        super().__init__()
        self.id_ = id_
        self.created = created
        self.start = start
        self.end = end
        self.updated = updated
        self.name = summary

    @property
    # ? have a timezone hidden trouble
    def span(self) -> int:
        start = self.start[:-6]
        end = self.end[:-6]
        diff = datetime.datetime.strptime(
            end, "%Y-%m-%dT%H:%M:%S"
        ) - datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        return diff.total_seconds() / 3600


if __name__ == "__main__":
    e = Event(1, "1", "2", 3, 4, 5)
    print(e.__dict__)
    print(Event.__dict__)
