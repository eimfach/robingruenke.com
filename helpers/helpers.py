import datetime
import calendar

def createbetterdate(datum):
  betterdate = createdatefromdatum(datum)
  betterdate = calendar.month_abbr[betterdate.month] + ' ' + str(betterdate.day) + ', ' + str(betterdate.year)
  return betterdate.upper()

def createdatefromdatum(datum):
  dateparts = [int(part) for part in datum.split('.')]
  return datetime.date(year=dateparts[2], month=dateparts[1], day=dateparts[0])

def sortrelatedtopicsbylastupdate(relatedTopics):
    return sorted(relatedTopics, key=lambda topic: topic['latestUpdate'], reverse=True)

def getlatestupdatefromjournal(journaldocument):
    dates = [createdatefromdatum(chapter['date'])
             for chapter in journaldocument['chapters']]
    return max(dates)