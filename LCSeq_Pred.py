import json
import logging
import torch

import pandas as pd
from simpletransformers.ner import NERModel, NERArgs
import dsUTl
import spacyUTl

class Q_Expansion_LCSeq_Pred:
    def __init__(self, model_path , old_dataset , q_label , new_dataset,  qNum , pNum , predict = True , predicted_queries=[]):
        #initialize the parameters and create a new dataset with expanded questions.
        #input:
            #model_path:    path to a pretrained model
            #old_dataset:   path to a jsonl dataset
            #q_label:       the label that questions are located under in the jsonl file
            #new_dataset:   the new dataset path that has the expanded questions.
            #qNum:          number of repetition of the question (int)
            #pNum:          number of repetition of the predicted query (int)
            #predict:       determine to whether do the prediction or not
            #predicted_queries: if the predict is false then the predicted queries should be provided here
        #return:
            #nothing. but create the new dataset in the given path (new_dataset)
        
        if self.is_inconsistent(predict , predicted_queries):
            return
            
        self.questionList = dsUTl.get_label_list_jsonl(old_dataset , q_label)
        if predict:
            self.model = self.get_model_form_model_path(model_path)
            predictions = self.predict_LCSeq(self.model , self.questionList)
            predicted_queries = convert_predictions_to_queries(questions , predictions)
        
        tupleList = get_tuple_list_for_dataset_creation( self.questionList , predicted_queries , qNum , pNum)
        dsUTl.creatNewDataset(tupleList , old_dataset, new_dataset)
    
    def convert_predictions_to_queries(self, questions , tags_list):
        #Converts the list of questions to the list of new questions derived from the predicted tags
        #input:
            #questions: list of questions
            #tags_list: list of tags for each questions: [ [O,O,SEQ,O,... ] , ... ]
        #return:
            #predicted_queries: list of new queries
        predicted_queries = []
        for index , q in enumerate(questions):
            qList = spacyUTl.spacySplit(q)
            newQuery = createNewQueryFromSeqLabel(qList ,tags_list[index] )
            predicted_queries.append(newQuery)
        return predicted_queries
    
    def is_inconsistent(self, predict , predicted_queries):
        #checks if there is any inconsistency in the arguments
        #input:
            #constructor arguments
        #return:
            #True if arguments are inconsistent
        if (predict ==False and len(predicted_queries)==0) or (predict ==True and len(predicted_queries)!=0):
            print("Inonsistency in predict , predicted_queries!")
            return True
        else:
            return False
            
    def get_tuple_list_for_dataset_creation( self, questionList , predicted_queries , qNum , pNum):
        #generates the tupleList that is needed to create a new dataset
        #input:
            #questionList: list of questions
            #predicted_queries: list of predicted questions (list of string)
            #qNum: number of repetition of the question (int)
            #pNum: number of repetition of the predicted query (int)
        #return:
            #tupleList: the tuple list ( [ ( index , new_expanded_query ) , ... ] ) index: int , new_expanded_query:string
        tupleList = []
        splitter = 'kkkkkkkkkkkkkkk'
        for index , (q , p) in enumerate( zip(questionList , predicted_queries) ):
            tupleList.append( ( index , (q + ' ' + splitter) * qNum + pNum * (p + ' ' + splitter) ) )
        return tupleList
        
    def get_model_form_model_path(sefl, model_path):
        #does the basic config for simple transformer and get the model from the path
        #input:
            #path to the pre-trained model
        #return:
            #NERModel object
        cuda_available = torch.cuda.is_available()
        print('Cuda is available: ' , cuda_available)
        logging.basicConfig(level=logging.INFO)
        transformers_logger = logging.getLogger("transformers")
        transformers_logger.setLevel(logging.WARNING)
        model_args = NERArgs()
        model_args.train_batch_size = 64
        model_args.eval_batch_size = 64
        model_args.use_early_stopping = True
        model_args.evaluate_during_training = True
        model_args.learning_rate = 1e-04
        model_args.overwrite_output_dir = True
        model_args.num_train_epochs=70
        model_args.save_model_every_epoch=False
        custom_labels=['O' , 'SEQ']
        
        model = NERModel(
        "roberta", model_path,
        args=model_args , labels=custom_labels,
        use_cuda = cuda_available,
        weight = [1,3.35]
        )
        return model
        
    def predict_LCSeq(self , model , questionList):
        #generates the NERModel predictions for a list of question
        #input:
            #model:         NERModel model object from simple transformers
            #questionList:  list of questions
        #return:
            #predictions: list of predictions: [ [O,O,SEQ,O,... ] , ... ]
        predictions, raw_outputs = model.predict(questionList)
        return predictions