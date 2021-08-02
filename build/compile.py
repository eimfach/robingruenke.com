from yattag import indent
import os
import glob
from argparse import ArgumentParser

from html.skeleton import htmldocument
from journal_parser import parse


def main():
    args = parse_cli_arguments()
    features = {'feedback': True, 'journal-like': True,
                'interactive-example': True, 'related-topics': False,
                'missing-chapters-hint': True, 'chapter-index': True,
                'subscriptions': True
                }

    documents = []
    append = documents.append

    print("---------------------------------------")
    print("----- Compiling journal documents -----")
    print("---------------------------------------")

    for file_name in files(args):
        relative_path, filename = os.path.split(file_name)
        prod_path = relative_path.split('..')[1]
        filename = filename.split('.')[0]

        document = None
        with open(file_name) as f:
            for doc, err in parse(f):
                if err:
                    print(r"    - " + err)

                    if not args.verbose:
                        break

                document = doc

        if not document:
            print("Parsing failed: " + file_name)
            print(("---------------------------------------"
                   "---------------------------------------"
                   "---------------------------------------"))
            continue

        doc_features = features.copy()
        if hasattr(document.meta, "opt_out"):
            for feature in document.meta.opt_out.split(" "):
                doc_features[feature] = False

        append({"path": prod_path,
                "filepath": relative_path,
                "filename": filename,
                "document": document,
                "features": doc_features})

    # for document in documents:
    #     filename = document['filename']
    #     document = document['document']
    #     filepath = document['filepath']
    #     features = document['features']

    #     htmlfile = os.path.join(filepath, filename + '.html')
    #     with open(htmlfile, 'w') as f:
    #         html = htmldocument(filename, features, data=document)
    #         f.write(indent(html.getvalue()))


def parse_cli_arguments():
    ap = ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true", default=False,
                    help="Show all errors")
    ap.add_argument("-f", "--file", help="Parse this file only")
    return ap.parse_args()


def files(args):
    if args.file:
        return [args.file]
    else:
        return glob.glob("../journal/**/*.journal", recursive=True)


if __name__ == "__main__":
    main()
