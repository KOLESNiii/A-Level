import nltk
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

with open("intents.json") as file:
    data = json.load(file)
new = False
if new == True:
    with open("Spec.json") as file:
        spec = json.load(file)
    cleanSpec = []
    for line in spec:
        cleanSpec.append(line.strip("\n"))
    dataToAdd = {}
    tempKeyName = None
    tempKeyValue = None
    for line in cleanSpec:
        if line[1] == "." and line[3] == ".":
            if tempKeyName != None and tempKeyValue != None:
                dataToAdd.update({tempKeyName: tempKeyValue})
            tempKeyName = line
        if not line[0].isnumeric():
            tempKeyValue = line
    numericalLines = []
    for line in cleanSpec:
        if line[0].isnumeric():
            numericalLines.append(line)
    tempKeyName = "1.1 Systems architecture"
    tempKeyValue = []
    for line in numericalLines:
        if line == tempKeyName:
            pass
        elif line[:3] == tempKeyName[:3]:
            tempKeyValue.append(line)
        elif line[:3] != tempKeyName[:3]:
            dataToAdd.update({tempKeyName:"\n".join(tempKeyValue)})
            tempKeyName = line
            tempKeyValue = []
    for key, value in dataToAdd.items():
        if key[3] == " ":
            data["intents"].append({"tag": key, "patterns": [key, key[:3], key[4:], "What is in chapter "+key[:3]+"?", "Tell me about the "+key[4:]+" topic", "Topic "+key[:3], "What are the subtopics of topic "+key[:3]+"?"], "responses": [value+"\nfeel free to ask about any of these subtopics."]})
        else:
            data["intents"].append({"tag": key, "patterns": [key, key[:5], key[6:], "What is in chapter "+key[:5]+"?", "Tell me about the "+key[6:]+" topic", "Topic "+key[:5]], "responses": [value]})
    with open("intents.json", "w") as file:
        json.dump(data, file)
#extracting data from JSON
try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
        if intent["tag"] not in labels:
            labels.append(intent["tag"])
            
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    
    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.load("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])
        print(results)
        results_index = numpy.argmax(results)
        print(results_index)
        tag = labels[results_index]
        print(tag)

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        print(random.choice(responses))

chat()
