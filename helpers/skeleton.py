from yattag import Doc, indent
import os
import datetime
import helpers.components

inlinecss = open(os.getcwd() + '/stylesheets/inline.css').read()
fontcss = open(os.getcwd() + '/stylesheets/font.css').read()
criticalpathcss = open(os.getcwd() + '/stylesheets/criticalpath.css').read()

js = open(os.getcwd() + '/js/main.js').read()

def htmldocument(data):
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
        text(fontcss)

      with tag('style', media='screen'):
        text(criticalpathcss)

      with tag('style', media='screen'):
        text(inlinecss)

      asis('<!--[if lt IE 9]><script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->')
      
      line('title', data['title'])

    with tag('body', klass=''):
      with tag('div', id='content'):
        helpers.components.pagetitle(doc, introtext=data['introtext'], topic=data['topic'], author=data['author'])

        with doc.tag('section', klass='projects'):
          content(doc, data)

        with doc.tag('div', klass='center'):
          doc.line('small', 'Copyright ' + str(data['year']) +  '-' + str(datetime.datetime.now().year) + ' Robin T. Gruenke')

  stag('link', href='/stylesheets/styles.css?v=3', rel='stylesheet')
  stag('link', href='/fonts/styles.css?v=3', rel='stylesheet')
  line('script','', src='/js/main.js')

  return doc

def content(doc, data):
  for entry in data['entries']:
    helpers.components.entry(doc, heading=entry['topic'], datum=entry['date'], paragraphs=entry['paragraphs'], author=entry['author'], picture=entry.get('picture', None), appendix=entry.get('appendix', None))
