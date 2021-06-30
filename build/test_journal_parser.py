from os import close
import pytest
import os
import re
import json
import cProfile
from journal_parser import blank, component_identifier, end_of_file
from journal_parser import buffer_document, buffer_until_next_component
from journal_parser import drafting, component_type_is, parse_component_properties
from journal_parser import parse_component_meta, parse_component_introduction

# TODO: check msg for each test
# TODO: refactor test names
# TODO: refactor fixture names
# TODO: extract from fixtures

dir = os.path.dirname(os.path.abspath(__file__))

##################################################
############ TESTS OF EXTRACTED UNITS ############
##################################################


def test_blank():
    t = blank(" ")
    assert t == True


def test_blank_2():
    t2 = blank("    ")
    assert t2 == True


def test_blank_3():
    t3 = blank("\n")
    assert t3 == True


def test_blank_4():
    t4 = blank("     \n")
    assert t4 == True


def test_blank_inverse():
    t = blank("  abc\n")
    t2 = blank("abc: def")
    t3 = blank("/abc  \n")

    assert t == False and t2 == False and t3 == False


def test_component_identifier():
    msg = "should return true if the first char is /"
    t = component_identifier("/meta")
    t1 = component_identifier("abc")
    assert t == True and t1 == False


def test_end_of_file():
    msg = "should return true for empty string"
    t = end_of_file("")
    t2 = end_of_file("abc")
    assert t == True and t2 == False


def test_drafting():
    t = drafting("--")
    t1 = drafting("---")
    t2 = drafting("----")
    t3 = drafting(" ---")

    assert t == False and t1 == True and t2 == True and t3 == False


###########################################
############## FIXTURES  ##################
###########################################


@pytest.fixture
def blank_lines_file():
    f = open(os.path.join(dir, 'fixtures', "blank_lines.journal"))
    yield f
    f.close()


@pytest.fixture
def blank_lines_file_as_list():
    return readlines("blank_lines.journal")


@pytest.fixture
def buffer_two_components():
    return readlines("buffer_two_components.journal")


@pytest.fixture
def component_buffer():
    return readlines("component_buffer.journal")


@pytest.fixture
def drafting_expected():
    return readlines("drafting_expected.journal")


@pytest.fixture
def drafting_file():
    f = open(os.path.join(dir, 'fixtures', "drafting.journal"))
    yield f
    f.close()


@pytest.fixture
def empty_file():
    f = open(os.path.join(dir, 'fixtures', "empty.journal"))
    yield f
    f.close()


@pytest.fixture
def empty_whitespace_file():
    f = open(os.path.join(dir, 'fixtures', "empty_whitespace.journal"))
    yield f
    f.close()


@pytest.fixture
def introduction():
    return read_json("introduction.json")


@pytest.fixture
def introduction_parsed():
    return read_json("introduction_parsed.json")


@pytest.fixture
def journal_file():
    f = open(os.path.join(dir, 'fixtures', "test.journal"))
    yield f
    f.close()


@pytest.fixture
def journal_file_expected():
    return read_json("test_journal.json")


@pytest.fixture
def journal_file_meta_missing():
    return read_json("test_journal_meta_missing.json")


@pytest.fixture
def journal_file_meta_invalid():
    return read_json("test_journal_meta_invalid.json")


@pytest.fixture
def meta_properties():
    return read_json("meta_properties.json")


@pytest.fixture
def meta_properties_parsed():
    return read_json("meta_properties_parsed.json")

###########################################
################# TESTS ###################
###########################################

###### parse_journal.buffer_until_next_component ######


def test_buffer_until_next_component(journal_file, component_buffer):
    msg = "Should buffer each item of one component into a list"
    b = buffer_until_next_component(journal_file)
    assert b == component_buffer, msg


def test_buffer_not_remove_blank_lines(blank_lines_file_as_list, blank_lines_file):
    msg = "Should not remove any blank lines"
    b = buffer_until_next_component(blank_lines_file)
    assert b == blank_lines_file_as_list, msg


def test_buffer_two_components(journal_file, buffer_two_components):
    msg = '''
    Should create one buffer per multiple components with the same filehandle
    '''
    b1 = buffer_until_next_component(journal_file)
    b2 = buffer_until_next_component(journal_file)
    b = b1 + b2
    assert b == buffer_two_components, msg


def test_buffer_return_empty_for_empty_file(empty_file):
    msg = "should return empty buffer for empty file"
    b = buffer_until_next_component(empty_file)
    assert b == [], msg


def test_buffer_stop_when_drafting_occurs(drafting_file, drafting_expected):
    msg = "should not parse beyond a line with three dashes"
    b = buffer_until_next_component(drafting_file)
    assert b == drafting_expected, msg


def test_buffer_complete_document(journal_file, journal_file_expected):
    msg = "should create buffer for each component in document"
    buffers = buffer_document(journal_file)

    assert buffers == journal_file_expected, msg


def test_component_type(journal_file_expected):
    is_meta = component_type_is("meta", journal_file_expected[0])
    assert is_meta == True


def test_component_type_missing(journal_file_meta_missing):
    is_meta = component_type_is("meta", journal_file_meta_missing[0])
    assert is_meta == False


def test_component_type_invalid(journal_file_meta_invalid):
    is_meta = component_type_is("meta", journal_file_meta_invalid[0])
    assert is_meta == False


def test_parse_component_properties(meta_properties, meta_properties_parsed):
    props, tail = parse_component_properties(meta_properties)
    assert props == meta_properties_parsed and tail == ["no property"]


def test_parse_component_meta(journal_file_expected, meta_properties_parsed):
    props, err = parse_component_meta(journal_file_expected[0])
    assert props == meta_properties_parsed


def test_parse_component_meta_w_tail(meta_properties, meta_properties_parsed):
    err_msg = "Error Parsing Meta Properties: Expected property notation but found: \"no property\""
    props, err = parse_component_meta(meta_properties)
    assert err_msg == err


def test_parse_component_introduction(introduction, introduction_parsed):
    intro = parse_component_introduction(introduction)
    assert intro == introduction_parsed

###########################################
############## HELPERS ####################
###########################################


def read_json(file_name):
    f = open(os.path.join(dir, 'fixtures', file_name))
    j = json.load(f)
    f.close()
    return j


def readlines(file_name):
    f = open(os.path.join(dir, 'fixtures', file_name))
    buffer = f.readlines()
    f.close()
    return buffer


def remove_blank_lines(buffer):
    new_buffer = []
    for line in buffer:
        if line.isspace():
            new_buffer.append(line)

    return new_buffer


def time_test_buffer_complete_document():
    f = open(os.path.join(dir, 'fixtures', "test.journal"))
    buffers = buffer_document(f)


if __name__ == "__main__":
    cProfile.run("time_test_buffer_complete_document()")
