#/usr/bin/python2
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

if __name__=="__main__":
    if len(sys.argv)==0:
        save_location="../data/training_df.pk"
        file_location="../data/text_training.csv"
    elif len(sys.argv)==3:
        save_location=sys.argv[2]
        file_location=sys.argv[1]
    elif len(sys.argv)==2:
        if sys.argv[1] in {'help','h','-h','--help'}:
            print(help_string)
            sys.exit()
    else:
        print("unknown option, enter help as command line option for help")

    print('loading dataframe')
    df = pd.read_csv(file_location,delimiter='\|\|',index_col=0,
                     encoding='utf-8',engine='python',skiprows=1,
                     names=['text'])
    print('processing data')
    df['text'] = df.text.map(prep.clean_text)
    df['text'] = df.text.map(prep.port_tokenizer)
    df.to_pickle(save_location)
    print('saved file, {} lines processed'.format(df.size))


