from yattag import Doc, indent
import os
import datetime
import helpers.components
import re

def htmldocument(features, data):
  responsivecss = open(os.getcwd() + '/stylesheets/responsive.css').read()
  fontcss = open(os.getcwd() + '/stylesheets/font.css').read()
  criticalpathcss = open(os.getcwd() + '/stylesheets/criticalpath.css').read()

  packedcss = '\n' + fontcss + '\n\n' + criticalpathcss + '\n\n' + responsivecss

  packedjspath = assetpipeline('journal.js', 'js/modules/polyfills.js', 'js/modules/startup.js', 'js/modules/chapterindex.js', 'js/modules/articleupdatehint.js', 'js/modules/gallery.js', 'js/modules/feedback.js', 'js/modules/likesubmit.js')

  doc = Doc()
  tag, text, stag, line, asis = doc.tag, doc.text, doc.stag, doc.line, doc.asis

  asis('<!DOCTYPE html>')
  with tag('html', lang = 'en'):
    with tag('head'):

      stag('meta', charset='utf-8')
      stag('meta', ('http-equiv', 'X-UA-Compatible'), content='chrome=1')
      stag('meta', name='viewport', content='width=device-width')
      stag('meta', name='description', content=data['description'])
      stag('meta', name='keywords', content=data['keywords'])
      stag('meta', name='author', content=data['author'])

      with tag('style', media='screen'):
        asis(packedcss)

      asis('<!--[if lt IE 9]><script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->')
      
      line('title', data['title'])

    with tag('body'):
      with tag('div', id='content'):
        helpers.components.pagetitle(doc, introtext=data['introtext'], topic=data['topic'], author=data['author'], website=data['owner-website'])

        with doc.tag('section', klass='projects'):
          journalcontent(doc, data, enablefeedback=features['feedback'], enablejournallike=features['journal-like'])

        with doc.tag('div', klass='center  margin-top-40'):
          with doc.tag('a', href='/', title='robingruenke.com'):
            with doc.tag('span', klass='icon-home-house-streamline colorful-font font-big'):
              doc.text('')

        with doc.tag('div', klass='center'):
          doc.line('small', 'Copyright ' + str(data['year']) +  '-' + str(datetime.datetime.now().year) + ' Robin T. Gruenke')

  stag('link', href='/stylesheets/styles.css?v=3', rel='stylesheet')
  stag('link', href='/fonts/styles.css?v=3', rel='stylesheet')
  line('script','', src=packedjspath)

  return doc

def journalcontent(doc, data, enablefeedback=False, enablejournallike=False):
  # render chapter index
  if len(data['chapters']) > 2:
    ids = [getnormalizedtopic(chapter['topic']) for chapter in data['chapters']]
    helpers.components.chapterindex(doc, data['chapters'], ids=ids)

  for chapter in data['chapters']:
    helpers.components.chapter(doc, enablefeedback=enablefeedback, id=getnormalizedtopic(chapter['topic']), heading=chapter['topic'], datum=chapter['date'], paragraphs=chapter['paragraphs'], author=chapter['author'], picture=chapter.get('picture', None), appndx=chapter.get('appendix', None), gallery=chapter.get('gallery', None))

  if enablejournallike:
    helpers.components.like(doc, data['topic'])

def getnormalizedtopic(s):
  return ''.join(re.findall('[a-zA-Z]', s)).lower()

def assetpipeline(distfilename, *assets):
  filetype = distfilename.split('.')[1]

  assetscontent = ''
  for asset in assets:
    assetscontent = assetscontent + open(os.path.join(os.getcwd(), asset)).read() + '\n\n'

  if filetype == 'js':
    distfilepath = os.path.join('js', 'dist', distfilename)
    distpathhandle = open(os.path.join(os.getcwd(), distfilepath), 'w')
    skeletonjs = open(os.path.join(os.getcwd(), 'js', 'skeleton.js'))

    distributioncontent = '// auto generated, don\'t modify \n\n'
    for line in skeletonjs:
      if re.search('^//{modules}', line):
        distributioncontent = distributioncontent + assetscontent + '\n\n'
      else:
        distributioncontent = distributioncontent + line

    distpathhandle.write(distributioncontent)
    distpathhandle.close()

    return '/' + distfilepath

  else:
    raise TypeError('assetPipeline: Unsupported filetype: ' + filetype)

  
  

