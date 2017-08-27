# Kaggle_Cancer_Dataset
A repository for the kaggle cancer compitition

## Goal:

For each gene mutation there are several journal articles which can be parsed by a human to decide how harmful/benign it may be.  Currently this takes a long time, and the goal of this compitition is to create a machine learning algorithm to predict how benign or harmful mutation is given the literature.  

## Dataformat

There are training and test csv files which correspond to either variants or text.

1. variants: columns = (ID,Gene,Variation,Class)
  - ID: int, Index Column
  - GENE: str, name of gene
  - Mutation: str, mutation in gene
  - Class: int, 1-9, class of mutation (corresponds to cancer risk), this is the column we are trying to predict
2. text: columns = (ID,Text)
  - ID: int, Index Column
  - Text: str, long string corresponding to portions of journal articles which are related to the gene mutation

