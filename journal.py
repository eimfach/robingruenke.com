import re

def parsingError(err):
  print("[ERROR] " + err)
  exit(2)

def parsejournal(filehandle):
  result = {}
  introtext = ""
  parsingintrotext = False
  chapterbuffers = []
  parsingallowed = True

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
      result['owner-website'] = getAuthorsWebsite(linenumber, line)

    elif linenumber == 3:
      result['year']= getyear(line)
      continue

    elif linenumber == 4:
      result['title'] = gettitle(line)
      continue

    elif linenumber == 5:
      result['description'] = getdescription(line)
      continue

    elif linenumber == 6:
      result['keywords'] = getkeywords(line)
      continue

    elif linenumber == 7:
      result['topic'] = gettopic(linenumber, line)
      continue

    elif linenumber == 8:
      if expectnewline(linenumber, line):
        continue

    elif linenumber == 9:
      if re.search('^/introduction$', line) is None:
        parsingError('Line 8: The next paragraph has to start with \'/introduction\', an introduction to the topic is the bare minium of a journal document')
      else:
        continue

    elif linenumber == 10:
      if expectnewline(linenumber, line):
        continue

    elif linenumber == 11 or parsingintrotext:
      parsingintrotext = True

      if isnewline(line):
        parsingintrotext = False
        result['introtext'] = introtext

        introtextnospaces = result['introtext'].split(' ')
        introtextnospaces = ''.join(introtextnospaces)
        introtextlength = len(introtextnospaces)
        if introtextlength > 300:
          parsingError('Intro Text should not be longer than 300 characters !')

        if introtextlength < 50:
          parsingError('Intro Text should not be smaller than 50 characters')

      else:
        introtext = introtext + trimline(line)

      continue

    else:

      # if a draft separator occurres, dismiss all further buffering and the stop parsing.
      if re.search('^---+', line):
        break

      elif re.search('^/chapter$', line) is not None:
        chapterbuffers.append([])
        continue

      elif len(chapterbuffers) > 0:
        
        chapterbuffers[-1].append((linenumber, line))

      else:
        continue
  
  result['chapters'] = []

  # parse each chapter content
  for chapterbuffer in chapterbuffers:
    chapter = parsechapter(chapterbuffer)
    result['chapters'].append(chapter)

  return result

def getKeywordUsageHistogram(result):
  keywords = result['keywords'].split(' ')
  keywordUsageHistogram = dict.fromkeys(keywords, 0)

  # check keyword usages in content
  for keyword in keywords:
    keywordsInPageTopic = len(re.findall(keyword, result['topic']))
    keywordsInIntroText = len(re.findall(keyword, result['introtext']))
    keywordUsageHistogram[keyword] = keywordUsageHistogram[keyword] + keywordsInPageTopic + keywordsInIntroText

    for chapter in result['chapters']:
      paragraphsContent = [paragraph['content'] for paragraph in chapter['paragraphs'] if paragraph['type'] == 'text']
      joinedContents = chapter['topic'] + ' ' + ' '.join(paragraphsContent)
      keywordsInTopicAndContent = len(re.findall(keyword, joinedContents, re.IGNORECASE))
      keywordUsageHistogram[keyword] = keywordUsageHistogram[keyword] + keywordsInTopicAndContent

  return keywordUsageHistogram

def trimline(line):
  return line.replace('\n', ' ')

# chapter -> {'topic': String, 'author': String, 'date': String, picture: String, 'paragraphs': List <{'type': String, 'content': String}>}
def parsechapter(chapterbuffer):

  chapter = {}
  chapterblocks = []
  hasPicture = False
  hasAppendix = False
  hasGallery = False
  hasQuote = False
  hasInteractiveExample = False
  attributesParsingDone = False
  contenttype = None
  optionalAttributesBuffer = []

  for index, (linenumber, line) in enumerate(chapterbuffer):

    if index == 0:
      chapter['topic'] = gettopic(linenumber, line)

    elif index == 1:
      chapter['author'] = getauthor(linenumber, line)

    elif index == 2:
      chapter['date'] = getDate(linenumber, line)
      
    elif index > 2 and re.search('^\n$', line) is None and not attributesParsingDone:
      optionalAttributesBuffer.append((linenumber, line))

    else:
      # parse the buffered optional attributes if not done yet
      if len(optionalAttributesBuffer) > 0 and not attributesParsingDone:
        for linen,attribute in optionalAttributesBuffer:
          params = [chapter, attribute, linen]
          picture, appendix, gallery, quote, example = getChapterPicture(*params), getChapterAppendix(*params), getChapterGallery(*params), getChapterQuote(*params), getChapterInteractiveExample(*params)

          if (picture and hasPicture):
            parsingError('Line ' + str(linen + 1) + ': Duplicate picture attribute.')

          elif (appendix and hasAppendix):
            parsingError('Line ' + str(linen + 1) + ': Duplicate appendix attribute.')

          elif (gallery and hasGallery):
            parsingError('Line ' + str(linen + 1) + ': Duplicate gallery attribute.')

          elif (quote and hasQuote):
            parsingError('Line ' + str(linen + 1) + ': Duplicate quote attribute.')

          elif (example and hasInteractiveExample):
            parsingError('Line ' + str(linen + 1) + ': Duplicate interactive-example attribute.')

          if picture:
            hasPicture = True

          elif appendix:
            hasAppendix = True

          elif gallery:
            hasGallery = True

          elif quote:
            hasQuote = True

          elif example:
            hasInteractiveExample = True

        if (hasGallery and not hasPicture):
          parsingError('Line: ' + str(linenumber) + ': Found gallery attribute, but couldn\'t find picture attribute. A gallery attribute also requires you to set a picture attribute.')
      
      attributesParsingDone = True

      # buffer the chapter content stuff line by line, it can be as long as you want.
      if re.search('^\n$', line) is None:

        if len(chapterblocks) == 0:
          chapterblocks.append({'type': None, 'content': trimline(line)})

        else:
            isCodeOpening = re.search('^code:$', line)
            isCodeClosing = re.search('^:code$', line)

            if chapterblocks[-1]['type'] is None:

              if isCodeOpening: 
                chapterblocks[-1]['type'] = 'code'
              else:
                chapterblocks[-1]['type'] = 'text'

            if (chapterblocks[-1]['type'] == 'code' and isCodeClosing):
              chapterblocks.append({'type': None, 'content': ''})

            else:
              if isCodeOpening:
                continue
              else:
                if chapterblocks[-1]['type'] == 'text':
                  line = trimline(line)

                chapterblocks[-1]['content'] = chapterblocks[-1]['content'] + line

      # if the current line is a line break
      else:
        # codeblock: keep adding the lines even if a linebreaks occurres
        if len(chapterblocks) > 0 and chapterblocks[-1]['type'] == 'code':
          chapterblocks[-1]['content'] = chapterblocks[-1]['content'] + line
        else:
          # create new empty paragraph
          chapterblocks.append({'type': None, 'content': ''})

  chapter['paragraphs'] = chapterblocks

  # convert all dashes in text blocks to '•  '
  for txt in chapter['paragraphs']:
    if txt['type'] == 'text':
      txt['content'] = txt['content'].replace('- ', '•  ')

  return chapter

def getChapterInteractiveExample(chapter, line, linenumber):
  hasInteractiveExampleAttributeStart = re.search('^interactive-example$', line)
  hasValidInteractiveExampleAttrStart = re.search('^interactive-example:', line)

  if hasInteractiveExampleAttributeStart:
    parsingError('Line ' + str(linenumber + 1) + ' found interactive-example attribute but colon and value are missing !')

  elif hasValidInteractiveExampleAttrStart:
    interactiveExample = re.findall('^interactive-example: (\S*)$', line)
    if len(interactiveExample) < 1:
      parsingError('Line ' + str(linenumber + 1) + ' found interactive-example attribute, but the given value is invalid')
    else:
      chapter['interactive-example'] = interactiveExample[0]

def getChapterGallery(chapter, line, linenumber):
  hasGalleryAttributeStart  = re.search('^gallery$', line)
  hasValidGalleryAttrStart = re.search('^gallery:', line)

  if hasGalleryAttributeStart:
    parsingError('Line ' + str(linenumber + 1) + ' found gallery attribute but colon and values are missing !')
  
  elif hasValidGalleryAttrStart:
    #look up css compatible image height
    height = re.findall('^gallery: (\d{,4}px|%|em|rem)', line)

    if len(height) < 1:
      parsingError('Line ' + str(linenumber + 1) + ': Found gallery attribute but found no height value or it is invalid. A valid height value must be a valid css height value like: 250px 50% 2em 1rem, where the digits are max. 4 characters.')

    else:
      gallery = {'height': height[0], 'pictures': []}

      pictures = re.findall(' \((\S+?.jpg|\S+?.jpeg|\S+?.png)\)', line)

      if len(pictures) < 1:
        parsingError('Line ' + str(linenumber + 1) + ' missing or invalid picture values. Please add pictures space separated, with it\'s paths like so: (pic1.png) (pic2.png) | Supported files are .jpg .jpeg .png')
      
      elif len(pictures) < 3:
        parsingError('Line ' + str(linenumber + 1) + ' you should specify at least three pictures.')

      elif len(pictures) % 3 != 0:
        parsingError('Line ' + str(linenumber + 1) + ' you should specify an amount of pictures which is dividable by 3 with rest 0.')

      else:
        for picture in pictures:
          gallery['pictures'].append(picture)

        chapter['gallery'] = gallery

        return True

  return False

def getChapterQuote(chapter, line, linenumber):
  hasQuoteStart  = re.search('^quote$', line)
  quote = re.findall('^quote: (\[.+\] \[.+\] \[.+\])', line)
  onlyQuote = re.search('^quote: (\[.+\] \[.+\] \[.+\])$', line)
    
  if hasQuoteStart:
    parsingError('Line ' + str(linenumber + 1) + ' found quote attribute but colon and value are missing !')

  if len(quote) > 0:

    if not onlyQuote:
      parsingError('Line ' + str(linenumber + 1) + ': Found quote attribute and values but also found leaping characters. Quote has to look like \'quote: [description] [quote] [hyperlink]\'')

    else:
      parts = re.findall('\[(.+?)\]', line)
      description = parts[0]
      content = parts[1]
      href = parts[2]

      chapter['quote'] = {'description': description, 'content': content, 'href': href}
      return True

  return False

def getChapterPicture(chapter, line, linnumber):
  #TODO replace any character for picture src with any non-whitespace character
  picture = re.findall('^picture: (\d+px .+)$', line)

  if len(picture) > 0:
    pictureAttr = picture[0].split(' ')
    chapter['picture'] = {'src': pictureAttr[1], 'height': pictureAttr[0]}
    return True

  return False

def getChapterAppendix(chapter, line, linenumber):
  appendix = re.findall('^appendix: (\[.*\] [^ ]+)', line)
  onlyAppendix = re.search('^appendix: (\[.*\] [^ ]+)$', line)
    
  if len(appendix) > 0:
    if not onlyAppendix:
      parsingError('Line ' + str(linenumber + 1) + ': Found appendix attribute but also found leaping characters. Appendix has to look like \'appendix: [Hyperlink description] url_no_whitespaces\'')
    
    else:
      href = re.findall('^\[.+\] (.+)', appendix[0])[0]
      description = re.findall('^\[(.+)\]', appendix[0])[0]
      chapter['appendix'] = {'href': href, 'description': description}
      return True

  return False

def getAuthorsWebsite(linenumber, s):
  website = re.findall('^website: (.+)$', s)

  if len(website) > 0:
    return website[0]
  else:
    parsingError('Line ' + str(linenumber + 1) + ': This line must be the authors website matching \'website: url\'')  

def getDate(linenumber, s):
  date = re.findall('^date: (\d{2}\.\d{2}\.\d{4})$', s)

  if len(date) > 0:
    return date[0]
  else:
    parsingError('Line ' + str(linenumber + 1) + ': This line must be a date matching \'date: 07.03.2020\'')  

def gettopic(linenumber, s):
  topic = re.findall('^topic: ([A-Za-z 0-9\.,\/\\\|\?\!\&\-\+\=\_\#\*\:\;\(\)]+)$', s)

  if len(topic) > 0:
    if len(topic[0]) > 50:
      parsingError('Line ' + str(linenumber + 1) + ': Chapter topic is longer than 50 characters')
    else:
      return topic[0]
  else:
    parsingError('Line ' + str(linenumber + 1) + ': Expecting Chapter topic like \'topic: Another Topic\'. Possible characters can be: A-Z a-z . , [space] [numbers] | \ / + = - & ! ? _ # * : ; ( )')

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
  title = re.findall('^title: (\w+ - \w+ \w+ \w+ \| .+)$', s)
  if len(title) > 0:
    return title[0]
  else:
    parsingError('Line 4: The fourth line must be the title matching \'title: PrimaryKeyword - Word Word Word | BrandNameAnyCharacters\'')

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
    print('[ERROR] Your journal document is not valid. Missing data includes:')
    for err in errors:
      print('\n' + err)

    print('\nHave Look at this valid document:')
    print(validjournal)

  else:
    print('\n Great ! Your journal document is valid !')

validjournal = '''
/meta
author: Robin Gruenke
website: https://www.robingruenke.com
year: 2020
title: Journal - Blog Html Tools | robingruenke.com
description: Generate static html flexible, approachable, consistent and with a custom format
keywords: journal generate html python elm
topic: How my Journal is build

/introduction

I was looking for a simple and clean solution to generate static html without a server,
since I wanted to start this journal and reuse my html.

'''