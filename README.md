# MotionPredict

## SequentialCoveringAlgorithm

## word2vec_doc2vec

##  model_data 

### adding_dm script

Will go through the data that is given as argument 1 to the script and identify the attorney specialization for all the attorneys that are present in the data.
This is done through shannons entropy smoothed by a dirichlet multinomial with a dirichlet of [1,1,...,1].
This script can be ran as the following: 
```
python3 adding_dm.py /path/to/motionStrike_TVcodes_data.tsv.gz
```
The output from this code will be a new file in the form [```/path/to/motionStrike_TVcodes_data_dm.tsv.gz```]

### adding_w2v_d2v script

Will go through all of the data given to match the sparse data with the dense data.
Argument 1 is the complaint documents in the form of columns=["page", "docid", "text", "certainty"]
Argument 2 is the path to the input data without the attorney specilization
Argument 3 is the document translation table in the form columns=['DocumentNo','CaseRefNum']
Argument 4 is the simple rules generated in the sequential covering algorithm script
Argument 5 is the foil rules generated in the sequential covering algorithm script
Argument 6 is the path to doc2vec embeddings
Argument 7 is the path to the word2vec embeddings
Argument 8 is the path to the data containing the attorney specilization

The scripts can be ran as follows:
```
python3 adding_w2v_d2v.py /path/to/strikemotion_code_T_V_complaint_doc_ocr.txt.gz /path/to/motionStrike_TVcodes_data.tsv.gz /path/to/judcaseid_docid_translationtable.tsv.gz /path/to/rules/simple_Rules.csv /path/to/rules/foil_Rules.csv /path/to/word2vec/ /path/to/doc2vec/ /path/to/motionStrike_TVcodes_data_dm.tsv.gz
```
The output will be new data files in the same directory as the input with an appended name to it based on the word2vec or doc2vec model used.

# classifiers script

This script will do a grid search over the 7 different models depending on the ones sepcified for argument 2.
Argument 1 is the data to do a grid search over.
Argument 2 is the algorithm to run, pick one of  [0,1,2,3,4,5,6]
Argument 3 is the subset of features to use, pick one of ['minimal','subset','full']

The script can be run as follows:
```
python3 classifiers.py /path/to/motionStrike_TVcodes_data.tsv.gz [0-6] ['minimal','subset','full']
```
The out put from this is to stderr and stdout. Where stderr is outputting the feature importance from the top parameters for the model.
Stdout will have the train and test accuracy from the best parameters.

When running the model split the output so stderr goes to a .err file and the input goes to a .out file with the same root name.

### pul_params script

This script is using the ouput from the 
```
python3 pull_params.py /path/to/errorAndOutFiles/ [-r,-nr] output_dictionary_params.pickle
```

```
python3 bootstrap.py /path/to/motionStrike_TVcodes_data.tsv.gz [0-6] ['minimal','subset','full'] output_dictionary_params.pickle
```
