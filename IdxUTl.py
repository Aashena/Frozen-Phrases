#This file has function that work with an index object. (IdxUTl)

def get_parsed(query , idxx):
    #Parsing a string by the index object (getting all ngrams that index supports)
    #input:
        # query:       String to extract th ngrams from
        # idxx:        Index object (should have .parse() )
    #return:
        # parsed_tmp:  
    parsed_tmp = idxx.parse(query)
    return parsed_tmp
    
def deleteElementFromList(element , mylist):
    #delete an element form a list  (only the firs occurance)
    #input:
        #element: The element that should be deleted if it is presented in the list
        #mylist:  The list that we want to delete the element from
    #return:
        #tmp:     The new list without the unwanted element
    badIndex = mylist.index(element)
    tmp = mylist[:badIndex]
    if badIndex+1<len(mylist):
        tmp.extend( mylist[badIndex+1:] )
    return tmp
   
def get_ngram_parsed(query , idxx , ngram):
    # get all ngram of a query that exist in the index (ngram is specified)
    #input:
        #query: string (the question)
        #idxx:  index object
        #ngram: int: specifys the n value for 'n'-gram
    #return:
        #parsed: a list of all requested ngrams.
    parsed_tmp = idxx.parse(query)
    parsed = []
    for i in parsed_tmp:
        if len(i.split()) == ngram:
            parsed.append(i)
    while 'kkkkkkkkkkkkkkk' in parsed:
        parsed = deleteElementFromList('kkkkkkkkkkkkkkk' , parsed)
    return parsed
    
def get_doctf_from_question(parsed_q_list , idx , psg_IDs):
    # get the term frequency in some passages
    #input:
        # parse_q_list: List of terms (ngrams)
        # idx:          Our index object (should have: .term_dict[] , .get_doc_index() , .freq_matrix[])
        # psg_IDs:      List of our passage IDs that we want to check the tf in them
    #return:
        #doc_tf_list:   List of integers corresponding to the tf of each term with the same index
    doc_tf_list = []
    for term in parsed_q_list:
        try:
            term_index = idx.term_dict[term]
            doc_tf = 0
            for psg_ID in psg_IDs:
                psg_index = idx.get_doc_index(psg_ID)
                doc_tf+=idx.freq_matrix[term_index,psg_index]
            doc_tf_list.append(doc_tf)
        except KeyError:
            doc_tf_list.append(0)
    return doc_tf_list
    
