def pagetitle(doc, introtext, topic, author):
  with doc.tag('div', klass='heading-container'):
    with doc.tag('h1', klass='content-heading font-thin'):
      with doc.tag('span', klass='icon-ink-pen-streamline colorful-font'):
        doc.text('')
      doc.text(' ' + topic)
      doc.stag('br')
      doc.line('small', 'Journal Topic of ' + author)
    intro(doc, text=introtext)

def entry(doc, heading, datum, paragraphs, author, picture=None):

  with doc.tag('section', klass='project'):
    if picture:
      picturedata = picture.split(' ')
      src = picturedata[0]
      height = picturedata[1]

      with doc.tag('div', klass='item project-text read-width-optimized no-border'):
        doc.stag('img', src=picturedata[0], style='max-height: ' + height)
        
    with doc.tag('h3'):
      doc.text(heading)
      doc.stag('br')
      doc.line('small', datum)
      doc.line('small', ' - ' + author)
    with doc.tag('div', klass='item project-text read-width-optimized'):
      for paragraph in paragraphs:
        if paragraph['type'] == 'text':
          doc.line('p', paragraph['content'])

        if paragraph['type'] == 'code':
          codelines = paragraph['content'].split('\n')
          with doc.tag('pre'):
            doc.text(paragraph['content'])


def intro(doc, text):
  with doc.tag('blockquote', klass='last'):
    doc.text(text)