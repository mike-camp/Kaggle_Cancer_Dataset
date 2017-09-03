""" A Collection of preprocessing functions intended to be
used with the kaggle cancer text data
"""
import re
import nltk
import pandas as pd


def port_tokenizer(text, variants, genes):
    """Splits and tokenizes text.   The split is done on
    any pattern that isn't a letter, number, or dash thats longer
    1 or more characters long.

    Parameters:
    ---------------
    text: str, string to tokenize
    variants, set(str)
        Set of all names of variants in test and training set
    genes, set(str)
        Set of all names of genes in the test and trianing set


    Returns:
    ---------------
    list of tokens (strings) formed by splitting the original text
    and removing stopwords (note genes/variants are left uppercase)
    """
    words = re.split(r'[^a-z0-9-]+', text.lower())
    ps = nltk.stem.porter.PorterStemmer()

    def process_word(word):
        if word in variants or word in genes:
            return word
        if word and word not in nltk.corpus.stopwords.words('english'):
            return ps.stem(word.lower())
        return ''
    return [process_word(word) for word in text if word]


def get_genes_variants(train_loc, test_loc):
    """
    finds the genes and the varients from
    the data and stores them in a two sets.

    Parameters:
    -----------
    train_loc: str
        filename of training data
    test_loc: str
        filename of test data

    Returns:
    --------
    Varients:
        set of all possible variations
    genes:
        set of all possible genes
    """
    df_train = pd.read_csv(train_loc, index_col=0)
    df_test = pd.read_csv(test_loc, index_col=0)
    genes = set(df_train.Gene.unique()).union(set(df_test.Gene.unique()))
    variants = set(df_train.Variation.unique())\
        .union(set(df_test.Variation.unique()))
    return genes, variants


def clean_text(text):
    """Removes references, figure references and numbers from text
    and returns the cleaned string

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
    return text.strip()


def process_text(text):
    """Removes references, figure references and numbers from text
    Then tokenizes the text by splitting it up on anything that isn't a letter,
    a number, or a dash, and returns the list, with stopwords removed
    """
    test = clean_text(text)
    return port_tokenizer(text)
