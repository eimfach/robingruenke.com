from collections import namedtuple
from datetime import date
from enum import Enum
from functools import partial, reduce
from re import match
from typing import Dict, List, Tuple
from operator import getitem

from pydantic.error_wrappers import ValidationError
from model import Article, Chapter, Introduction, Meta
from model import type_chapter_with_gallery_url, type_chapter_with_picture_url


class TokenizePropertyValues():
    def __init__(self):
        self.input_map = {
            "appendix": self._tokenize_appendix,
            "picture": self._tokenize_picture,
            "gallery": self._tokenize_gallery,
            "quote": self._tokenize_quote
        }

    def _tokenize_appendix(self, v: str):
        m = match(r"^\[(.*)\] (\S+)$", v)
        if m:
            v = {"description": m[1].strip(), "href": m[2]}
        else:
            err_msg = ("ensure this value has valid syntax: \""
                       "appendix\", like this: \"[description] "
                       "https://www.robingruenke.com\"")

            return None, err_msg

        return v, None

    def _tokenize_picture(self, v: str):
        m = match(r"^(\d+px) (\S+)$", v)
        if m:
            v = {"height": m[1], "src": m[2]}
        else:
            err_msg = ("ensure this value has valid syntax: \""
                       "picture\", like this: \"250px "
                       "/gallery/img.png\"")
            return None, err_msg

        return v, None

    def _tokenize_gallery(self, v: str):
        m = match(r"^(\d+px) (.+)$", v)
        if m:
            v = {"height": m[1], "items": m[2].split(" ")}
        else:
            err_msg = ("ensure this value has valid syntax: "
                       "\"gallery\", like this: \"45px "
                       "/gallery/img_1.png /gallery/img_2.png\"")
            return None, err_msg

        return v, None

    def _tokenize_quote(self, v: str):
        m = match(r"^\[(.*)\] \[(.+)\] (.+)$", v)
        if m:
            v = {
                "author": m[1],
                "content": m[2],
                "reference": m[3]
            }
        else:
            err_msg = ("ensure this value has proper formatting "
                       "\"quote\", like this \"[description] [content] \""
                       "https://wikipedia.com\"")
            return None, err_msg

        return v, None


class TokenizeComponent:

    def __init__(self):
        self.input_map = {
            "/meta": self.tokenize_component_meta,
            "/introduction": self.tokenize_component_introduction,
            "/chapter": self.tokenize_component_chapter
        }

    class Decorators:
        @classmethod
        def tokenize_properties(cls, has_content_body: bool):
            def wrapper(next_step):
                def h(self, chunk: List):
                    err_comp = f"Error in {chunk[0].rstrip()} properties"
                    props, tail = tokenize_component_properties(chunk)
                    msg = partial(err_msg, err_comp)

                    if len(tail) > 0:
                        invalid_msg = cls._invalid_tail(
                            has_content_body, props, tail)

                        if invalid_msg:
                            return None, msg(*invalid_msg)

                    return next_step(self, msg, props, tail)

                return h
            return wrapper

        @classmethod
        def _invalid_tail(cls, has_content_body, props, tail):
            if not props_body_terminated(tail):
                msg = analyze_incorrect_property(tail[0], props)
                return (msg, tail[0])

            elif not has_content_body:
                line = get_first_contentful(tail)
                if not line is "":
                    # TODO: Refactor msg
                    msg = ("Properties were terminated by"
                           " blank line, overflowing content not allowed")

                    return (msg, line)

            return None

        @classmethod
        def tokenize_property_values(cls, tpv: TokenizePropertyValues):
            def wrapper(next_step):
                def h(self, msg, props, tail):
                    psc = props.copy()
                    input_map = tpv.input_map

                    for prop, val in props.items():
                        tokenize = input_map.get(prop)
                        if not tokenize:
                            continue

                        t, err = tokenize(val)
                        if err:
                            return None, msg(err)
                        else:
                            psc[prop] = t

                    return next_step(self, msg, psc, tail)

                return h
            return wrapper

    @Decorators.tokenize_properties(has_content_body=True)
    @Decorators.tokenize_property_values(TokenizePropertyValues())
    def tokenize_component_chapter(self, msg, props, tail):
        paragraphs = []
        append = paragraphs.append
        previously_blank = False
        inside_code_block = False

        for line in tail:

            if blank(line) and not inside_code_block:
                previously_blank = True

            elif match(r"^\|code", line):
                append({"type": "code", "content": ""})
                inside_code_block = True

            elif match(r"^code\|", line):
                inside_code_block = False

            elif inside_code_block:
                paragraphs[-1]["content"] += line

            elif previously_blank:
                append({"type": "text", "content": [line.strip()]})
                previously_blank = False

            else:
                paragraphs[-1]["content"].append(line.strip())

        for p in paragraphs:
            if p["type"] is "text":
                p["content"] = " ".join(p["content"])

        return ({**props, "paragraphs": paragraphs}, None)

    @Decorators.tokenize_properties(has_content_body=True)
    @Decorators.tokenize_property_values(TokenizePropertyValues())
    def tokenize_component_introduction(self, msg, props, tail):
        lines = [line.rstrip() for line in tail if not blank(line)]

        intro = " ".join(lines)
        return ({"content": intro.strip(), **props}, None)

    @Decorators.tokenize_properties(has_content_body=False)
    def tokenize_component_meta(self, msg, props, tail):
        return props, None


class ParseComponent:
    @classmethod
    def parse_component_chapter(cls, tokens: Dict):
        try:
            Model = Chapter
            if "picture" in tokens and is_url(tokens["picture"]["src"]):
                Model = type_chapter_with_picture_url(Model)

            if "gallery" in tokens and is_url(tokens["gallery"]["items"][0]):
                Model = type_chapter_with_gallery_url(Model)

            chapter = Model(**tokens)

        except ValidationError as e:
            err_comp = "Error in /chapter"
            return None, default_err_msg(e, err_comp, tokens)

        return chapter, None

    @classmethod
    def parse_component_introduction(cls, tokens: Dict):
        try:
            intro = Introduction(**tokens)

        except ValidationError as e:
            err_comp = "Error in /introduction"
            return None, default_err_msg(e, err_comp, tokens)

        return intro, None

    @classmethod
    def parse_component_meta(cls, tokens: Dict):
        err_comp = "Error in /meta properties"

        try:
            meta = Meta(**tokens)
            return meta, None

        except ValidationError as e:
            return None, default_err_msg(e, err_comp)


def chunk_until_next_component(file) -> List[str]:

    fi = SeekableFileIterator(file)
    first_line = next(fi, "---")

    if drafting(first_line):
        return []

    chunk = [first_line]
    append = chunk.append

    for line in fi:
        if component_identifier(line) or drafting(line):
            fi.rewind()
            break
        else:
            append(line)

    return chunk


def component_iterator(file):
    return iter(partial(chunk_until_next_component, file), [])


def parse(file, parse_c: ParseComponent = ParseComponent(), tokenize_c: TokenizeComponent = TokenizeComponent()) -> Article:
    # loop read chunk by chunk from file
    # for cmp in component_iterator(file):
    #   expect first item to be meta comp, return err
    #   expect second item to be intro comp, return err

    #   decide other comp types dynamically, return err
    #   then parse each individual comp
    #     tokenize comp, return err
    #     tokens, err = tokenize_c.input_map[cmp[0]]()
    #     parse comp with tokens
    #     parse_c.input_map[cmp[0]](tokens)
    return False


def tokenize_component_properties(chunk: List):
    properties = {}
    tail = []
    append_tail = tail.append
    chunk = chunk[1:]

    for n, line in enumerate(chunk):

        if blank(line):
            tail += chunk[n:]
            break

        lrs = line.rstrip()
        prop, value = tokenize_property(lrs)

        if prop and prop not in properties:
            properties[prop] = value

        else:
            append_tail(line)

    return (properties, tail)


###########################################
################# HELPERS #################
###########################################


class SeekableFileIterator:
    def __init__(self, file):
        self._file_pos = file.tell()
        self._file = file

    def __iter__(self):
        return self

    def __next__(self):
        self._file_pos = self._file.tell()
        line = self._file.readline()

        if self._end_of_file(line):
            raise StopIteration

        return line

    def _end_of_file(self, line):
        return line is ""

    def rewind(self):
        self._file.seek(self._file_pos)


class Message:

    class Limit(Enum):
        MAX_LENGTH = "at most"
        MIN_LENGTH = "at least"

    dict = {
        "MAX_LENGTH": Limit.MAX_LENGTH,
        "MIN_LENGTH": Limit.MIN_LENGTH
    }


def analyze_incorrect_property(line: str, props: List):
    err_msg_notation = "expected property notation but found"
    err_msg_space = "expected space after first colon"
    err_duplicate = "duplicate of field"

    if prop_missing_space(line):
        return err_msg_space

    elif tokenize_property(line)[0] in props:
        return err_duplicate

    else:
        return err_msg_notation


def blank(line):
    return line.isspace()


def component_identifier(line):
    return line[0] is "/"


def component_type_is(name, chunk: List):
    line = chunk[0]
    return line.rstrip() == "/" + name


def default_err_msg(err, cmp, tokens=None):
    error = err.errors()[0]
    msg = error["msg"]
    keys = error["loc"]

    target = "->".join(replace(keys, "_", "-"))

    if tokens and keys[0] in tokens:
        v = get_value_from_nested_dict(tokens, keys)
        vt = truncate(v, 14)
        target = target + f": {vt} (len={len(v)})"

    return err_msg(cmp, msg, target)


def drafting(line):
    return line[:3] == "---"


def err_msg(component, msg, target=None):
    l = [component, ": ", msg]

    if target:
        l += [": ", "\"", target, "\""]

    return "".join(l)


def err_str_boundaries(entity, target, count, limit: Message.Limit):
    return f"ensure {entity} {target} has {limit.value} {count} characters"


def get_first_contentful(tail):
    for l in tail:
        if not blank(l):
            return l

    return ""


def get_value_from_nested_dict(d: Dict, path: Tuple[str]):
    return reduce(getitem, path, d)


def is_url(s):
    return bool(match(r"^[a-z]+://", s))


def prop_missing_space(line: str):
    matches = line.rstrip().split(":", maxsplit=1)

    if len(matches) is 2 and matches[1][0] is not " ":
        return True
    else:
        return False


def props_body_terminated(tail):
    return blank(tail[0])


def replace(sl: List[str], c1, c2):
    l = []
    append = l.append
    for s in sl:
        append(str(s).replace(c1, c2))

    return l


def tokenize_property(line: str):
    m = match(r"^(.+?): (.+?)$", line)
    if m:
        prop, value = m.group(1, 2)
        return (prop.replace("-", "_"), value)
    else:
        return (None, None)


def truncate(s, l):
    return (s[:l] + "...") if len(s) > l else s
