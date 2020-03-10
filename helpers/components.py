def pagetitle(doc, introtext, topic, author, website):
  with doc.tag('div', klass='heading-container'):
    with doc.tag('h1', klass='content-heading font-thin', id='pagetitle', style='margin-bottom: 5px'):
      with doc.tag('span', klass='icon-ink-pen-streamline colorful-font'):
        doc.text('')
      doc.text(' ' + topic)
    with doc.tag('p', klass='center'):
      with doc.tag('small'):
        doc.text(' Journal Topic of ')
        with doc.tag('a', href=website, title=author):
          doc.text(author)
    intro(doc, text=introtext)

def chapter(doc, id, heading, datum, paragraphs, author, picture=None, appendix=None):
  with doc.tag('section', klass='project chapter', id=id):
    if picture:
      with doc.tag('div', klass='item project-text read-width-optimized no-border'):
        doc.stag('img', src=picture['src'], style='max-height: ' + picture['height'])

    with doc.tag('h2'):
      doc.text(heading)
      doc.stag('br')
      doc.line('small', datum)
      doc.line('small', ' - ' + author)
    with doc.tag('div', klass='item project-text read-width-optimized'):
      for paragraph in paragraphs:
        if paragraph['type'] == 'text':
          doc.line('p', paragraph['content'])

        if paragraph['type'] == 'code':
          with doc.tag('div', klass='fancy-code'):
            codelines = paragraph['content'].split('\n')
            with doc.tag('pre', klass='code'):
              doc.text(paragraph['content'])

      if appendix:
        with doc.tag('div', klass='small-emphasis-container'):
          with doc.tag('h4', klass='no-margin'):
            doc.line('i', 'Appendix')
          with doc.tag('small'):
            with doc.tag('a', href=appendix['href'], target='_blank'):
              with doc.tag('i'):
                doc.text(appendix['description'])

def intro(doc, text):
  with doc.tag('blockquote'):
    doc.text(text)
  
  with doc.tag('a', href='/journal/error.html', id='new-chapter-hint', style='display: none'):
    with doc.tag('blockquote', klass='highlight'):
      doc.text('A new chapter was released since your last visit ! Click this box to jump right in !')

def chapterindex(doc, chapters, ids):
  with doc.tag('blockquote', klass='chapter-index'):

    with doc.tag('div', id='chapter-index-toggle'):
      with doc.tag('h5', klass='no-margin font-regular'):
        with doc.tag('span', klass='icon-book-read-streamline v-align font-big colorful-font'):
          doc.text('')
        doc.line('span', ' Chapter Index')

    with doc.tag('div'):
      with doc.tag('ul', id='chapter-index-list', klass='margin-top-20 margin-bottom-20 colorful-font-soft', style='display: none'):
        for chapter,id in zip(chapters, ids):
          with doc.tag('li'):
            with doc.tag('a', href='#' + id):
              doc.text(chapter['topic'])
