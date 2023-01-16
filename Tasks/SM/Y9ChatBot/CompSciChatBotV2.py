import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

#opening keyword and response data
with open("intents.json") as file:
    data = json.load(file)
#extracting data from JSON
try:
    with open("data.pickle", "rb") as f: #opening pickle file of variables
        words, labels, training, output = pickle.load(f)
except: #rebuilding variables if pickle file is not found
    words = []
    labels = []
    words_x = []
    words_y = []
    for intent in data["intents"]: #for type of question
        for pattern in intent["patterns"]: #for each keyword
            wrds = nltk.word_tokenize(pattern) #tokenize the keyword
            words.extend(wrds)
            words_x.append(wrds)
            words_y.append(intent["tag"]) #append the tag of the keyword
        if intent["tag"] not in labels: #append tag if not already in list
            labels.append(intent["tag"])
    
    words = [stemmer.stem(w.lower()) for w in words if w != "?"] #stems the keywords to their root
    words = sorted(list(set(words))) #removes duplicates and sorts alphabetically
    
    labels = sorted(labels)
         
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))] #makes empty array for output

    for x, doc in enumerate(words_x): #assembling training data array
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(words_y[x])] = 1 #sets the matching tag to 1, so model can match it to the correct response
        training.append(bag)
        output.append(output_row)
    #training, output get processed like the zip() function would, so the indexes of each list match
    training = numpy.array(training) #converting to numpy array
    output = numpy.array(output)
    
    with open("data.pickle", "wb") as f: #saves to pickle file as to not have to rebuild variables every time
        pickle.dump((words, labels, training, output), f)

#setting up neural network
tensorflow.compat.v1.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])]) #input layer
net = tflearn.fully_connected(net, 8) #two hidden layers, softmax activation function
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net) #output, gives a numerical value based on its predicted odds that the input corresponds to a certain tag

model = tflearn.DNN(net) #converts network into a model

try:
    model.load("model.tflearn") #tries to load
except: #if not possible, has to rebuilt model
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")
    model.load("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))] #empty array

    s_words = nltk.word_tokenize(s) #tokenizes input string
    s_words = [stemmer.stem(word.lower()) for word in s_words] #stems every word in input string
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1 #converts string to an array of 0s and 1s, where 1s represent the presence of a keyword
            
    return numpy.array(bag)


def main():
    debug = False
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("\n\nYou: ")
        if inp.lower() == "quit": #detection of commands
            break
        elif inp.lower() == "debug":
            debug = not debug
        results = model.predict([bag_of_words(inp, words)]) #gets prediction from model
        results_index = numpy.argmax(results) #returns highest possibility
        tag = labels[results_index]
        if numpy.max(results) < 0.55: #if the highest possibility is less than 55%, the model is not confident enough to give a response
            tag = "None"
        if debug: #prints debug info
            for i, value in enumerate(results[0]):
                print(str(i)+". "+ labels[i]+": " + str(value))
            print(results_index)
            print(tag)
        if tag == "None": #responses if model is not confident enough
            responses = [
                        "Please be clearer with your query",
                        "I do not understand your question", 
                        "I do not understand", 
                        "Please be more specific"
                         ]
            advice = ["This could be because:","You are misspelling to an extend that I cannot understand","You are asking questions about a topic I am not familiar with (I am a CompSci GCSE bot :D )","You are using vocabulary that I do not understand"]
            responses = [response + "\n" + "\n  ".join(advice) for response in responses]
        else:
            for tg in data["intents"]:
                if tg['tag'] == tag: #finds the response that matches the tag
                    responses = tg['responses']
        print("\n\nChatBot: "+random.choice(responses)) #prints random response from list of responses

main()
