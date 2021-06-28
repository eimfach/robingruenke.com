from os import close
import pytest
import os
import re
from journal_parser import buffer_until_next_component, blank

dir = os.path.dirname(os.path.abspath(__file__))

###########################################
############## FIXTURES  ##################
###########################################


@pytest.fixture
def journal_file():
    f = open(os.path.join(dir, 'fixtures', "test.journal"))
    yield f
    f.close()


@pytest.fixture
def component_buffer():
    f = open(os.path.join(dir, 'fixtures', "component_buffer.journal"))
    buffer = f.readlines()
    f.close()

    return buffer


@pytest.fixture
def blank_lines_file():
    f = open(os.path.join(dir, 'fixtures', "blank_lines.journal"))
    yield f
    f.close()


@pytest.fixture
def buffer_two_components():
    f = open(os.path.join(dir, 'fixtures', "buffer_two_components.journal"))
    buffer = f.readlines()
    f.close()

    return remove_blank_lines(buffer)


###########################################
################# TESTS ###################
###########################################

def test_buffer_until_next_component(journal_file, component_buffer):
    msg = "Should buffer each item of one component into a list"
    b = buffer_until_next_component(journal_file)
    assert b == component_buffer, msg


def test_buffer_remove_blank_lines(journal_file, blank_lines_file):
    msg = "Should remove any blank lines"
    b1 = buffer_until_next_component(journal_file)
    b2 = buffer_until_next_component(blank_lines_file)
    assert b1 == b2, msg


def test_buffer_two_components(journal_file, buffer_two_components):
    msg = '''
    Should create one buffer per multiple components with the same filehandle
    '''
    b1 = buffer_until_next_component(journal_file)
    b2 = buffer_until_next_component(journal_file)
    b = b1 + b2
    assert b == buffer_two_components, msg


############ journal_parser.blank #############

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


def test_blank_reverse():
    t = blank("  abc\n")
    t2 = blank("abc: def")
    t3 = blank("/abc  \n")

    assert t == False and t2 == False and t3 == False


def remove_blank_lines(buffer):
    new_buffer = []
    for line in buffer:
        if re.match('^\s+', line) is None:
            new_buffer.append(line)

    return new_buffer
