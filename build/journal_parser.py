import re


def buffer_until_next_component(file):
    buffer = []

    line = file.readline()
    buffer.append(line)
    file_pos = file.tell()
    reading = True

    while reading:
        line = file.readline()

        if end_of_file(line):
            break

        blank_line = blank(line)

        if not blank_line and component_identifier(line):
            reading = False
            file.seek(file_pos)
        else:
            if not blank_line:
                buffer.append(line)

            file_pos = file.tell()

    # for i, line in enumerate(file):

    #     if line[0] == "/" and i > 0:
    #         break
    #     elif line != "\n":
    #         buffer.append(line)

    return buffer


def end_of_file(line):
    return line == ""


def blank(line):
    whitespaces = bool(re.match('^\s+$', line))
    return whitespaces


def component_identifier(line):
    return line[0] == "/"
