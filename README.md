# MotionPredict

All code in this repository was used in the manuscript - MotionPredict: Case-level Prediction of Motion Outcomes in Civil Litigation.<br>

Upon approval of CT Judical Branch a subset of our data will be provided for testing and exploritary use.<br>

## SequentialCoveringAlgorithm
To obtain training, testing, and cross validation data run 
```
python3 scap.py splitdata
```
It creates 2 directories. One is called TrainTest which contains training and testing data. The other is called CrossValidationData which contains kfold cross validation data.

To run cross validation 
```
python3 sca.py CV foil
``` 
Will print suggested threshold to stop making rules. Will also output directories containing results.txt files that have threshold and its respective calculated accuracy.

To run the final training data on the test data run: 
```
python3 sca.py ./DataPrep/TrainTest/TrainingData.csv 8 foil
```
Will also create directory containg rules in a txt file as well as prints the classification accuracy.

## word2vec_doc2vec

If one wants, this will scrape appellate court opinions off of the State of Connecticut Judicial Branch website and adds the contents of the files into a new file  ```[/path/to/AppellateOpinionLegalData.txt]```.
```
pthon3 appellateScrape.py
```
Lemmatizes, stems and tokenizes the words in the documents and output a new file in the form of ```[/path/to/Appellate_Opinion_To_Be_Embedded.csv]```.
```
python3 appellateDataPrep.py /path/to/AppellateOpinionLegalData.txt
```
If one would like, the following applies the doc2vec and word2vec pretrained model on the new file and rules from the sequential covering algorithm.
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

### adding_w2v_d2v script

Will go through all of the data given to match the sparse data with the dense data.<br>
Argument 1 is the complaint documents in the form of columns=["page", "docid", "text", "certainty"]<br>
Argument 2 is the path to the input data without the attorney specilization<br>
Argument 3 is the document translation table in the form columns=['DocumentNo','CaseRefNum']<br>
Argument 4 is the simple rules generated in the sequential covering algorithm script<br>
Argument 5 is the foil rules generated in the sequential covering algorithm script<br>
Argument 6 is the path to doc2vec embeddings<br>
Argument 7 is the path to the word2vec embeddings<br>
Argument 8 is the path to the data containing the attorney specilization<br>

The scripts can be ran as follows:
```
python3 adding_w2v_d2v.py /path/to/strikemotion_code_T_V_complaint_doc_ocr.txt.gz /path/to/motionStrike_TVcodes_data.tsv.gz /path/to/judcaseid_docid_translationtable.tsv.gz /path/to/rules/simple_Rules.csv /path/to/rules/foil_Rules.csv /path/to/word2vec/ /path/to/doc2vec/ /path/to/motionStrike_TVcodes_data_dm.tsv.gz
```
The output will be new data files in the same directory as the input with an appended name to it based on the word2vec or doc2vec model used.

# classifiers script

This script will do a grid search over the 7 different models depending on the ones sepcified for argument 2.<br>
Argument 1 is the data to do a grid search over.<br>
Argument 2 is the algorithm to run, pick one of  [0,1,2,3,4,5,6]<br>
Argument 3 is the subset of features to use, pick one of ['minimal','subset','full']<br>

The script can be run as follows:
```
python3 classifiers.py /path/to/motionStrike_TVcodes_data.tsv.gz [0-6] ['minimal','subset','full']
```
The out put from this is to stderr and stdout. Where stderr is outputting the feature importance from the top parameters for the model.
Stdout will have the train and test accuracy from the best parameters.

When running the model split the output so stderr goes to a .err file and the input goes to a .out file with the same root name.

### pull_params script

This script is using the ouput from the classifiers script to pull the best scoring parameters from the machine learning models.<br>
Argument 1 path to the output files from classifiers.py<br>
Argument 2 if the sequential covering algorithm was used or not (rules or no rules) [-r, -nr]<br>
Argumetn 3 the name you want for the output of the best parameters<br>

The script can be ran as followed:
```
python3 pull_params.py /path/to/errorAndOutFiles/ [-r,-nr] output_dictionary_params.pickle
```

The output will be a dictionary containing the best parameters for each model, feature set, rules, and data set (database or dm)

### bootstrap script

This script will run 100 bootstraps of the model you desire with the feature set you want. <br>
Argument 1 the data you want to run <br>
Argument 2 the model you want to run <br>
Argument 3 the dictionary that contains all of the parameters for the model <br>

The code can be run as follows:
```
python3 bootstrap.py /path/to/motionStrike_TVcodes_data.tsv.gz [0-6] ['minimal','subset','full'] output_dictionary_params.pickle
```

The output for this scirpt is stderr and stdout and will out output the 100 bootstraps for each model in the stdout file.

### *.pickle files

All the *.pickle files contain the best parameters that we found for our models, per model, feature set, rules, and data set
