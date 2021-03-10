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

```
python3 adding_w2v_d2v.py /path/to/strikemotion_code_T_V_complaint_doc_ocr.txt.gz /path/to/motionStrike_TVcodes_data.tsv.gz /path/to/judcaseid_docid_translationtable.tsv.gz /path/to/rules/simple_Rules.csv /path/to/rules/foil_Rules.csv /path/to/word2vec/ /path/to/doc2vec/ /path/to/motionStrike_TVcodes_data_dm.tsv.gz
```

```
python3 classifiers.py /path/to/motionStrike_TVcodes_data.tsv.gz [0-6] ['minimal','subset','full']
```

```
python3 pull_params.py /path/to/errorAndOutFiles/ [-r,-nr] output_dictionary_params.pickle
```

```
python3 bootstrap.py /path/to/motionStrike_TVcodes_data.tsv.gz [0-6] ['minimal','subset','full'] output_dictionary_params.pickle
```
