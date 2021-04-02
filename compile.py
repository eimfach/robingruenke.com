from yattag import indent
import os
import glob

from helpers.skeleton import htmldocument
from journal import parse_journal, is_valid_document, verbosetest, get_keyword_usage_histogram
from helpers.helpers import sort_related_topics_by_last_update, get_latest_update_from_journal

features = {'feedback': True, 'journal-like': True,
            'interactive-example': True, 'related-topics': True, 'missing-chapters-hint': True,
            'chapter-index': True, 'subscriptions': True
            }

documents = []

print('--------------------------------')
print('Parsing journal documents ...')

for filepath in glob.glob('journal/**/*.journal', recursive=True):
    print('Parsing: ' + filepath)
    path, filename = os.path.split(filepath)
    filename = filename.split('.')[0]

    journal_file = open(filepath)
    journal_document = parse_journal(filehandle=journal_file)
    journal_file.close()
    document_features = features.copy()
    for optout in journal_document['opt-out']:
        document_features[optout] = False

    errors = is_valid_document(journal_document)

    if len(errors) > 0:
        verbosetest(filehandle=open(filepath))
        exit()
    else:
        print('Parsing successful!')

        keyword_usage_histogram = get_keyword_usage_histogram(journal_document)
        print('Keyword Usage: ', keyword_usage_histogram)
        for keyword, amount in keyword_usage_histogram.items():
            if amount < 2:
                print('[WARNING]: Keyword usage in content of keyword \'' + keyword +
                      '\' is ' + str(amount) + '. Expected at least 2 keyword usages.')

            elif amount > 50:
                print('[WARNING]: Keyword usage in content of keyword \'' +
                      keyword + '\' is high: ' + str(amount))

        documents.append({'path': path, 'filename': filename, 'journaldocument': journal_document,
                          'keywordUsageHistogram': keyword_usage_histogram, 'features': document_features})

print('--------------------------------')
print('--------------------------------')
print('Determine related topics ...')

for index, document in enumerate(documents):
    current_journal_doc = document['journaldocument']
    current_journal_doc['relatedTopics'] = []

    other_documents = [another_document for other_index, another_document in enumerate(
        documents) if other_index != index]

    # match all documents with at least one common keyword
    for other_document in other_documents:
        for key in other_document['keywordUsageHistogram']:
            if key in document['keywordUsageHistogram']:
                latestUpdate = get_latest_update_from_journal(
                    other_document['journaldocument'])
                current_journal_doc['relatedTopics'].append({'url': '/' + other_document['path'] + '/' + other_document['filename'] + '.html',
                                                             'keywordUsageHistogram': other_document['keywordUsageHistogram'], 'topic': other_document['journaldocument']['topic'], 'commonKeywords': [], 'latestUpdate': latestUpdate})
                break

    # keyword count is enforced to be exactly 5 for each document
    # Highest common keyword count goes first
    one_common_keyword = []
    two_common_keywords = []
    three_common_keywords = []
    four_common_keywords = []
    five_common_keywords = []

    for related_topic in current_journal_doc['relatedTopics']:
        common_keyword_count = 0

        for key_index, keyword in enumerate(related_topic['keywordUsageHistogram']):

            if keyword in document['keywordUsageHistogram']:
                common_keyword_count = common_keyword_count + 1
                related_topic['commonKeywords'].append(keyword)

            if key_index == 4:
                if common_keyword_count == 0:
                    exit(
                        'Error while matching common keywords in related topic, common keyword count is 0 for an already matched topic', 1)
                elif common_keyword_count == 1:
                    one_common_keyword.append(related_topic)
                elif common_keyword_count == 2:
                    two_common_keywords.append(related_topic)
                elif common_keyword_count == 3:
                    three_common_keywords.append(related_topic)
                elif common_keyword_count == 4:
                    four_common_keywords.append(related_topic)
                elif common_keyword_count == 5:
                    five_common_keywords.append(related_topic)

    # sort each list by latest update
    one_common_keyword = sort_related_topics_by_last_update(one_common_keyword)
    two_common_keywords = sort_related_topics_by_last_update(
        two_common_keywords)
    three_common_keywords = sort_related_topics_by_last_update(
        three_common_keywords)
    four_common_keywords = sort_related_topics_by_last_update(
        four_common_keywords)
    five_common_keywords = sort_related_topics_by_last_update(
        five_common_keywords)

    current_journal_doc['relatedTopics'] = [*five_common_keywords, *four_common_keywords,
                                            *three_common_keywords, *two_common_keywords, *one_common_keyword]

    # slice first three
    current_journal_doc['relatedTopics'] = current_journal_doc['relatedTopics'][:3]

print('--------------------------------')
print('--------------------------------')
print('Compiling journal documents to html ...')

for document in documents:
    filename = document['filename']
    journal_document = document['journaldocument']
    path = document['path']

    html = htmldocument(filename, document['features'], data=journal_document)
    htmlfile = os.path.join(path, filename + '.html')
    result = open(htmlfile, 'w')
    result.write(indent(html.getvalue()))
    print('[SUCCESS] Compiled journal document to Html: ' + htmlfile)
