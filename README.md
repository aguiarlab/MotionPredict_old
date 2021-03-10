# MotionPredict

## SequentialCoveringAlgorithm

Will split the data 80% for training and 20% for testing. Outputs 2 files: ```/path/to/TrainingData.csv``` and ```/path/to/TestingData.csv```
```
python3 TrainingTestingSplit.py /path/to/corpus
```

Runs the sequential covering algorithm on the training data. Second parameter is the specified cuttoffscore found from cross validation. Third parameter is either "foil" or "simple" to run on those conditions. Outputs a csv file containing the rules in the form of ```[/path/to/Simple_Rules_.csv]``` or ```[/path/to/Foil_Rules_.csv]``` depending on the third parameter.
```
python3 sca.py /path/to/TrainingData.csv 0.2 simple
```
Classifies documents in the testing data. Will output file in the form of ```[/path/to/Simple_classifier_.csv]``` or ```[/path/to/Foil_classifier_.csv]``` depending on the third parameter. 
```
python3 predict.py /path/to/TestingData.csv /path/to/Simple_Rules_.csv simple
```
Prints the classification accuracy .
```
python3 classification_accuracy.py /path/to/TestingData.csv /path/to/Simple_classifier_.csv
```

## word2vec_doc2vec

Scrapes appellate court opinions off of the State of Connecticut Judicial Branch website and adds the contents of the files into a new file in the form of ```[/path/to/AppellateOpinionLegalData.txt]```.
```
pthon3 appellateScrape.py
```
Lemmatizes and tokenizes the words in the documents and output a new file in the form of ```[/path/to/Appellate_Opinion_To_Be_Embedded.csv]```.
```
python3 appellateDataPrep.py /path/to/AppellateOpinionLegalData.txt
```
The following applies the doc2vec and word2vec pretrained model on the new file and rules from the sequential covering algorithm.
```
python3 doc2vec.py /path/to/Appellate_Opinion_To_Be_Embedded.csv /path/to/pretrained doc2vec models
```
```
python3 word2vec.py /path/to/Appellate_Opinion_To_Be_Embedded.csv /path/to/pretrained word2vec models
```
```
python3 word2vec_rules.py /path/to/rules /path/to/pretrained word2vec models
```

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
