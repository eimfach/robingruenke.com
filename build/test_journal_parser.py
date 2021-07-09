import cProfile
import json
from functools import lru_cache
import os
import pytest
import random
from journal_parser import blank, component_identifier, end_of_file, parse_component_introduction
from journal_parser import chunk_document, chunk_until_next_component
from journal_parser import drafting, component_type_is, tokenize_component_properties
from journal_parser import tokenize_component_meta, tokenize_component_introduction
from journal_parser import prop_missing_space, parse_component_meta

# TODO: check msg for each test
# TODO: refactor test names
# TODO: refactor fixture names
# TODO: extract from fixtures
# TODO: Order imports

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


def test_prop_missing_space():
    missing = prop_missing_space("prop:value\n")
    assert missing == True


def test_prop_has_space():
    missing = prop_missing_space("prop: value\n")
    assert missing == False


def test_prop_missing_space_but_colon_value():
    missing = prop_missing_space("prop:value:abc\n")
    assert missing == True


def test_prop_has_space_but_colon_in_value():
    missing = prop_missing_space("prop: value:abc\n")
    assert missing == False

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
def introduction_tokenized():
    return read_json("introduction_tokenized.json")


@pytest.fixture
def introduction_tokenized_w_link():
    return read_json("introduction_tokenized_w_link.json")


@pytest.fixture
def introduction_w_link():
    return read_json("introduction_w_link.json")


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
def meta_properties_tokenized():
    return read_json("meta_properties_tokenized.json")


@pytest.fixture
def meta_properties_prop_no_space():
    return read_json("meta_properties_prop_no_space.json")


@pytest.fixture
def meta_properties_w_duplicate():
    return read_json("meta_properties_w_duplicate.json")

###########################################
################# TESTS ###################
###########################################


def test_chunk_until_next_component(journal_file, component_buffer):
    msg = "Should chunk each line of one component into a list"
    b = chunk_until_next_component(journal_file)
    assert b == component_buffer, msg


def test_chunk_not_remove_blank_lines(blank_lines_file_as_list, blank_lines_file):
    msg = "Should not remove any blank lines"
    c = chunk_until_next_component(blank_lines_file)
    assert c == blank_lines_file_as_list, msg


def test_chunk_two_components(journal_file, buffer_two_components):
    msg = '''
    Should create one chunk per multiple components with the same filehandle
    '''
    c1 = chunk_until_next_component(journal_file)
    c2 = chunk_until_next_component(journal_file)
    c = c1 + c2
    assert c == buffer_two_components, msg


def test_chunk_return_empty_for_empty_file(empty_file):
    msg = "should return empty chunk for empty file"
    c = chunk_until_next_component(empty_file)
    assert c == [], msg


def test_chunk_stop_when_drafting_occurs(drafting_file, drafting_expected):
    msg = "should not parse beyond a line with three dashes"
    c = chunk_until_next_component(drafting_file)
    assert c == drafting_expected, msg


def test_chunk_complete_document(journal_file, journal_file_expected):
    msg = "should create chunk for each component in document"
    chunks = chunk_document(journal_file)

    assert chunks == journal_file_expected, msg


def test_component_type(journal_file_expected):
    is_meta = component_type_is("meta", journal_file_expected[0])
    assert is_meta == True


def test_component_type_missing(journal_file_meta_missing):
    is_meta = component_type_is("meta", journal_file_meta_missing[0])
    assert is_meta == False


def test_component_type_invalid(journal_file_meta_invalid):
    is_meta = component_type_is("meta", journal_file_meta_invalid[0])
    assert is_meta == False


def test_tokenize_component_properties(meta_properties, meta_properties_tokenized):
    props, tail = tokenize_component_properties(meta_properties)
    assert props == meta_properties_tokenized and tail == ["no property"]


def test_tokenize_component_duplicate_property():
    chunk = ["/meta", "author: Robin Gruenke\n", "author: Robin T. Gruenke\n"]
    expected = ["author: Robin T. Gruenke\n"]
    props, tail = tokenize_component_properties(chunk)
    assert tail == expected


def test_tokenize_component_meta(journal_file_expected, meta_properties_tokenized):
    props, err = tokenize_component_meta(journal_file_expected[0])
    assert props == meta_properties_tokenized and err is None


def test_tokenize_component_meta_w_tail(meta_properties):
    err_msg = "Error in /meta properties: Expected property notation but found: \"no property\""
    props, err = tokenize_component_meta(meta_properties)
    assert err_msg == err


def test_tokenize_component_meta_missing_space(meta_properties_prop_no_space):
    err_msg = "Error in /meta properties: Expected space after first colon: \"prop:value:withcolon\n\""
    props, err = tokenize_component_meta(meta_properties_prop_no_space)
    assert err_msg == err


def test_tokenize_component_meta_duplicate_prop():
    err_msg = ("Error in /meta properties: duplicate of field:"
               " \"author: Robin T. Gruenke\n\"")
    chunk = ["author: Robin Gruenke\n", "author: Robin T. Gruenke\n"]
    props, err = tokenize_component_meta(chunk)
    assert err_msg == err


def test_tokenize_component_introduction(introduction, introduction_tokenized):
    intro = tokenize_component_introduction(introduction)
    assert intro == introduction_tokenized


def test_tokenize_component_introduction_w_link(introduction_w_link, introduction_tokenized_w_link):
    intro = tokenize_component_introduction(introduction_w_link)
    assert intro == introduction_tokenized_w_link


def test_tokenize_component_introduction_empty():
    intro = tokenize_component_introduction(["      \n", "   "])
    assert intro == ["", None]


def test_parse_component_meta():
    err_msg = "Error in /meta properties: field required: \"author\""
    meta, err = parse_component_meta({})
    assert err == err_msg and meta is None


def test_parse_component_meta_missing_website():
    err_msg = "Error in /meta properties: field required: \"website\""
    meta, err = parse_component_meta({"author": "Robin Gruenke"})
    assert err == err_msg and meta is None


def test_parse_component_meta_missing_year():
    err_msg = "Error in /meta properties: field required: \"year\""
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_missing_title():
    err_msg = "Error in /meta properties: field required: \"title\""
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2021",
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_missing_description():
    err_msg = "Error in /meta properties: field required: \"description\""
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2021",
        "title": "Journal - Generate Html Tool | robingruenke.com"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_missing_keywords():
    err_msg = "Error in /meta properties: field required: \"keywords\""
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2021",
        "title": "Journal - Generate Html Tool | robingruenke.com",
        "description": "Generate static html flexible, approachable, consistent"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_missing_year_unordered():
    err_msg = "Error in /meta properties: field required: \"year\""
    meta, err = parse_component_meta({
        "title": "Journal - Generate Html Tool | robingruenke.com",
        "description": "Generate static html flexible, approachable, consistent",
        "keywords": "html text python generate tool",
        "website": "https://www.robingruenke.com",
        "author": "Robin Gruenke",
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_random_prop():
    err_msg = "Error in /meta properties: field required: \"author\""
    props = [
        ("title", "Journal - Generate Html Tool | robingruenke.com"),
        ("description", "Generate static html flexible, approachable, consistent"),
        ("keywords", "html text python generate tool"),
        ("website", "https://www.robingruenke.com"),
        ("year", "2021")
    ]
    prop = random.choice(props)
    meta, err = parse_component_meta(dict([prop]))
    assert err == err_msg and meta is None


def test_parse_component_meta_random_prop_2():
    err_msg = "Error in /meta properties: field required: \"website\""
    props = [
        ("title", "Journal - Generate Html Tool | robingruenke.com"),
        ("description", "Generate static html flexible, approachable, consistent"),
        ("keywords", "html text python generate tool"),
        ("year", "2021")
    ]
    prop = random.choice(props)
    d = dict([("author", "Robin Gruenke"), prop])
    meta, err = parse_component_meta(d)
    assert err == err_msg and meta is None


def test_parse_component_meta_with_author_not_set():
    err_msg = ("Error in /meta properties: ensure this value has"
               " at least 2 characters: \"author\"")
    meta, err = parse_component_meta({"author": ""})
    assert err == err_msg


def test_parse_component_meta_with_author_too_long():
    err_msg = ("Error in /meta properties: ensure this value has"
               " at most 48 characters: \"author\"")
    a = "abcdefghiklmnopqrstuvwxyzabcdefghiklmnopqrstuvwxyzabcdefg"
    meta, err = parse_component_meta({"author": a})
    assert err == err_msg and meta is None


def test_parse_component_meta_with_invalid_url():
    err_msg = ("Error in /meta properties: invalid or missing"
               " URL scheme: \"website\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "abcdefg"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_with_invalid_url_protocol():
    err_msg = "Error in /meta properties: URL scheme not permitted: \"website\""
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "http://www.robingruenke.com"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_with_year_not_set():
    err_msg = ("Error in /meta properties: ensure this value has"
               " at least 4 characters: \"year\"")

    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": ""
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_with_invalid_year():
    err_msg = ("Error in /meta properties: ensure this value has "
               "these formats of integers \"2020 - 2021\" or \"2020\": "
               "\"year\"")

    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "20144"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_with_invalid_data():
    err_msg = ("Error in /meta properties: ensure this value has "
               "these formats of integers \"2020 - 2021\" or \"2020\": "
               "\"year\"")

    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "abcd"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_with_two_years():
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2020 - 2021",
        "title": "Journal - Generate Html Tool | robingruenke.com",
        "description": "Generate static html flexible, approachable, consistent",
        "keywords": "html text python generate tool"
    })
    assert err is None \
        and meta.year == "2020 - 2021" \



def test_parse_component_meta_title_shortness():
    err_msg = ("Error in /meta properties: ensure this value has at least"
               " 24 characters: \"title\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2020",
        "title": "Journal"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_title_length():
    err_msg = ("Error in /meta properties: ensure this value has"
               " at most 60 characters: \"title\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2020",
        "title": fixed_str("a", 61)
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_description_shortness():
    err_msg = ("Error in /meta properties: ensure this value has at least"
               " 50 characters: \"description\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2020",
        "title": fixed_str("a", 60),
        "description": "Description"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_description_length():
    err_msg = ("Error in /meta properties: ensure this value has"
               " at most 160 characters: \"description\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2020",
        "title": fixed_str("a", 60),
        "description": fixed_str("a", 161)
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_keywords_not_set():
    err_msg = ("Error in /meta properties: ensure this value has"
               " exactly 5 words with at least 3 characters and up to 16"
               " for each word: \"keywords\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2020",
        "title": fixed_str("a", 60),
        "description": fixed_str("a", 60),
        "keywords": ""
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_keywords_not_enough_words():
    err_msg = ("Error in /meta properties: ensure this value has"
               " exactly 5 words with at least 3 characters and up to 16"
               " for each word: \"keywords\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2020",
        "title": fixed_str("a", 60),
        "description": fixed_str("a", 60),
        "keywords": "abc def"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_keywords_words_too_short():
    err_msg = ("Error in /meta properties: ensure this value has"
               " exactly 5 words with at least 3 characters and up to 16"
               " for each word: \"keywords\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2020",
        "title": fixed_str("a", 60),
        "description": fixed_str("a", 60),
        "keywords": "ab de ca ge gt"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_keywords_six_words():
    err_msg = ("Error in /meta properties: ensure this value has"
               " exactly 5 words with at least 3 characters and up to 16"
               " for each word: \"keywords\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2020",
        "title": fixed_str("a", 60),
        "description": fixed_str("a", 60),
        "keywords": "abf dew cax gef gta tya"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_keywords_duplicate():
    err_msg = ("Error in /meta properties: ensure this value has"
               " no duplicates in it: \"keywords\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2020",
        "title": fixed_str("a", 60),
        "description": fixed_str("a", 60),
        "keywords": "abc abc cax gef gta"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_with_required_properties():
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2021",
        "title": "How my web journal is build",
        "description": "Generate static html flexible, approachable, consistent",
        "keywords": "html text python generate tool"
    })
    assert err is None \
        and meta.author == "Robin Gruenke" \
        and meta.website == "https://www.robingruenke.com" \
        and meta.year == "2021" \
        and meta.title == "How my web journal is build" \
        and meta.description == "Generate static html flexible, approachable, consistent" \
        and meta.keywords == "html text python generate tool"


def test_parse_component_meta_with_unknown_properties():
    err_msg = ("Error in /meta properties: extra fields not permitted:"
               " \"unknown\"")
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2021",
        "title": "How my web journal is build",
        "description": "Generate static html flexible, approachable, consistent",
        "keywords": "html text python generate tool",
        "unknown": "stuff"
    })
    assert err == err_msg and meta is None


def test_parse_component_meta_with_optional_optout():
    meta, err = parse_component_meta({
        "author": "Robin Gruenke",
        "website": "https://www.robingruenke.com",
        "year": "2021",
        "title": "How my web journal is build",
        "description": "Generate static html flexible, approachable, consistent",
        "keywords": "html text python generate tool",
        "optout": "a b c d e"
    })
    assert err is None and meta.optout == "a b c d e"


def test_parse_component_introduction_content_length():
    err_msg = "Error in /introduction: ensure introduction content has at most 600 characters"
    intro, err = parse_component_introduction([
        fixed_str("a", 601), None
    ])
    assert intro is None and err == err_msg


def test_parse_component_introduction_content_shortness():
    err_msg = "Error in /introduction: ensure introduction content has at least 50 characters"
    intro, err = parse_component_introduction([
        fixed_str("a", 49), None
    ])
    assert intro is None and err == err_msg


def test_parse_component_introduction_link_text_length():
    err_msg = "Error in /introduction: ensure link text has at most 16 characters"
    link = {"text": fixed_str("a", 17), "url": "https://www.robingruenke.com"}
    intro, err = parse_component_introduction([
        fixed_str("a", 50), link
    ])
    assert intro is None and err == err_msg


def test_parse_component_introduction_link_text_shortness():
    err_msg = "Error in /introduction: ensure link text has at least 3 characters"
    link = {"text": "aa", "url": "https://www.robingruenke.com"}
    intro, err = parse_component_introduction([
        fixed_str("a", 50), link
    ])
    assert intro is None and err == err_msg


def test_parse_component_introduction_link_url():
    err_msg = "Error in /introduction: URL scheme not permitted"
    link = {"text": "aaa", "url": "http://www.robingruenke.com"}
    intro, err = parse_component_introduction([
        fixed_str("a", 50), link
    ])
    assert intro is None and err == err_msg


def test_parse_component_introduction_with_required():
    link = {"text": "aaa", "url": "https://www.robingruenke.com"}
    intro, err = parse_component_introduction([
        fixed_str("a", 50), link
    ])
    assert err is None \
        and intro.content == fixed_str("a", 50) \
        and intro.link.text == "aaa" \
        and intro.link.url == "https://www.robingruenke.com"

###########################################
############## HELPERS ####################
###########################################


# Python 3.8 use functools.cache
@lru_cache(maxsize=None)
def fixed_str(c: str, l: int):
    return c * l


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


def remove_blank_lines(chunk):
    new_chunk = []
    for line in chunk:
        if line.isspace():
            new_chunk.append(line)

    return new_chunk


def time_test_chunk_complete_document():
    f = open(os.path.join(dir, 'fixtures', "test.journal"))
    chunks = chunk_document(f)


if __name__ == "__main__":
    cProfile.run("time_test_chunk_complete_document()")
