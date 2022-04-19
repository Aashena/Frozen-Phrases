#This file has functions that work with a sqlite database: (dbUTl)

def filterOutPassages(psg_IDs , answerList , cursor): # Only for passage level
    #This function returns the passages that contain the answer for a question form all passages of a doc.
    #input:
        # psg_IDs:     List of passage IDs of all passages that are in a document or are candidates
        # answerList:  List of answers (string) for a question (derived from line_json_form['answer'] ') 
        #cursor:       A cursor to a db that has table documents with columns: id (psg id) and text
    #return:
        # new_psgIDs:  List of passage IDs that has the answer passage
    new_psgIDs = []
    for psgID in psg_IDs:
        query = 'select text from documents where id = '
        query = query + str(psgID)
        cursor.execute( query )

        psg_text = cursor.fetchall()[0][0]
        if any([(i in psg_text) for i in answerList]):
            new_psgIDs.append(psgID)
    return new_psgIDs
   
def get_psg_text(psg_ID , psg_cursor):
    #get the text of a corresponding passage.
    #input:
        # psg_ID:     id of a passage (int)
        # psg_cursor: a cursor object to a passage sqlite db (.db file)
    # output:
        # psg_text:   The text of the wanted passage
    query = 'select text from documents where id = '
    query = query + str(psg_ID)
    psg_cursor.execute( query )
    psg_text = psg_cursor.fetchall()[0][0]
    return psg_text

def embedVarInSQL_query(query , variable): # this function is refined in dbUTl.py
    #add the variable name at the end of the query
    #input:
        #query:    string of the SQL query that variable should be added to (with = and without ")
        #variable: stirng of the variable that should be added. (title)
    #return:
        #newQuery: new SQL query that is the combination of the given query and the variable
    variable = replaceElementInString('"' , '""' , variable)
    newQuery = query + '"' +variable + '"'
    return newQuery  
    
def get_psgID_from_title( title , psg_cursor):
    #get passage IDs of a document
    #input:
        # title:      title of a document (string)
        # psg_cursor: A cursor object to a passage sqlite db (.db file)
    # output:
        # psg_IDs:    list of psg IDs (list of int)
    query = 'select id from documents where title = '
    query = embedVarInSQL_query(query , title)
    psg_cursor.execute( query )

    psg_IDs = [ i[0] for i in psg_cursor.fetchall() ]
    return psg_IDs
    
def get_answer_psgs_of_doc(title , answerList , psg_cursor ):
    #get passage IDs of a document that contain the answer in the answerList
    #input:
        # title:            title of a document (string)
        # answerList:       List of answers (string) for a question (derived from line_json_form['answer'] ') 
        # psg_cursor:       A cursor object to a passage sqlite db (.db file)
    # output:
        # answer_psg_IDs:   List of passage IDs that has the answer passage (list of int)
    psg_IDs = get_psgID_from_title(title , psg_cursor)
    answer_psg_IDs = filterOutPassages(psg_IDs , answerList , psg_cursor)
    return answer_psg_IDs
    
def replaceElementInString(element , replacementstr , mystr): # refined in dbUTl.py
#     replace an element in a stringwith another element for all occurance of the first element
    #input:
        #element:        an element that should be replaced: string
        #replacementstr: an element that is replacing the other one: string
        #mystr:          The string that we are changing
    #return:
        #mystr:          The changed string
    indexList = []
    newList = []
    while element in mystr:
        badIndex = mystr.index(element)
        tmp = mystr[:badIndex]
        if badIndex+len(element)<len(mystr):
            tmp+= mystr[badIndex+len(element):]
        mystr = tmp
        indexList.append(badIndex)
    for Xindex , x in enumerate(indexList):
        actualIndex = x + Xindex * len(replacementstr)
        mystr = mystr[:actualIndex] + replacementstr + mystr[actualIndex:]
        
    return mystr
    
def get_docText_by_title(DBcursor , title):
    #get the documnet text that has the answer for the question
    #input:
        #DBcursor:     cursor to a sqlite db which has a documnets table with columns id and text
        #title:        string: title of the target document
    #return:
        #doc:          text of the target document
    query = 'select text from documents where id = '
    query = embedVarInSQL_query(query , title)
    DBcursor.execute( query )
    fetched = DBcursor.fetchall()
    if len(fetched) ==0:
        return ''
    doc = fetched[0][0]
    return doc