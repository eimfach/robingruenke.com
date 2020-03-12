from yattag import indent
import os
import glob

from helpers.skeleton import htmldocument
from journal import parsejournal, isvaliddocument, verbosetest, getKeywordUsageHistogram

features = {'feedback': True}

for filepath in glob.glob('journal/**/*.journal', recursive=True):
  print('--------------------------------')
  print('Opening and parsing: ' + filepath)
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

    doc = htmldocument(features, data=journaldocument)
    htmlfile = os.path.join(path, filename + '.html')
    result = open(htmlfile, 'w')
    result.write(indent(doc.getvalue()))
    print('Html written to: ' + htmlfile)