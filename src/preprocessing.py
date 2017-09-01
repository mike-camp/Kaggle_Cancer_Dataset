""" A Collection of preprocessing functions intended to be
used with the kaggle cancer text data
"""
import re
import nltk


def port_tokenizer(text):
    """Splits and tokenizes text.   The split is done on
    any pattern that isn't a letter, number, or dash thats longer
    1 or more characters long.

    Parameters:
    ---------------
    text: str, string to tokenize

    Returns:
    ---------------
    list of tokens (strings) formed by splitting the original text
    """
    words = re.split(r'[^a-z0-9-]+', text.lower())
    ps = nltk.stem.porter.PorterStemmer()
    return [ps.stem(word) for word in words if word not in
            nltk.corpus.stopwords.words('english') and word]


def clean_text(text):
    """Removes references, figure references and numbers from text
    and returns the lowercase string

    example:
    >>>process_text("As we can see from fig. 1 and the results from [1]")
       "As we can see from and the results from"

    >>>process_test("If the quantity is increased by .132%, (ref. 1)")
       "If the quantity is increased"

    Parameters:
    -----------------
    text: str, string to process

    Return:
    -----------------
    cleansed string
    """
    # add space to beginning and end to allow regex to match beginning and end
    text = ' '+text+' '
    # remove references ie "(ref. 1)"
    text = re.sub(r'\([Rr]ef[^)]+\)', '', text)
    #  remove figures, ie "Fig 1"
    text = re.sub(r'(:?[fF]ig)(:?s)?(:?\.|(ure))(:?\s*[a-zA-Z0-9]+)',
                  '', text)
    # remove numeric references ie "[1]"
    text = re.sub(r'[([][0-9, ]*[)\]]', '', text)
    # remove letter refernces, ie "[A]"
    text = re.sub(r'[([][a-zA-Z][)\]]', '', text)
    # remove numbers
    text = re.sub(r'\s([0-9,.%]+)\s', '', text)
    return text.lower().strip()


def process_text(text):
    """Removes references, figure references and numbers from text
    Then tokenizes the text by splitting it up on anything that isn't a letter,
    a number, or a dash, and returns the list, with stopwords removed
    """
    test = clean_text(text)
    return port_tokenizer(text)
