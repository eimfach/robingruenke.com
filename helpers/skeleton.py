from yattag import Doc, indent
import os
import datetime
import helpers.components
import re


def htmldocument(filename, features, data):
    responsivecss = open(
        os.getcwd() + '/stylesheets/inline/responsive.css').read()
    fontcss = open(os.getcwd() + '/stylesheets/inline/font.css').read()
    iconfontcss = open(os.getcwd() + '/fonts/styles.css').read()
    criticalpathcss = ''

    try:
        criticalpathcss = open(
            os.getcwd() + '/stylesheets/inline/critical/' + filename + '.css').read()

    except:
        print('[WARNING]: Critical CSS File not found !')

    printcss = open(os.getcwd() + '/stylesheets/print.css').read()

    packedinlinecss = '\n' + fontcss + '\n\n' + iconfontcss + \
        '\n\n' + criticalpathcss + '\n\n' + responsivecss

    packedjspath = assetpipeline('journal.js', 'js/modules/polyfills.js', 'js/modules/startup.js',
                                 'js/modules/subscriptions.js', 'js/modules/chapterindex.js', 'js/modules/articleupdatehint.js',
                                 'js/modules/gallery.js', 'js/modules/feedback.js', 'js/modules/likesubmit.js')

    doc = Doc()
    tag, text, stag, line, asis = doc.tag, doc.text, doc.stag, doc.line, doc.asis

    asis('<!DOCTYPE html>')
    with tag('html', lang='en'):
        with tag('head'):

            stag('meta', charset='utf-8')
            stag('meta', ('http-equiv', 'X-UA-Compatible'), content='chrome=1')
            stag('meta', name='viewport', content='width=device-width')
            stag('meta', name='description', content=data['description'])
            stag('meta', name='keywords', content=data['keywords'])
            stag('meta', name='author', content=data['author'])
            stag('link', rel='icon', type='image/svg+xml', href='/img/favicon.svg')

            with tag('style'):
                asis(packedinlinecss)

            asis(
                '<!--[if lt IE 9]><script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->')

            line('title', data['title'])

        with tag('body'):

            if features['related-topics'] and len(data['relatedTopics']) > 0:
                with tag('div', id='side-pane', klass='journal'):
                    line('h4', 'Related Topics')

                    for relatedTopic in data['relatedTopics']:
                        with tag('div', klass='post-item'):
                            line('a', relatedTopic['topic'],
                                 href=relatedTopic['url'])

            with tag('div', id='content'):
                helpers.components.pagehero(
                    doc, introtext=data['introtext'], topic=data['topic'], author=data['author'], website=data['owner-website'], enable_subscriptions=features['subscriptions'])

                with doc.tag('section', klass='projects'):
                    journalcontent(doc, data, enablefeedback=features['feedback'], enablejournallike=features[
                                   'journal-like'], enableinteractiveexample=features['interactive-example'],
                                   enablemissingchaptershint=features['missing-chapters-hint'], enablechapterindex=features['chapter-index'])

                with doc.tag('div', klass='center  margin-top-40'):
                    with doc.tag('a', href='/', title='robingruenke.com'):
                        with doc.tag('span', klass='icon-home-house-streamline colorful-font font-big'):
                            doc.text('')

                with doc.tag('div', klass='center'):
                    doc.line('small', getcopyright(data))

    stag('link', href='/stylesheets/styles.css', rel='stylesheet')
    stag('link', href='/stylesheets/print.css', rel='stylesheet', media='print')
    line('script', '', src=packedjspath)

    return doc


def journalcontent(doc, data, enablefeedback=False, enablejournallike=False, enableinteractiveexample=False, enablemissingchaptershint=False, enablechapterindex=False):
    # render chapter index
    if enablechapterindex and len(data['chapters']) > 2:
        ids = [getnormalizedtopic(chapter['topic'])
               for chapter in data['chapters']]
        helpers.components.chapterindex(doc, data['chapters'], ids=ids)

    doc.line('div', '', klass='pagebreak')

    for chapter in data['chapters']:
        helpers.components.chapter(doc, enablefeedback=enablefeedback, enableinteractiveexample=(enableinteractiveexample, chapter.get('interactive-example', None)), id=getnormalizedtopic(
            chapter['topic']), heading=chapter['topic'], datum=chapter['date'], paragraphs=chapter['paragraphs'], author=chapter['author'], picture=chapter.get('picture', None), appndx=chapter.get('appendix', None), gallery=chapter.get('gallery', None), quote=chapter.get('quote', None))

    if enablemissingchaptershint and len(data['chapters']) < 3:
        with doc.tag('blockquote', klass='last no-border margin-top-40', id='more-info'):
            doc.text('Note: Wonder where the rest of the article is ? In my Journal articles, I write and publish small chapters. Every now and then I add a new chapter. Just come back later !')

    if enablejournallike:
        helpers.components.like(doc, data['topic'])


def getnormalizedtopic(s):
    return '-'.join(re.findall('\w+', s)).lower()


def getcopyright(data):
    return 'Copyright ' + str(data['year']) + '-' + str(datetime.datetime.now().year) + ' Robin T. Gruenke'


def assetpipeline(distfilename, *assets):
    filetype = distfilename.split('.')[1]

    assetscontent = ''
    for asset in assets:
        assetscontent = assetscontent + \
            open(os.path.join(os.getcwd(), asset)).read() + '\n\n'

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
