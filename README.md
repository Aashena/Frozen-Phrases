# Frozen-Phrases
Supporting matterial for the paper "Detecting Frozen Phrases in Open-Domain Question Answering"
#### Index file:
We used the Following index file to get IDF of each term (for calculating the score of an alignment):  [Coming soon]()
You can load the index by:
```python
from semir.ir import InvertedIndex
idx = InvertedIndex('/path/docs-freqs-ngram=2-tokenizer=spacy-filter=all.npz')
```
#### .db file:
We used the Following .db file to store the corpus:  [Coming soon]()
You can connect to the .db file using sqlite:
```python
import sqlite3
con_doc = sqlite3.connect('/path/docs.db')
cursor_doc = con_doc.cursor() # you will need the cursor object for generating the development set
```
## Data Generation
You can use the `longestSubSequenceFinder_weighted(bigList , smallList , idx)` function in alignment.py to extract the question frozen phrase by aligning the quesiton to its answer document: (You should tokenize the question and the document first. we use spacy tokenization)
```python
import alignment as alig
import spacyUTl
bigList = spacyUTl.spacySplit(document_text) #tokenizing the answer document
smallList = spacyUTl.spacySplit(question_text) #tokenizing the question "who wrote he ai n't heavy he 's my brother lyrics"
LCseq , LCseq_tags = longestSubSequenceFinder_weighted(bigList , smallList , idx)
LCseq: ['he', 'ai', "n't", 'heavy', 'he', "'s", 'my', 'brother']
LCseq_tags: [ 'O', 'O', 'LCSeq', 'LCSeq', 'LCSeq', 'LCSeq', 'LCSeq', 'LCSeq', 'LCSeq', 'LCSeq', 'O' ]
```
### Training and validation sets
We have generated our training and validation set from [NQ training set](https://ai.google.com/research/NaturalQuestions/download) (v1.0-simplified_simplified-nq-train.jsonl)
training set: `LCS_training_data.pickle`
evaluation set: `LCS_validation_data.pickle`
You can simply use the `convertDataSetLinesToTraingData` function in alignment.py and pass it the lines of the jsonl file in a list:
```python
import alignment as alig
with open('v1.0-simplified_simplified-nq-train.jsonl' , 'r') as f: #reading the lines of the NQ training set
    lines = f.readlines() 
train_data = alig.convertDataSetLinesToTraingData(lines) 
with open('LCS_training_data.pickle' , 'wb') as f:
    pkl.dump(train_data , f)
```
### Development set
The generated Develompent set: LCS_development_data.pickle
We used the [NQ-open development set](https://huggingface.co/datasets/nq_open) to generate our development set. NQ-open dataset and its corpus is a subset of NQ dataset and corpus. However, we have some questions in NQ-open devset that their answer document which is identified in the NQ dataset are not in the NQ-open corpus. So we removed those questions and create a new development set: `orig_dev_converted_hasAnswerer.jsonl`
We have created a dictionary object (`dev_q_title_dict.pickle`) that map our devset questions to their answer document title.
You can generate the develpment set by:
```python
with open('orig_dev_converted_hasAnswerer.jsonl' , 'r') as f:
    lines = f.readlines()
with open('dev_q_title_dict.pickle' , 'rb') as f: #ref [2]
    q_title_dict = pkl.load(f)
    
dev_data = convertDataSetLinesToTraingData(lines , cursor_doc=cursor_doc , q_title_dict=q_title_dict)
with open('LCS_development_data.pickle' , 'wb') as f:
    pkl.dump(dev_data , f)
```
## Training the Model
Coming soon ...
## Prediction
Coming soon ...
