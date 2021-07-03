from pydantic import BaseModel, stricturl
from re import findall
from typing import List, Optional


class MetaComponent(BaseModel):
    pass


class Author(BaseModel):
    name: str
    sur_name: Optional[str]
    website: Optional[stricturl(allowed_schemes=["https"])]


class Paragraph(BaseModel):
    type: str
    content: str


class Chapter(BaseModel):
    author: Author
    topic: str
    date: str
    paragraphs: List[Paragraph]


class Article(BaseModel):
    author: Author
    year: int
    last_entry_year: Optional[int]
    html_title: str
    description: str
    keywords: str
    topic: str
    introtext: str
    chapters: List[Chapter]


def parse_components(buffers):
    # loop buffers
    #  expect first item to be meta comp
    #  expect second item to be intro comp
    #  decide remaining comp types dynamically
    #  then parse individual comp
    #   remove linebreak on properties and identifier
    #   parse properties
    #   parse text
    return False


def tokenize_component_introduction(buffer):
    introduction = []
    append = introduction.append

    for line in buffer:
        if not blank(line) and not line is buffer[0]:
            l = line.rstrip()
            append(l)

    return " ".join(introduction)


def tokenize_component_meta(buffer):
    err_comp = "Error in Meta Properties: "
    err_msg_notation = "Expected property notation but found: "
    err_msg_space = "Expected space after first colon: "
    props, tail = tokenize_component_properties(buffer)

    if len(tail) > 0:
        if prop_missing_space(tail[0]):
            return props, err_msg(err_comp, err_msg_space, tail[0])
        else:
            return props, err_msg(err_comp, err_msg_notation, tail[0])
    else:
        return props, None


def tokenize_component_properties(buffer):
    properties = {}
    tail = []
    append_tail = tail.append

    for line in buffer:
        l = line.rstrip()
        matches = l.split(": ")

        if len(matches) == 2:
            prop = matches[0]
            value = matches[1]
            properties[prop] = value

        elif blank(line) or line is buffer[0]:
            continue

        else:
            append_tail(line)

    return (properties, tail)


def buffer_document(file):
    buffers = []
    append = buffers.append
    buffer = buffer_until_next_component(file)

    while len(buffer) > 0:
        append(buffer)
        buffer = buffer_until_next_component(file)

    return buffers


def buffer_until_next_component(file):
    buffer = []
    append = buffer.append
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

    return buffer


def blank(line):
    return line.isspace()


def component_identifier(line):
    return line[0] is "/"


def component_type_is(name, buffer):
    line = buffer[0]
    return line.rstrip() == "/" + name


def drafting(line):
    return line[:3] == "---"


def end_of_file(line):
    return line is ""


def err_msg(component, msg, target):
    return "".join([component, msg, "\"", target, "\""])


def prop_missing_space(line):
    l = line.rstrip()
    matches = l.split(":", maxsplit=1)

    if len(matches) == 2 and matches[1][0] != " ":
        return True
    else:
        return False
