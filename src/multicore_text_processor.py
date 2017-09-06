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
<file location> <save location>.  If no arguments are provided, the
script will attempt to read the input file ../data/training_text.csv and save
it to ../data/training_df.pk

Ex usage
$python text_processor ../data/training_text.csv ../data/text_new.pk

 processing data
 2496 lines processed
$
"""
def clean_and_tokenize(x):
    return prep.port_tokenizer(prep.clean_text(x),var,genes)

if __name__=="__main__":
    if len(sys.argv)==0:
        save_location="../data/training_df.pk"
        file_location="../data/training_text.csv"
    elif len(sys.argv)==3:
        save_location=sys.argv[2]
        file_location=sys.argv[1]
    elif len(sys.argv)==4:
        variants_loc=sys.argv[3]
        save_location=sys.argv[2]
        file_location=sys.argv[1]
        keep_genes_variations=True
    elif len(sys.argv)==2:
        if sys.argv[1] in {'help','h','-h','--help'}:
            print(help_string)
            sys.exit()
    else:
        print("unknown option, enter help as command line option for help")

    print('loading dataframe')
    df = pd.read_csv(file_location, delimiter=r'\|\|', index_col=0,
                     encoding='utf-8', engine='python', skiprows=1,
                     names=['text'])
    print('processing data')
    if keep_genes_variations:
        if 'test' in variants_loc:
            test_loc = variants_loc
            train_loc = variants_loc.replace('test', 'training')
        elif 'train' in variants_loc:
            test_loc = variants_loc.replace('training', 'test')
            train_loc = variants_loc
        else:
            print('cannot find test/train files')
            print('please ensure that both train/test files exist')
            sys.exit()
        var, genes = prep.get_genes_variants(train_loc, test_loc)
    else:
        var, genes = set(), set()


    # Implement the multiprocessing class by creating multiple threads
    pool = Pool()
    def process(text):
        return prep.process_text(text, var, genes)
    df['processed'] = pool.map(process,df.text)
    df.to_pickle(save_location)
    print('saved file, {} lines processed'.format(df.size))


