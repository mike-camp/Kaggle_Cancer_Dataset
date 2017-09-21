""" A module of functions for processing dataframes
into useful features.

"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd

def _return_same(x):
    """Needed for tfidf analyzer"""
    return x


def gene_variation_dataframe():
    """Processes the training and test datasets
        into a usefule collection of features

    Returns:
    --------
    dataframes corresponding to training and test data
        df_train
        df_test
    """
    df_train = pd.read_csv('../data/training_variants.csv', index_col='ID')
    df_test = pd.read_csv('../data/test_variants.csv', index_col='ID')
    df = pd.concat((df_train, df_test))
    df = df.reset_index(drop=True)
    df_stemmed = pd.concat((pd.read_pickle('../data/stem-train.pk'),
                            pd.read_pickle('../data/stem-test.pk')))
    df_genes = pd.concat((pd.read_pickle('../data/genes-train.pk'),
                          pd.read_pickle('../data/genes-test.pk')))
    df['stemmed_text'] = df_stemmed.reset_index(drop=True).processed
    del df_stemmed
    df['text_gene_var'] = df_genes.reset_index(drop=True).processed
    del df_genes
    df_genes = find_gene_components(df)
    X_text = find_pca_components(df.stemmed_text,n_components=250)
    return np.hstack((df_genes.values,X_text))


def find_gene_components(df):
    """breaks the gene components up into several features.
    """
    columns = ['gene_present','variation_present']
    df['gene_present'] = df.apply(lambda r: r['Gene'] in r['text_gene_var'],
                                  axis=1)
    df['variation_present'] = df.apply(lambda r: r['Variation'] in
                                       r['text_gene_var'], axis=1)
    for i in range(2, 10):
        df['gene_let_{}'.format(i)] = df.Gene.map(lambda x: ord(x[i]) if
                                                  i < len(x) else -1)
        columns.append('gene_let_{}'.format(i))
    for i in range(3, 20):
        df['var_let_{}'.format(i)] = df.Variation.map(lambda x: ord(x[i]) if
                                                       i < len(x) else -1)
        columns.append('var_let_{}'.format(i))
    return df[columns]




def find_pca_components(word_series, n_components=100):
    """Computes the tfidf of df.processed, then
    finds the top n_components principle components,
    and returns the fitted dataframe.

    Parameters:
    -----------
    df dataframe, must have column named processed
    n_components, int
        number of principle components to find

    Returns:
    --------
    X: arraylike shape n_samples, n_components
    """
    tfidf = TfidfVectorizer(min_df=10, analyzer=_return_same)
    X = tfidf.fit_transform(word_series)
    pca = PCA(n_components=n_components)
    X = pca.fit_transform(X.toarray())
    return X






