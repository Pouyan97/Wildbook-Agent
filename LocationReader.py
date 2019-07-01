########################################
# Pouyan Firouzabadi
#
# UIC
########################################
# Needs Stanford CoreNLP installed which isn't used in this program For now.
# from nltk.parse import CoreNLPParser
# from nltk import word_tokenize,pos_tag, ne_chunk, tree2conlltags
#from nltk.corpus import wordnet as wn
# from contextlib import closing
# import sqlite3
# from sys import argv

#### 1. Base Line to recognize the location by matching entities. 
#### 2. Tree built from the dictionary. as hierarchy. 
#### 3. using sentence analysis to get more detailed.

# from collections import Counter
import csv

#Install Spacy and en_core_web_sm through Spacy website.
import spacy
from spacy import displacy
from collections import defaultdict, Counter

#load the english data base downloaded on the system.
nlp = spacy.load("en_core_web_sm")

# These are CoreNLP parsers: To know more Contact Me
# parser = CoreNLPParser(url='http://localhost:9000', encoding = 'utf8')
# ner_parser = CoreNLPParser(url='http://localhost:9000', encoding = 'utf8', tagtype='ner')
# pos_parser = CoreNLPParser(url='http://localhost:9000', encoding = 'utf8', tagtype='pos')


#Youtube video row[1]
#title row[2]

with open('youTubeLocationIDWeka.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    line_count = 0 #To keep track of lines read.
    dic = defaultdict(list) #Dictionary Made

    for row in csv_reader:
        subList = [] #Temp List to Populate the Dictionary

        #Only read lines with data in them (Used to skip attributes since Weka files are complicated)
        if len(row) > 1:
            #Is there any location Estimated?
            if row[5] != '':
                #Make a list of all the estimated location IDs
                for ent in nlp(row[5].replace("'","")).ents:
                    # print(ent.text, ent.start_char, ent.label_) #Print if needed 
                    if ent.label_ == "GPE":
                        subList.append(ent.text)
                #if more than one location found
                if len(subList) > 1:
                    mainLoc = subList.pop()
                    subLoc = subList.pop()
                    dic[mainLoc].append(subLoc)
                    for k in dic:
                        for num in dic[k]: 
                            if subLoc == num:
                                pass
                                # print(f'Location {subLoc} Already On {mainLoc} Dictionary.')
                #if only one loc found
                if len(subList) == 1:
                    mainLoc = subList.pop()
                    dic[mainLoc]
                    #find the Youtube link
                    if row[1] != '':
                        splitString = row[1].rpartition('v=')
                        print(f'YouTube Video Missing Location info for {mainLoc} : {splitString[-1]}.')
                    #not a YouTube Video
                    else:
                        print(f'{row[0]} Would You Mind Telling Me More About Where Exactly In {mainLoc}.')
                #No Location was Detected.
                else:
                    continue
            else:
                print(f'No Location Detected for {row[0]}')
                # tokens = word_tokenize(row[5].replace("'",""))
                # NER = list(ner_parser.tag(tokens))
                # print(NER)
        subList.clear()
        line_count += 1
        # if line_count == 200: #to get faster results.
            # break;


    print(f'Processed {line_count} lines.')
    # print(str(dic))

#Making An Output File.
##############################################
    final_list = [] #To filter repeating data.
    outputFile = open("output.txt" ,'w')
    for k in dic:
        for num in dic[k]: 
            if num not in final_list: 
                final_list.append(num) 
        #use the loop to write in the File.
        outputFile.write(f"{k}:  {list(final_list)}\n\n")
        final_list.clear()
    


######### Testing reading Weka Files ##########
################################################################################################################
        # if line_count == 0:
        # print(f'Column names are {", ".join(row)}')
        # print(row)
        # print(len(row))
        # print(row[1])

        # else:
        #     print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            # line_count += 1


# import weka.core.jvm as jvm
# from weka.core.converters import Loader
# data = loader.load_file(data_dir + "youTubeLocationIDWeka.csv")
# data.class_is_last()

# from weka.attribute_selection import ASSearch, ASEvaluation, AttributeSelection
# search = ASSearch(classname="weka.attributeSelection.BestFirst", options=["-D", "1", "-N", "5"])
# evaluator = ASEvaluation(classname="weka.attributeSelection.CfsSubsetEval", options=["-P", "1", "-E", "1"])
# attsel = AttributeSelection()
# attsel.search(search)
# attsel.evaluator(evaluator)
# attsel.select_attributes(data)

# print("# attributes: " + str(attsel.number_attributes_selected))
# print("attributes: " + str(attsel.selected_attributes))
# print("result string:\n" + attsel.results_string)