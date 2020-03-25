from yattag import indent
import os
import glob

from helpers.skeleton import htmldocument
from journal import parsejournal, isvaliddocument, verbosetest, getKeywordUsageHistogram

features = {'feedback': True, 'journal-like': True, 'interactive-example': True, 'related-topics': True}

documents = []

print('--------------------------------')
print('Parsing journal documents ...')

for filepath in glob.glob('journal/**/*.journal', recursive=True):
  print('Parsing: ' + filepath)
  path,filename = os.path.split(filepath)
  filename = filename.split('.')[0]

  journalfile = open(filepath)
  journaldocument = parsejournal(filehandle=journalfile)

  errors = isvaliddocument(journaldocument)

  if len(errors) > 0:
    verbosetest(filehandle=open(filepath))
    exit()
  else:
    print('Parsing successful!')


    keywordUsageHistogram = getKeywordUsageHistogram(journaldocument)
    print('Keyword Usage: ', keywordUsageHistogram)
    for keyword,amount in keywordUsageHistogram.items():
      if amount < 2:
        print('[WARNING]: Keyword usage in content of keyword \'' + keyword + '\' is ' + str(amount) + '. Expected at least 2 keyword usages.')

      elif amount > 10:
        print('[WARNING]: Keyword usage in content of keyword \'' + keyword + '\' is high: ' + str(amount))

    documents.append({'path': path, 'filename': filename, 'journaldocument': journaldocument, 'keywordUsageHistogram': keywordUsageHistogram})

print('--------------------------------')
print('--------------------------------')
print('Determine related topics ...')

for index,document in enumerate(documents):
  currentJournalDoc = document['journaldocument']
  currentJournalDoc['relatedTopics'] = []

  otherDocuments = [anotherDocument for otherIndex,anotherDocument in enumerate(documents) if otherIndex != index]

  # match all documents with at least one common keyword
  for otherDocument in otherDocuments:
    for key in otherDocument['keywordUsageHistogram']:
      if key in document['keywordUsageHistogram']:
        currentJournalDoc['relatedTopics'].append({'url': '/' + otherDocument['path'] + '/' + otherDocument['filename'] + '.html', 'keywordUsageHistogram': otherDocument['keywordUsageHistogram'], 'topic': otherDocument['journaldocument']['topic'], 'commonKeywords': [] })
        break

  # sort related topics (common keywords count)
  # keyword count is enforced to be exactly 5 for each document
  oneCommonKeyword = []
  twoCommonKeywords = []
  threeCommonKeywords = []
  fourCommonKeywords = []
  fiveCommonKeywords = []

  for relatedTopic in currentJournalDoc['relatedTopics']:
    commonKeywordCount = 0

    for keyIndex,keyword in enumerate(relatedTopic['keywordUsageHistogram']):

      if keyword in document['keywordUsageHistogram']:
        commonKeywordCount = commonKeywordCount + 1
        relatedTopic['commonKeywords'].append(keyword)

      if keyIndex == 4:
        if commonKeywordCount == 0:
          exit('Error while matching common keywords in related topic, common keyword count is 0 for an already matched topic', 1)
        elif commonKeywordCount == 1:
          oneCommonKeyword.append(relatedTopic)
        elif commonKeywordCount == 2:
          twoCommonKeywords.append(relatedTopic)
        elif commonKeywordCount == 3:
          threeCommonKeywords.append(relatedTopic)
        elif commonKeywordCount == 4:
          fourCommonKeywords.append(relatedTopic)
        elif commonKeywordCount == 5:
          fiveCommonKeywords.append(relatedTopic)

  currentJournalDoc['relatedTopics'] = [*fiveCommonKeywords, *fourCommonKeywords, *threeCommonKeywords, *twoCommonKeywords, *oneCommonKeyword]

  # slice first three
  currentJournalDoc['relatedTopics'] = currentJournalDoc['relatedTopics']

print('--------------------------------')
print('--------------------------------')
print('Compiling journal documents to html ...')

for document in documents:
    filename = document['filename']
    journaldocument = document['journaldocument']
    path = document['path']

    html = htmldocument(filename, features, data=journaldocument)
    htmlfile = os.path.join(path, filename + '.html')
    result = open(htmlfile, 'w')
    result.write(indent(html.getvalue()))
    print('Compiled journal document to Html: ' + htmlfile)