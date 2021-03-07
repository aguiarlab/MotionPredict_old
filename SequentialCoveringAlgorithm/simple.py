import pandas as pd
import csv
import re
import sys

'''
The first parameter is your training data. The condition for generating rules is the simple function for calculating frequency.
You will need to cross validate in order to find the second parameter. The cross validation split can be created using a python script in this directory.

This script outputs a csv file with 5 columns. First column is the word.
Second column is the number of times the word appears in the granted documents. Third column is
the number of times the word appears in the denied documents. Fourth column is the total number of times
the word appears throughout all the documents. Fifth column is a statistic that the simple function outputs.

The command for running this script is the following: python3 name_of_this_script.py your_data your_cutoff_score. For training, suggested cutoff value 
for rule making is 0. With cross validation on our data, best cuttoff score is 0.2
'''

def Simple(trainingData, cutoff):
    #data processing
    GR_DN_nlp_training = pd.read_csv(trainingData, sep='\t')
    print("reading training data complete...")
    GR_DN_nlp_training.dropna(subset=["text"], inplace=True)
    dfCorpusColumns = GR_DN_nlp_training.columns
    c0 = dfCorpusColumns[0]
    c1 = dfCorpusColumns[1]
    c2 = dfCorpusColumns[2]
    listDecomposedWords = []
    for index, row in GR_DN_nlp_training.iterrows():
        idCase = row[c0]
        tvCode = row[c2]
        listTX = row[c1]
        listTX = listTX.lstrip()
        listTX = listTX.rstrip()
        lWords = listTX.split()
        for i in range(len(lWords)):
            try:
                lWords[i].encode(encoding='utf-8').decode('ascii')
            except UnicodeDecodeError:
                continue
            unnecessary_words = re.findall(r'((\w)\2{2,})', lWords[i])
            if len(unnecessary_words) > 0:
                continue
            listRowItems = []
            listRowItems.append(idCase)
            listRowItems.append(lWords[i])
            listRowItems.append(tvCode)
            listDecomposedWords.append(listRowItems)
    print("total words: ", len(listDecomposedWords))
    dfWords = pd.DataFrame(listDecomposedWords)
    dfWords.columns = [c0,'word',c2]


    Finish_run = False
    print("creating rules....")
    countRules = 0
    #sequential covering algorithm start
    while not Finish_run:
        dfGRwords = dfWords[dfWords[c2] == 'GR']
        if dfGRwords.shape[0] == 0:
            break
        GRgrouped = dfGRwords.groupby(['word', c2])[['word']].count()
        GRgrouped = GRgrouped.rename(columns={'word': 'count'})
        GRgrouped = GRgrouped.reset_index()
        dfDNwords = dfWords[dfWords[c2] == 'DN']
        DNgrouped = dfDNwords.groupby(['word', c2])[['word']].count()
        DNgrouped = DNgrouped.rename(columns={'word': 'count'})
        DNgrouped = DNgrouped.reset_index()
    #----------merge 2 dataframes--------------------
        mergedFrames = pd.merge(GRgrouped, DNgrouped, on=['word'], how='outer')
        mergedFrames.drop(['MotionResultCode_x', 'MotionResultCode_y'], axis=1, inplace=True)
        mergedFrames = mergedFrames.rename(columns={'count_x': 'GR_count', 'count_y': 'DN_count'})
        mergedFrames.fillna(0, inplace=True)
        mergedFrames['GR_count'] = mergedFrames['GR_count'].astype(int)
        mergedFrames['DN_count'] = mergedFrames['DN_count'].astype(int)
        mergedFrames['Total_Count'] = mergedFrames["GR_count"] + mergedFrames["DN_count"]
        #simple equation
        mergedFrames['function'] = (mergedFrames.GR_count + 1)/(mergedFrames.Total_Count + 2)
        mvalue = mergedFrames[mergedFrames['function'] == mergedFrames['function'].max()]
        for j, row in mvalue.iterrows():
            if mvalue.loc[j, 'function'] < float(cutoff):
                Finish_run = True
                break
        if Finish_run:
            break
        #writing rules to csv
        if countRules == 0:
            mvalue.to_csv("Rules_simple_.csv", sep='\t', header=True, index=False)
        else:
            mvalue.to_csv("Rules_simple_.csv", sep='\t', mode='a', header=False, index=False)

        mvalue = mvalue.reset_index()
        #removing documents that the rule covers
        docid_to_be_removed = []
        for i, r in mvalue.iterrows():
            if len(dfWords) == 0:
                break
            for j, rw in dfWords.iterrows():
                if dfWords.loc[j, 'word'] == mvalue.loc[i, 'word']:
                    docid_to_be_removed.append(dfWords.loc[j, 'docid'])
                if len(dfWords) == 0:
                    break

        unique_docid = list(set(docid_to_be_removed))
        print("creating remaining words list ...")
        remaining_words = []
        for i, rw in dfWords.iterrows():
            if rw[0] in unique_docid:
                continue
            remaining_words.append(rw)

        dfRemainingWords = pd.DataFrame(remaining_words)
        dfRemainingWords.columns = [c0,'word',c2]

        dfWords = dfRemainingWords

        countRules += 1

        print("total dfWords left, count Rule .... ", countRules, len(dfWords))
        if len(dfWords) == 0:
            Finish_run = True
    print("rules generated...")

if __name__ =='__main__':
    trainingData = sys.argv[1]
    cutoff = sys.argv[2]
    Simple(trainingData, cutoff)
