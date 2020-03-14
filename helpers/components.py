import numpy

def pagetitle(doc, introtext, topic, author, website):
  with doc.tag('div', klass='heading-container'):
    with doc.tag('h1', klass='content-heading', id='pagetitle', style='margin-bottom: 5px'):
      with doc.tag('span', klass='icon-ink-pen-streamline colorful-font'):
        doc.text('')
      doc.text(' ' + topic)

    with doc.tag('p', klass='center'):
      with doc.tag('small'):
        doc.text(' Journal Topic of ')
        with doc.tag('a', href=website, title=author):
          doc.text(author)

    intro(doc, text=introtext)

def chapter(doc, id, heading, datum, paragraphs, author, picture=None, appndx=None, gallery=None, enablefeedback=False):
  with doc.tag('section', klass='project chapter', id=id):

    if picture:
      containerClasses = 'item project-text read-width-optimized'

      if gallery:
        containerClasses = containerClasses + ' gallery-background no-padding' 
      else:
        containerClasses = containerClasses + ' no-border' 

      with doc.tag('div', klass=containerClasses):
        doc.stag('img', klass='main-image', src=picture['src'], style='display: block; max-height: ' + picture['height'])

        if gallery:
          segmentedPictures = numpy.array(gallery['pictures']).reshape(-1, 3)
          
          for gallerysegment in segmentedPictures:
            with doc.tag('div', klass='gallery-container'):
              for gallerypicture in gallerysegment:
                doc.stag('img', klass='gallery-picture', src=gallerypicture, style='max-height: ' + gallery['height'])

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

      with doc.tag('div', klass='chapter-footer'):
          if appndx:
            appendix(doc, appndx)

          if enablefeedback:
            feedbackbutton(doc, idparent=id, topic=heading)

      if enablefeedback:
        feedbackform(doc, idparent=id, topic=heading)
      
  doc.line('div', '', klass='pagebreak')


def appendix(doc, appendix):
  with doc.tag('div', klass='small-emphasis-container text-shorten'):
    with doc.tag('h4', klass='no-margin'):
      doc.line('i', 'Appendix:')
    with doc.tag('small'):
      doc.line('span', '', klass='icon-link-streamline v-align font-regular')
      with doc.tag('a', href=appendix['href'], target='_blank'):
        with doc.tag('i'):
          doc.text(appendix['description'])

def feedbackbutton(doc, idparent, topic):
  with doc.tag('div', id='feedback-container-' + idparent, klass='feedback-container', style='position: relative'):
    with doc.tag('div', klass='right text-shorten'):
      with doc.tag('span', id='feedback-toggle-' + idparent, klass='leave-feedback'):
        with doc.tag('span'):
          doc.line('i', 'Send Feedback  ', klass='font-thin')
        with doc.tag('span', klass='icon-bubble-comment-streamline-talk colorful-font font-regular'):
          doc.text('')

def feedbackform(doc, idparent, topic):
  with doc.tag('div', id='feedback-form-container-' + idparent, klass='fancy-feedback margin-top-20', style='display: none'):
    with doc.tag('form', ('data-netlify', 'true'), klass='feedback-form', name='feedback', method='POST'):
      doc.stag('input', type='hidden', name='topic', value=topic)
      doc.line('h5', 'Feedback scope:', klass='no-margin')
      doc.line('h5', topic[:36] + '...', klass='no-margin')
      doc.line('hr', '', klass='margin-top-10 margin-bottom-10')
      doc.line('textarea', '', klass='no-border', name='content', placeholder='Click here to write your feedback')
      doc.line('button', 'Submit', klass='call-to-action no-border font-regular margin-top-20', type='submit', style='display: block; width: 100%; cursor: pointer;')
      with doc.tag('div', klass='center'):
        with doc.tag('small', klass='max-char-hint'):
          with doc.tag('span', klass='max-1000-characters'):
            doc.text('0')
          doc.text(' of max. 1500 characters')

def chapterindex(doc, chapters, ids):
  with doc.tag('blockquote', klass='chapter-index'):

    with doc.tag('div', id='chapter-index-toggle'):
      with doc.tag('h5', klass='no-margin font-regular'):
        with doc.tag('span', klass='icon-book-read-streamline v-align font-regular colorful-font'):
          doc.text('')
        doc.line('span', ' Chapter Index')

    with doc.tag('div'):
      with doc.tag('ul', id='chapter-index-list', klass='margin-top-20 margin-bottom-20 colorful-font-soft', style='display: none'):
        for chapter,id in zip(chapters, ids):
          with doc.tag('li'):
            with doc.tag('a', href='#' + id):
              doc.text(chapter['topic'])

def like(doc, topic):
  with doc.tag('div', klass='center auto read-width-optimized margin-bottom-20', id='feature-like-journal'):
    with doc.tag('form', ('data-netlify', 'true'), name='Like +1 ' + topic, method='POST', klass='like-form', id='like-form'):
      doc.stag('input', type='hidden', name='content', value='Received +1')
      with doc.tag('p'):
        doc.line('i', 'Please click the heart icon if you enjoyed this article ! ')
        doc.line('span', '', klass='icon-bubble-love-streamline-talk font-big submit')

def intro(doc, text):
  with doc.tag('blockquote', klass='last'):
    doc.text(text)
  
  with doc.tag('a', href='/journal/error.html', id='new-chapter-hint', style='display: none'):
    with doc.tag('blockquote', klass='highlight'):
      doc.text('A new chapter was released since your last visit ! Click this box to jump right in !')        