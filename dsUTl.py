import json
import pickle as pkl

def get_label_list_jsonl(jsonl_file , label):
    #gets a list of the field that has a certain label
    #input:
        #jsonl_file: an string address of a jsonl_file
        #label:      the label that we need the list of
    #return:
        #label_list: the list of all the enteries of that label
    label_list = []
    with open(jsonl_file , 'r') as f:
        lines = f.readlines()
    for line in lines:
        j_form = json.loads(line)
        label_list.append( j_form[label]  )
    return label_list
    
def creatNewDataset(listOftuples , old_jsonl_dataset, new_jsonl_dataset): #should be refined! where?
    # listOftuples: [(index: int , questions: string), ...]
    dataList = []
    with open(old_jsonl_dataset,'r') as f:
        lines = f.readlines()
    for i in listOftuples:
        data = lines[i[0]]
        json_format = json.loads(data)
        json_format['question'] = i[1]
        data = json.dumps(json_format)
        dataList.append(data)
    with open(new_jsonl_dataset , 'w') as f:
        for i in dataList:
            f.write(i+'\n')
            
def createNewQueryFromSeqLabel(splittedQ , seqLable): # should be refined! where?
    # turn collect the terms form questionList and make a new query (terms that are labeled)
    #input:
        #splittedQ:    a list of question terms (question splitted by splitSpacy() )
        #seqLable:     a label sequence that labels each terms in questionList whether they should or shouldn't come in the final query
    #Return:
        #newQuestion:  The new question generated
    newQuestion = ''
    beforeIsEmpty=False
    for word, dict in zip(splittedQ , seqLable):
        tag = dict[word]
        if tag!='O':
            if beforeIsEmpty==True:
                newQuestion+='kkkkkkkkkkkkkkk '
            beforeIsEmpty=False
            newQuestion+= (word + ' ')
        else:
            beforeIsEmpty=True
    return newQuestion

def MixTwoDataSet(new_jsonl_dataset , old1_jsonl_dataset , old2_jsonl_dataset , old1_freq , old2_freq , splitter='kkkkkkkkkkkkkkk'):
    # concatenate the questions of two dataset create a new dataset: (dataset1*1)+(dataset2*10)
    # Calling example: MixTwoDataSet('1orig_concat_1NNinPOS_dev_converted_hasAnswerer.jsonl', 'orig_dev_converted_hasAnswerer.jsonl' , 'NNinPOS_dev_converted_hasAnswerer.jsonl' , 1 , 1 )
    #input:
        #new_jsonl_dataset:     Name of the new jsonl dataset that its question are the concatenation of the two datasets
        #old1_jsonl_dataset:    Name of dataset one that its question comes first
        #old2_jsonl_dataset:    Name of the dataset two that its questions come after dataset one questions.
        #old1_freq:             The frequency of the dataset one question in the target dataset.
        #old2_freq:             The frequency of the dataset two question in the target dataset.
        #splitter:              The out of vocabulary word that splits each question from each other.
    #return:
        #Nothing
    tupleList = []
    old1Q = get_label_list_jsonl(old1_jsonl_dataset , 'question')
    old2Q = get_label_list_jsonl(old2_jsonl_dataset , 'question')
    for index , (i, j) in enumerate( zip( old1Q ,old2Q )):
        tupleList.append( ( index , (i + ' ' + splitter) * old1_freq + old2_freq * (j + ' ' + splitter) ) )
    creatNewDataset(tupleList , old1_jsonl_dataset, new_jsonl_dataset)
    