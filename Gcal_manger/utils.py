import pandas as pd
import datetime
from event import Event
from connect import connect
from pprint import pprint
from operator import itemgetter
import matplotlib.pyplot as plt


def get_df(service, maxResults):
    df = pd.DataFrame(
        columns=["id", "name", "start", "end", "updated", "span"], index=["id"]
    )
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print(f"Getting the upcoming {maxResults} events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=maxResults,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get(
            "dateTime", (event["start"].get("date", " ") + "T01:00:00+01:00")
        )
        end = event["end"].get(
            "dateTime", (event["end"].get("date", " ") + "T01:00:00+01:00")
        )
        created = event.get(
            "created", event["start"].get("date", " ") + "T01:00:00+01:00"
        )
        updated = event.get("updated", " ")
        id_ = event.get("id")
        name = event.get("summary", " ")
        e = Event(id_, created, start, end, updated, name)
        df = df.append(
            {
                "id": e.id_,
                "start": e.start,
                "end": e.end,
                "created": e.created,
                "name": e.name,
                "span": e.span,
            },
            ignore_index=True,
        )
    return df


def report(df, attr):
    report = dict()
    df_group = df.groupby(df[attr])
    for key, value in df_group:
        report[key] = sum(value["span"])
    report = {
        k: v for k, v in sorted(report.items(), key=lambda item: item[1], reverse=True)
    }
    return report


def get_pie(report, topn=5):
    labels = list(report.keys())[:topn]
    x = list(report.values())[:topn]
    plt.pie(
        x, labels=labels, autopct="%.0f%%", textprops={"fontsize": 15, "color": "k"}
    )
    plt.axis("equal")
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    plt.savefig(f"../images/pie_{now}_topn_{topn}.png")
    plt.show()


if __name__ == "__main__":
    service = connect()
    df = get_df(service, 40)
    print(df)
    report = report(df, "name")
    print(report)
    get_pie(report, 6)
