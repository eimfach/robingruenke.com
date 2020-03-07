from yattag import indent
import os
import glob

from helpers.skeleton import htmldocument
from parsejournal import parsejournal, isvaliddocument, verbosetest

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
    doc = htmldocument(data=journaldocument)
    htmlfile = os.path.join(path, filename + '.html')
    result = open(htmlfile, 'w')
    result.write(indent(doc.getvalue()))
    print('Html written to: ' + htmlfile)