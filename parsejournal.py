import re

def parsingError(err):
  print(err)
  exit()

def parsejournal(filehandle):
  result = {}
  introtext = ""
  parsingintrotext = False
  entrybuffers = []

  for linenumber,line in enumerate(filehandle):
    if linenumber == 0:
      if re.search('^/meta$', line) is None:
        parsingError('Line 1: The first line of a Journal Document has to begin with /meta')
      else:
        continue
    
    elif linenumber == 1:
      result['author'] = getauthor(linenumber, line)
      continue

    elif linenumber == 2:
      result['year']= getyear(line)
      continue

    elif linenumber == 3:
      result['title'] = gettitle(line)
      continue

    elif linenumber == 4:
      result['description'] = getdescription(line)
      continue

    elif linenumber == 5:
      result['keywords'] = getkeywords(line)
      continue

    elif linenumber == 6:
      result['topic'] = gettopic(linenumber, line)
      continue

    elif linenumber == 7:
      if expectnewline(linenumber, line):
        continue

    elif linenumber == 8:
      if re.search('^/introduction$', line) is None:
        parsingError('Line 8: The next paragraph has to start with \'/introduction\', an introduction to the topic is the bare minium of a journal document')
      else:
        continue

    elif linenumber == 9:
      if expectnewline(linenumber, line):
        continue

    elif linenumber == 10 or parsingintrotext:
      parsingintrotext = True

      if isnewline(line):
        parsingintrotext = False
        result['introtext'] = introtext

        introtextlength = len(result['introtext'])
        if introtextlength > 300:
          parsingError('Intro Text should not be longer than 300 characters !')

        if introtextlength < 50:
          parsingError('Intro Text should not be smaller than 50 characters')

      else:
        introtext = introtext + line

      continue

    else:
      if re.search('^/entry$', line) is not None:
        entrybuffers.append([])
        continue

      elif len(entrybuffers) > 0:
        
        entrybuffers[-1].append((linenumber, line))

      else:
        continue
  
  result['entries'] = []
  keywords = result['keywords'].split(' ')
  matchingkeywords = 0
  matchingkeywordnames = []

  #TODO: Keyword lookup not working properly
  #TODO: Also lookup headings/topics
  #TODO: Create function for keyword lookups
  #TODO: Create keyword usage histogram

  # parse the entry contents
  for entrybuffer in entrybuffers:
    entry = parseentry(entrybuffer)

    # check occurrence of keywords in entries content
    for paragraph in entry:
      words = paragraph.split(' ')
      for keyword in keywords:
        if keyword in words:
          matchingkeywords = matchingkeywords + 1
          matchingkeywordnames.append(keyword)

    result['entries'].append(entry)

  # check occurrence of keywords in introtext content
  introwords = result['introtext'].split()
  for keyword in keywords:
    if keyword in introwords:
      matchingkeywords = matchingkeywords + 1
      matchingkeywordnames.append(keyword)

  if matchingkeywords < len(keywords):
    print('\t[WARNING]: Not enough Keywords in your content ! There are ' + str(matchingkeywords) + ' of at least ' + str(len(keywords)) + ' Keywords.')
    print('\tFound following keywords in content: ' + ', '.join(matchingkeywordnames))
    print('\tKeywords are: ' + result['keywords'])

  return result

def parseentry(entrybuffer):

  entry = {}
  entrytext = []
  haspicture = False
  contenttype = None

  for index, (linenumber, line) in enumerate(entrybuffer):

    if index == 0:
      entry['topic'] = gettopic(linenumber, line)

    elif index == 1:
      entry['author'] = getauthor(linenumber, line)

    elif index == 2:
      entry['date'] = getDate(linenumber, line)
      
    elif index == 3:
      picture = re.findall('^picture: (.+ \d+px)$', line)

      if len(picture) > 0:
        entry['picture'] = picture[0]
        haspicture = True
      else:
        expectnewline(linenumber, line)

    elif index == 4 and haspicture:
      expectnewline(linenumber, line)

    # read the entry content stuff line by line, it can be as long as you want.
    else:

     # if the current line is not a line break
      if re.search('^\n$', line) is None:

        if len(entrytext) == 0:
          entrytext.append({'type': None, 'content': line})

        else:
            isCodeOpening = re.search('^code:$', line)
            isCodeClosing = re.search('^:code$', line)

            if entrytext[-1]['type'] is None:

              if isCodeOpening: 
                entrytext[-1]['type'] = 'code'
              else:
                entrytext[-1]['type'] = 'text'

            if (entrytext[-1]['type'] == 'code' and isCodeClosing):
              entrytext.append({'type': None, 'content': ''})

            else:
              if isCodeOpening:
                continue
              else:
                entrytext[-1]['content'] = entrytext[-1]['content'] + line

      # if the current line is a line break
      else:
        # codeblock: keep adding the lines even if a linebreaks occurres
        if len(entrytext) > 0 and entrytext[-1]['type'] == 'code':
          entrytext[-1]['content'] = entrytext[-1]['content'] + line
        else:
          # create new empty paragraph
          entrytext.append({'type': None, 'content': ''})

  entry['paragraphs'] = entrytext

  return entry

def getDate(linenumber, s):
  date = re.findall('^date: (\d{2}\.\d{2}\.\d{4})$', s)

  if len(date) > 0:
    return date[0]
  else:
    parsingError('Line ' + str(linenumber + 1) + ': This line must be a date matching \'date: 07.03.2020\'')  

def gettopic(linenumber, s):
  topic = re.findall('^topic: ([A-Za-z 0-9\.,\/\\\|\?\!\&\-\+\=\_\#\*\:\;]+)$', s)

  if len(topic) > 0:
    if len(topic[0]) > 32:
      parsingError('Line ' + str(linenumber + 1) + ': Entry topic is longer than 32 characters')
    else:
      return topic[0]
  else:
    parsingError('Line ' + str(linenumber + 1) + ': Expecting entry topic like \'topic: Another Topic\'. Possible characters can be: A-Z a-z . , [space] [numbers] | \ / + = - & ! ? _ # * : ;')

def getauthor(linenumber, s):
  author = re.findall('^author: (\w+ \w+)$', s)

  if len(author) > 0:
    return author[0]
  else:
    parsingError('Line ' + str(linenumber + 1) + ': This line must be the author matching \'author: Firstname Lastname\'')

def getyear(s):
  year = re.findall('^year: (\d{4})$', s)
  if len(year) > 0:
    return year[0]
  else:
    parsingError('Line 3: The third line must be the year matching \'year: 2020\' with exact length of 4 characters')

def gettitle(s):
  title = re.findall('^title: (\w+ - \w+ \| .+)$', s)
  if len(title) > 0:
    return title[0]
  else:
    parsingError('Line 4: The fourth line must be the title matching \'title: PrimaryKeyword - SecondaryKeyword | BrandNameAnyCharacters\'')

def getdescription(s):
  description = re.findall('^description: ([a-zA-z, \.0-9]{50,160})$', s)

  if len(description) > 0:
    lengthOfDescription = len(description[0])
    if lengthOfDescription < 50:
      parsingError('Line 5: The description must have at least 50 Characters')
    elif lengthOfDescription > 160:
      parsingError('Line 5: The description must have at maximum 160 Characters')
    else:
      return description[0]
  else:
    parsingError('Line 5: The fifth line must be the description matching \'description: Characters allowed: a-z | A-Z | , | [space] [.]\' of length between 50-160 according to optimal SEO')

def getkeywords(s):
  keywords = re.findall('^keywords: (\w{,16} \w{,16} \w{,16} \w{,16} \w{,16})$', s)
  if len(keywords) > 0:
    return keywords[0]
  else:
    parsingError('Line 6: The sixth line must be the keywords having exactly 5 keywords with maximum length of 16 and only latin characters \'keyword: ABC DEF Ghi def jkL\'')

def expectnewline(linenumber, s):
  if not isnewline(s):
    parsingError('Line ' + str(linenumber+1) + ': New Line expected')
  else:
    return True

def isnewline(s):
  if re.search('^\n$', s) is None:
    return False
  else:
    return True

def isvaliddocument(document):
  errors = []

  if 'author' not in document or len(document['author']) == 0:
    errors.append('- Missing meta data \'author\'')

  if 'year' not in document or len(document['year']) == 0:
    errors.append('- Missing meta data \'year\'')

  if 'title' not in document or len(document['title']) == 0:
    errors.append('- Missing meta data \'title\'')

  if 'description' not in document or len(document['description']) == 0:
    errors.append('- Missing meta data \'description\'')
    
  if 'keywords' not in document or len(document['keywords']) == 0:
    errors.append('- Missing meta data \'keywords\'')

  if 'introtext' not in document or len(document['introtext']) == 0:
    errors.append('- Missing introduction text. Note: Plain texts must be surrounded by newlines !')

  return errors

def verbosetest(filehandle):
  errors = isvaliddocument(parsejournal(filehandle))
  
  if len(errors) > 0:
    print('Your journal document is not valid. Missing data includes:')
    for err in errors:
      print('\n' + err)

    print('\nHave Look at this valid document:')
    print(validjournal)

  else:
    print('\n Great ! Your journal document is valid !')

validjournal = '''
/meta
author: Robin Gruenke
year: 2020
title: Journal - Test1 | JournalTestSuite
description: This file is used to test the journal Parser The length of this description has to between 50 and 160 according to SEO best practice
keywords: ABC abc abc abc abc

/introduction

I was looking for a simple and clean solution to generate static html without a server,
since I wanted to start this journal and reuse my html.

'''