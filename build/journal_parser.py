from enum import Enum, auto
from functools import lru_cache
from re import findall, match
from typing import Dict, List, Optional

from pydantic import BaseModel, ValidationError, constr, stricturl, validator
from pydantic.main import Extra


class Paragraph(BaseModel):
    _type: str
    content: str


class Chapter(BaseModel):
    author: str
    topic: str
    date: str
    paragraphs: List[Paragraph]


class Meta(BaseModel):
    author: constr(min_length=2, max_length=48)
    website: stricturl(allowed_schemes=["https"])
    year: constr(min_length=4)
    title: constr(min_length=24, max_length=60)
    description: constr(min_length=50, max_length=160)
    keywords: str
    optout: Optional[str]

    class Config:
        validate_assignment = True
        allow_mutation = False
        extra = Extra.forbid

    @validator("keywords")
    def keywords_must_be_five_words(cls, v):
        if not valid_keywords(word_count=5, kws=v):
            msg = ("ensure this value has exactly 5 words with at least 3"
                   " characters and up to 16 for each word")
            raise ValueError(msg)

        return v

    @validator("keywords")
    def keywords_must_not_have_duplicates(cls, v):
        if duplicates(v.split(" ")):
            msg = "ensure this value has no duplicates in it"
            raise ValueError(msg)

        return v

    @validator("year")
    def year_must_be_valid_format(cls, v):
        if not valid_year(v):
            msg = ("ensure this value has these formats of integers \"2020 - 2021\""
                   " or \"2020\"")
            raise ValueError(msg)

        return v


class Article(BaseModel):
    meta: Meta
    introtext: str
    chapters: List[Chapter]


class Link(BaseModel):
    text: constr(min_length=3, max_length=16)
    url: stricturl(allowed_schemes=["https"])


class Introduction(BaseModel):
    content: constr(min_length=50, max_length=600)
    link: Optional[Link]


class Message():

    class Limit(Enum):
        MAX_LENGTH = "at most"
        MIN_LENGTH = "at least"

    dict = {
        "MAX_LENGTH": Limit.MAX_LENGTH,
        "MIN_LENGTH": Limit.MIN_LENGTH
    }


def chunk_until_next_component(file):

    fi = FileIterator(file)
    chunk = []
    append = chunk.append
    comp_identified = False

    for line in fi:
        is_comp_line = component_identifier(line)
        is_drafting_line = drafting(line)

        if is_comp_line and comp_identified or is_drafting_line:
            fi.rewind()
            break

        else:
            append(line)

        if is_comp_line:
            comp_identified = True

    return chunk


def parse(file) -> Article:
    # loop read chunk by chunk from file
    #   expect first item to be meta comp, return err
    #   expect second item to be intro comp, return err

    #   decide other comp types dynamically, return err
    #   then parse each individual comp
    #     tokenize comp, return err TODO: tokenize interfaces are different
    #     parse comp with tokens
    return False


def parse_component_introduction(tokens: List):

    try:
        params = {"content": tokens[0]}

        if tokens[1]:
            params["link"] = Link(**tokens[1])

        intro = Introduction(**params)

    except ValidationError as e:
        err_comp = "Error in /introduction"
        error = e.errors()[0]
        model = e.model.__name__.lower()
        target = error["loc"][0]
        err_type = error["type"].split(".")[-1].upper()
        limit = error.get("ctx", {}).get("limit_value")

        if err_type in Message.dict:
            msg = err_str_boundaries(
                model, target, limit, Message.dict[err_type])

        else:
            msg = error["msg"]

        return None, err_msg(err_comp, msg)

    return intro, None


def parse_component_meta(tokens: Dict):
    err_comp = "Error in /meta properties"

    try:
        meta = Meta(**tokens)
        return meta, None

    except ValidationError as e:
        errors = e.errors()
        msg = errors[0]["msg"]
        target = errors[0]["loc"][0]
        return None, err_msg(err_comp, msg, target)


def tokenize_component_chapter():
    pass


def tokenize_component_introduction(chunk: List):
    lines = [line.rstrip() for line in chunk[1:] if not blank(line)]

    intro = " ".join(lines)
    tokens = match(r"^(.+?)\[(.+?)\]\((.+?)\)$", intro)

    if not tokens:
        return [intro.strip(), None]

    else:
        link = {"text": tokens[2].strip(), "url": tokens[3].strip()}
        return [tokens[1].strip(), link]


def tokenize_component_meta(chunk: List):
    err_comp = "Error in /meta properties"
    props, tail = tokenize_component_properties(chunk)

    if len(tail) > 0:
        msg = analyze_incorrect_property(tail[0], props)
        return props, err_msg(err_comp, msg, tail[0])
    else:
        return props, None


def tokenize_component_properties(chunk: List):
    properties = {}
    tail = []
    append_tail = tail.append

    for line in chunk[1:]:
        lrs = line.rstrip()
        prop, value = tokenize_property(lrs)

        if prop and prop not in properties:
            properties[prop] = value

        elif blank(line):
            continue

        else:
            append_tail(line)

    return (properties, tail)


###########################################
################# HELPERS #################
###########################################


class FileIterator():
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


def drafting(line):
    return line[:3] == "---"


def duplicates(l: List):
    return len(l) is not len(set(l))


def err_msg(component, msg, target=None):
    l = [component, ": ", msg]

    if target:
        l += [": ", "\"", target, "\""]

    return "".join(l)


def err_str_boundaries(entity, target, count, limit: Message.Limit):
    return f"ensure {entity} {target} has {limit.value} {count} characters"


def in_between(n, mi, mx):
    return n >= mi and n <= mx


def prop_missing_space(line: str):
    matches = line.rstrip().split(":", maxsplit=1)

    if len(matches) is 2 and matches[1][0] is not " ":
        return True
    else:
        return False


def tokenize_property(line: str):
    m = match(r"^(.+?): (.+?)$", line)
    if m:
        return m.group(1, 2)
    else:
        return (None, None)


def valid_year(y: str):
    return bool(match(r"^([0-9]{4}|[0-9]{4} - [0-9]{4})$", y))


def valid_keywords(word_count: int, kws: str) -> bool:
    ws = words(kws)
    if len(ws) is not word_count:
        return False

    return all(words_in_between_length(min_l=3, max_l=16, ws=ws))


def words(ws: str):
    return ws.split(" ")


def words_in_between_length(min_l: int, max_l: int, ws: List[str]):
    return (in_between(len(w), min_l, max_l) for w in ws)
