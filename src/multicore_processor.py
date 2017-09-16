"""A script to process the textual data, and format
it into a pandas dataframe which is then pickeled (A
way of storing objects in python.

The arguments should be given by command line and in the order
<file location> <save location>.  If no arguments are provided, the
script will attempt to read the input file ../data/training_text.csv and save
it to ../data/training_df.pk

Ex usage
$python text_processor ../data/training_text.csv ../data/text_new.pk

 processing data
 2496 lines processed
$
"""
import preprocessing as prep
import pandas as pd
import sys
from multiprocessing import Process, Pool, TimeoutError

help_string="""
A script to process the textual data, and format
it into a pandas dataframe which is then pickeled (A
way of storing objects in python.

The arguments should be given by command line and in the order
<save location> <mode>. 
The valid options for mode are 
  - tokenize
  - stem
  - genes 

Ex usage
$python text_processor ../data/training_text.csv ../data/text_new.pk

 processing data
 2496 lines processed
$
"""
def clean_and_tokenize(x):
    return prep.port_tokenizer(prep.clean_text(x), var, genes)

if __name__=="__main__":
    save_location="../data/training_df.pk"
    training_loc="../data/training_text.csv"
    test_loc = "../data/test_variants.csv"
    train_loc = "../data/training_variants.csv"
    var, genes = prep.get_genes_variants(train_loc, test_loc)
    
    if len(sys.argv)==2:
        if sys.argv[1] in {'help','h','-h','--help'}:
            print(help_string)
            sys.exit()
    elif len(sys.argv)==3:
        method=sys.argv[2]
        save_loc = sys.argv[3]
    else:
        print("unknown option, enter help as command line option for help")

    print('loading dataframe')
    df = pd.read_csv(file_location, delimiter=r'\|\|', index_col=0,
                     encoding='utf-8', engine='python', skiprows=1,
                     names=['text'])
    print('processing data')

    pool = Pool()
    processor = prep.processor(var, genes, method=method)
    df['processed'] = pool.map(processor.process_text, df.text)
    df.to_pickle(save_location)
    print('saved file, {} lines processed'.format(df.size))

