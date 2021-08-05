import glob
import os
from argparse import ArgumentParser
from cProfile import runctx
from html.skeleton import htmldocument
from sys import exit

from yattag import indent

from journalparser import parse


def main(args):
    features = {"feedback": True, "journal-like": True,
                "interactive-example": True, "related-topics": False,
                "missing-chapters-hint": True, "chapter-index": True,
                "subscriptions": True
                }

    documents = []
    append_doc = documents.append
    parser_err = False

    print("---------------------------------------")
    print("----- Compiling journal documents -----")
    print("---------------------------------------")

    for path in files(args):
        relative_path, file_name = os.path.split(path)
        prod_path = relative_path.split("..")[1]
        file_name = file_name.split(".")[0]

        document = None
        with open(path) as f:
            for doc, err in parse(f):
                if err:
                    print(r"    - " + err)

                    if not args.verbose:
                        break

                document = doc

        if not document:
            print_fail(path)
            parser_err = True
            continue

        doc_features = features.copy()
        if document.meta.opt_out:
            for feature in document.meta.opt_out.split(" "):
                doc_features[feature] = False

        append_doc({
            "path": prod_path,
            "filepath": relative_path,
            "filename": file_name,
            "document": document,
            "features": doc_features
        })

    if parser_err:
        exit(1)

    for document in documents:
        filename = document["filename"]
        data = document["document"]
        filepath = document["filepath"]
        features = document["features"]

        htmlfile = os.path.join(filepath, filename + ".html")
        with open(htmlfile, "w") as f:
            html = htmldocument(filename, features, data=data)
            f.write(indent(html.getvalue()))

    print("Done.")


def cli_arguments():
    ap = ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true", default=False,
                    help="Show all errors")
    ap.add_argument("-p", "--performance", action="store_true", default=False,
                    help="Show performance analysis")
    ap.add_argument("-f", "--file", help="Parse this file only")
    return ap.parse_args()


def files(args):
    if args.file:
        return [args.file]
    else:
        return glob.glob("../journal/**/*.journal", recursive=True)


def print_fail(file_name):
    print("Parsing failed: " + file_name)
    print(("---------------------------------------"
           "---------------------------------------"
           "---------------------------------------"))


if __name__ == "__main__":
    args = cli_arguments()
    if args.performance:
        runctx("main(args)", globals(), locals())
    else:
        main(args)
