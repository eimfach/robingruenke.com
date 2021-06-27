import datetime
import calendar


def create_better_date(datum):
    betterdate = create_date_from_datum(datum)
    betterdate = calendar.month_abbr[betterdate.month] + \
        ' ' + str(betterdate.day) + ', ' + str(betterdate.year)
    return betterdate.upper()


def create_date_from_datum(datum):
    dateparts = [int(part) for part in datum.split('.')]
    return datetime.date(year=dateparts[2], month=dateparts[1], day=dateparts[0])


def sort_related_topics_by_last_update(relatedTopics):
    return sorted(relatedTopics, key=lambda topic: topic['latestUpdate'], reverse=True)


def get_latest_update_from_journal(journaldocument):
    dates = [create_date_from_datum(chapter['date'])
             for chapter in journaldocument['chapters']]
    return max(dates)
