from pydantic import BaseModel
from re import findall


class MetaComponent(BaseModel):
    pass


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


def parse_component_introduction(buffer):
    introduction = []
    append = introduction.append

    for line in buffer:
        if not blank(line) and not line is buffer[0]:
            l = line.rstrip()
            append(l)

    return " ".join(introduction)


def parse_component_meta(buffer):
    err_msg = "Error Parsing Meta Properties: Expected property notation but found: "
    props, tail = parse_component_properties(buffer)

    if len(tail) > 0:
        return props, "".join([err_msg, "\"", tail[0], "\""])
    else:
        return props, []


def parse_component_properties(buffer):
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
