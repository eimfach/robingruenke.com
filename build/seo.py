import nltk


def extract_nouns(s):
    ft = ["NN", "NNP"]
    t = nltk.word_tokenize(s)
    tags = nltk.pos_tag(t)
    tags = [t for t in tags if t[0].isalpha()]
    return [word for word, pos in tags if pos in ft]


def most_common_words_histogram(s):
    tokens = nltk.word_tokenize(s)
    return nltk.FreqDist(tokens).most_common(5)
