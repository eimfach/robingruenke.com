from functools import lru_cache
from pydantic import BaseModel, stricturl, validator, ValidationError
from pydantic import constr
from pydantic.main import Extra

from typing import Dict, List, Optional
from re import match


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
        if not word_count(5, v, min_l=3, max_l=16):
            msg = ("ensure this value has exactly 5 words with at least 3"
                   " characters and up to 16 for each word")
            raise ValueError(msg)

        elif duplicates(v.split(" ")):
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


def chunk_document(file):
    chunks = []
    append = chunks.append
    chunk = chunk_until_next_component(file)

    while len(chunk) > 0:
        append(chunk)
        chunk = chunk_until_next_component(file)

    return chunks


def chunk_until_next_component(file):
    chunk = []
    append = chunk.append
    tell = file.tell
    readline = file.readline

    line = readline()
    file_pos = tell()
    first_line = True

    while not end_of_file(line):
        if component_identifier(line) and not first_line or drafting(line):
            file.seek(file_pos)
            break

        if first_line:
            first_line = False

        append(line)
        file_pos = tell()

        line = readline()

    return chunk


def parse_components(chunks: List[List]) -> Article:
    # loop chunks
    #  expect first item to be meta comp
    #  expect second item to be intro comp
    #  decide remaining comp types dynamically
    #  then parse individual comp
    #   remove linebreak on properties and identifier
    #   parse properties
    #   parse text
    return False


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


def tokenize_component_introduction(chunk: List):
    introduction = []
    append = introduction.append

    for line in chunk:
        if not blank(line) and not line is chunk[0]:
            l = line.rstrip()
            append(l)

    return " ".join(introduction)


def tokenize_component_meta(chunk: List):
    err_comp = "Error in /meta properties"
    err_msg_notation = "Expected property notation but found"
    err_msg_space = "Expected space after first colon"
    err_duplicate = "duplicate of field"
    props, tail = tokenize_component_properties(chunk)

    if len(tail) > 0:
        if prop_missing_space(tail[0]):
            return props, err_msg(err_comp, err_msg_space, tail[0])

        else:
            token = tokenize_property(tail[0])
            if token[0] in props:
                return props, err_msg(err_comp, err_duplicate, tail[0])
            else:
                return props, err_msg(err_comp, err_msg_notation, tail[0])
    else:
        return props, None


def tokenize_component_properties(chunk: List):
    properties = {}
    tail = []
    append_tail = tail.append

    for line in chunk:
        l = line.rstrip()
        matches = tokenize_property(l)

        if len(matches) == 2:
            prop = matches[0]
            value = matches[1]

            if prop in properties:
                append_tail(line)
            else:
                properties[prop] = value

        elif blank(line) or line is chunk[0]:
            continue

        else:
            append_tail(line)

    return (properties, tail)
###########################################
################# HELPERS #################
###########################################


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
    return len(l) != len(set(l))


def end_of_file(line):
    return line is ""


def err_msg(component, msg, target):
    return "".join([component, ": ", msg, ": ", "\"", target, "\""])


def in_between(n, m, x):
    return n >= m and n <= x


def prop_missing_space(line):
    l = line.rstrip()
    matches = l.split(":", maxsplit=1)

    if len(matches) == 2 and matches[1][0] != " ":
        return True
    else:
        return False


def tokenize_property(line):
    return line.split(": ")


def valid_year(s: str):
    return bool(match("^([0-9]{4}|[0-9]{4} - [0-9]{4})$", s))


def word_count(c: int, s: str, min_l: int, max_l: int):
    words = s.split(" ")
    if len(words) != c:
        return False

    return any(in_between(len(w), min_l, max_l) for w in words)
