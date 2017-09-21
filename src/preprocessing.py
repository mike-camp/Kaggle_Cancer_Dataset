""" A Collection of preprocessing functions intended to be
used with the kaggle cancer text data
"""
import re
import nltk
import pandas as pd
stopwords = set(nltk.corpus.stopwords.words('english'))


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
    words = re.split(r'[^a-zA-Z0-9-*]+', text)
    ps = nltk.stem.porter.PorterStemmer()

    return [ps.stem(process_word(word, variants, genes)) for word in words
            if process_word(word, variants, genes)]


def tokenizer(text, variants, genes):
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
    words = re.split(r'[^a-zA-Z0-9-*]+', text)
    return [process_word(word, variants, genes) for word in words
            if process_word(word, variants, genes)]


def gene_tokenizer(text, variants, genes):
    """splits a text, and then only returns the words which contain genes
    """
    words = re.split(r'[^a-zA-Z0-9*]', text)
    var_genes = variants.union(genes)
    return [word for word in words if word in var_genes]


def process_word(word, variants, genes):
    """ Returns a word if the word is long enough to be
        a word, is not a number, and is not found in
        var or genes

    Parameters:
    ----------
    word: str
        word to be processed
    var: set(str)
        set of gene variations
    genes: set(str)
        set of genes

    Returns:
    --------
    a string corresponding to processed word or ''
    """
    numbers = {'one', 'two', 'three', 'four', 'five', 'six',
               'seven', 'eight', 'nine', 'ten', 'elevin', 'twelve',
               'hundred', 'thousand', 'million'}
    if word in variants or word in genes:
        return word
    if word in numbers:
        return ''
    if len(word) <= 2:
        return ''
    if word not in stopwords:
        return word.lower()
    return ''


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
    text = re.sub(r'[^a-zA-Z0-9-]([0-9,.%]+)\s', '', text)
    # get rid of apostrophes and quoutes
    text = re.sub("'", '', text)
    text = re.sub('"', '', text)
    return text.strip()


def process_text(text, variants={}, genes={}):
    """Removes references, figure references and numbers from text
    Then tokenizes the text by splitting it up on anything that isn't a letter,
    a number, or a dash, and returns the list, with stopwords removed
    """
    test = clean_text(text)
    return port_tokenizer(text, variants, genes)


class processor(object):

    def __init__(self, variants, genes, method='stem'):
        self.variants = variants
        self.genes = genes
        self.method = method

    def process_text(self, text):
        if self.method == 'stem':
            return process_text(text, self.variants, self.genes)
        elif self.method == 'tokenize':
            return tokenizer(text, self.variants, self.genes)
        elif self.method == 'genes':
            return gene_tokenizer(text, self.variants, self.genes)
