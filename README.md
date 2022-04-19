# Frozen-Phrases
Supporting matterial for the paper "Detecting Frozen Phrases in Open-Domain Question Answering"

## Data Generation
### Training and validation sets
We have generated our training and validation set from [NQ training set](https://ai.google.com/research/NaturalQuestions/download) (JSONL file)
training set: LCS_training_data.pickle
evaluation set: LCS_validation_data.pickle
You can simply use the `convertDataSetLinesToTraingData` function in alignment.py and pass it the lines of the jsonl file in a list:
```python
import alignment as alig
with open('v1.0-simplified_simplified-nq-train.jsonl' , 'r') as f:
    lines = f.readlines()
train_data = alig.convertDataSetLinesToTraingData(lines)
with open('LCS_training_data.pickle' , 'wb') as f:
    pkl.dump(train_data , f)
```

## Training the Model

## Prediction
Coming soon ...
