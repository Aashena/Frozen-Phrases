import pandas as pd
import json
import dbUTl
import spacyUTl


def calculate_big_gap(status):
    #status indecated the # of previous big gaps BG1,BG2,BG3,BG4
    if status=='M':
        return -1,'BG1'
    
    statusInt = int(status[-1])
    if statusInt >= 3:
        return -1,'BG4'
    elif statusInt == 2:
        return -4,'BG3'
    elif statusInt == 1:
        return -2,'BG2'
    elif statusInt == 0:
        return -1,'BG1'

def longestSubSequenceFinder_weighted(bigList , smallList , idx):
    # returns the longest common sub-sequence of two list:
    #input:
        #bigList:      The bigger list (list of anything but normally string)
        #smallList:   The small list (list of anything but normally string)
        #idx:          An index object to get the idfs
    #return:
        #answer:      A list containing the longest common sub-sequence of two list.
        #tag_vector:  A list indecating wheather an element in smallList is included in the lCS or not
    # BIG GAP MEANS A GAP IN THE bigList
    # SAMLL GAP MEANS A GAP IN THE smallList
    bLen = len(bigList)
    sLen = len(smallList)
  
    # declaring the arrays for storing the DP values
    ans_score = [[None]*(sLen + 1) for i in range(bLen + 1)]     #score table
    answer = [[None]*(sLen + 1) for i in range(bLen + 1)]        #LCseq table
    tag_vector = [[None]*(sLen + 1) for i in range(bLen + 1)]    #tag table (like NER)
    statusTable = [[None]*(sLen + 1) for i in range(bLen + 1)]   #table to indecate what we had before {M: match , BGX: number of big gaps where X is a number from 0 to 4}
    
    small_gap = -.1
    
    for i in range(bLen + 1):
        for j in range(sLen + 1):
            if j==0: #before the beginning of the question
                if i == 0: #before starting the first word of the question and the document
                    ans_score[i][j] = 0
                else: # the document is started but not the question
                    ans_score[i][j] = ans_score[i-1][j] + calculate_big_gap('BG4')[0]
                answer[i][j] = []
                tag_vector[i][j]=[]
                statusTable[i][j] = 'BG4'
                
            elif i == 0: # The question is started but not the document
                ans_score[i][j] = ans_score[i][j-1] + small_gap
                answer[i][j] = []
                tag_vector[i][j]=['O' for i in range(j)]
                statusTable[i][j] = 'BG4'
                
            else: # we have started passing the question and the document
                matchScore = 0
                isMatched = False
                if bigList[i-1] == smallList[j-1]:
                    isMatched = True
                    #match score calculation
                    matchScore = ans_score[i-1][j-1] + idx.idf(smallList[j-1])
                        
                    if statusTable[i-1][j-1]=='M':
                        matchScore += idx.idf( smallList[j-2] + ' ' + smallList[j-1] )
                    
                #big gap score calculation
                penalty , newBigGapStatus= calculate_big_gap(statusTable[i-1][j])
                bigGscore = ans_score[i-1][j] + penalty
                
                #small gap score calculation
                smlGscore = ans_score[i][j-1] + small_gap
                    
                if i>=3 and j>=2 and isMatched and matchScore>=bigGscore and matchScore>=smlGscore: #When a match happends
                    ans_score[i][j] = matchScore
                    answer[i][j] = answer[i-1][j-1] + [ smallList[j-1] ]
                    tag_vector[i][j]= tag_vector[i-1][j-1] + [ 'SEQ' ]
                    statusTable[i][j] = 'M'
                elif bigGscore>=smlGscore: #When there is a gap in document
                    ans_score[i][j] = bigGscore
                    answer[i][j] =    answer[i-1][j]
                    tag_vector[i][j]= tag_vector[i-1][j]
                    statusTable[i][j] = newBigGapStatus
                else: #When there is a gap in the question
                    ans_score[i][j] = smlGscore
                    answer[i][j] =    answer[i][j-1]
                    tag_vector[i][j]= tag_vector[i][j-1] + [ 'O' ]
                    if statusTable[i][j-1]=='M':
                        statusTable[i][j] = 'BG0'
                    else:
                        statusTable[i][j] = statusTable[i][j-1]
    
    return answer[bLen][sLen] , tag_vector[bLen][sLen]

def convertDataSetLinesToTraingData(lines, idx, cursor_doc=None, q_title_dict=None ):
    # this is a complete preprocess for training a model on LCS predictor model.
    #input:
        #lines: the lines of the dataset (lines of jsonl)
    #return:
        #DF:    Data frame object that is suitable for simple transformer model to be trained on.
    df_list = []
    for index , line in enumerate(lines):
        j_form = json.loads(line)
        if cursor_doc==None:
            question = j_form['question_text']
            text = j_form['document_text']
        else:
            question = j_form['question']
            textTitle = q_title_dict[question]
            text = dbUTl.get_docText_by_title( cursor_doc , textTitle )
    
        
        text = text.lower()
        question = question.lower()
        
        textList = spacyUTl.spacySplit(text)
        qList = spacyUTl.spacySplit(question)
        
        LCseq , LCseq_tags = longestSubSequenceFinder_weighted( textList , qList , idx ) #intersection of the lCSeq with the title
        for term , label in zip(qList ,LCseq_tags ):
            df_list.append( [index , term , label] )

    DF = pd.DataFrame(df_list, columns = [ 'sentence_id' , 'words' , 'labels' ] )
    return DF