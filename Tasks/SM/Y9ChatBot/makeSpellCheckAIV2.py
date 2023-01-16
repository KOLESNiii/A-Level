# coding: utf-8

# In[1]:


import pandas as pd 
import os 
import numpy as np
from os import listdir
from os.path import isfile, join
import re
from sklearn.model_selection  import train_test_split
import io
from keras.callbacks import ModelCheckpoint


# In[2]:


def loading(path):
    input_file = os.path.join(path)
    with io.open(input_file, mode="r", encoding="utf-8") as f:
        data = f.read()
    return data


# In[3]:


path = './books/'
bookfiles = [f for f in listdir(path) if isfile(join(path, f))]
bookfiles = bookfiles[1:]


# In[6]:


books = []
for  i in bookfiles:
    books.append(loading( path+ i))


# In[7]:


books[0][:100]


# In[8]:


def clean_text(text):
    text = re.sub(r'\n', ' ', text)  # removing the /n from the above text 
    text = re.sub(r'[{}@_*>()\\#%+=\[\]]','', text) # removing the above seen \\  from the text 
    text = re.sub('a0','', text)
    text = re.sub('\'92t','\'t', text)
    text = re.sub('\'92s','\'s', text)
    text = re.sub('\'92m','\'m', text)
    text = re.sub('\'92ll','\'ll', text)
    text = re.sub('\'91','', text)
    text = re.sub('\'92','', text)
    text = re.sub('\'93','', text)
    text = re.sub('\'94','', text)
    text = re.sub('\.','. ', text)
    text = re.sub('\!','! ', text)
    text = re.sub('\?','? ', text)
    text = re.sub(' +',' ', text)
    return text


# In[9]:


book_clean = []
for i in books:
    book_clean.append(clean_text(i))


# In[10]:


# now see the clean text data 
book_clean[0][:100]


# In[11]:


vocab = {}
allowed = ['T', 'h', 'e', ' ', 'P', 'r', 'o',
          'j', 'c', 't', 'G', 'u', 'n', 'b', 'g', 'B', 'k', 
          'f', 'I', 'm', 'p', 'a', 'i', 'E', 's', ',', 'y', 
          'O', 'W', 'l', 'd', 'w', 'U', 'S', 'v', '.', 'Y', 
          '-', 'L', ':', 'A', 'C', 'R', 'D', 'M', '8', '1', 
          '9', '7', '4', 'F', '3', '2', '0', 'H', 'J', 'N', 
          'K', 'x', '5', 'V', 'q', '?', '—', '!', ';', 
          'z', 'æ', 'Q', '6', '/', '"', 'X', "'", '$']
count = 0 
for i in book_clean:
    for char in i :
        if char not in allowed:
            book_clean = book_clean.replace(char,'')
        if char not in vocab and char in allowed:
            vocab[char] = count
            count += 1           
vocab_size = len(vocab)
# In[12]:


#vocab


# In[13]:


codes = ['<PAD>','<EOS>','<GO>']
for code in codes:
    vocab[code] = count
    count += 1


# In[14]:


#vocab


# In[15]:


# now reversing the dictionary as 
int_vo ={}
for i,j in vocab.items():
    int_vo[j] = i


# In[16]:


#int_vo


# In[17]:


# extracting sentences from the bookclean
sentences = []
for i in book_clean:
    for sen in i.split('.'):
        sentences.append(sen + '.')
        


# In[18]:


#converting sentence into integer 
final_sentence = []
for i in sentences:
    b = []
    for  char in i :
        b.append(vocab[char])
    final_sentence.append(b)


# In[19]:


final_sentence[0] [:5]
# as in this assinging the values to the charcter in sentences


# In[20]:


# now dividing the  whole data set into train and test by using train test split
train , test =train_test_split(final_sentence , test_size = 0.25, random_state = 2)
#print(len(train))
#print(len(test))


# In[21]:


maxt = max([len(sentence) for sentence in train])
#print(maxt)


# In[22]:


# selecting the sentence between len of 10 to 300 as make training faster 
train_sort = []
min_length = 10 
max_length = 300
for i in range( min_length,max_length+2):
    for j in train:
        if (len(j) == i ):
            train_sort.append(j)


# In[23]:


maxt = max([len(sentence) for sentence in train_sort])
#print(maxt)


# In[24]:


# now we genrate noise in sentence 
letter =  ['a','b','c','d','e','f','g','h','i','j','k','l','m', 'n','o','p','q','r','s','t','u','v','w','x','y','z',]
def noise(sentence, threshold):
    noisy = []
    i = 0
    while i < len(sentence):
        rand = np.random.uniform(0,0.9,1)
        if rand < threshold:
            noisy.append(sentence[i])
        else:
            new_rand= np.random.uniform(0,0.9,1)
            if new_rand > 0.67:
                if i == (len(sentence) - 1):
                    continue
                else:
                    #noisy.append(sentence[i+1])
                    #noisy.append(sentence[i])
                    i += 1
            elif new_rand < 0.33:
                random_letter = np.random.choice(letter,1)[0]
                noisy.insert(vocab[random_letter])
                noisy.insert(sentence[i])
            else:
                pass     
        i += 1
    return noisy
   


# In[25]:


from random import randint
letter =  ['a','b','c','d','e','f','g','h','i','j','k','l','m', 'n','o','p','q','r','s','t','u','v','w','x','y','z',]
def nois(sentence, threshold):
    noisy = []
    i = 0
    while i < len(sentence):
        rand = np.random.uniform(0,0.9,1)
        if rand < threshold:
            noisy.append(sentence[i])
        else:
            random_letter = np.random.choice(letter,1)[0]
            a = vocab[random_letter]
            c = len(sentence)
            random_index = randint(0,c)
            #sentence[i] = a
            noisy.insert(random_index,a)
            
        i += 1
    return noisy
   


# In[26]:


#f = nois(train_sort[0],0.6)
#print(f)
#print(train_sort[0])


# In[27]:


#ef =  int_vo[5]
#print(ef)


# In[28]:


#b = []
#for i in train_sort[0:10]:
#    print(len(i))
    #b.append(noise(i,0.9))
#print(len(train_sort))   


# In[29]:


noisy_train = []
b= 0.9
for sentence in train_sort:
    f = nois(sentence,b)
    noisy_train.append(f)


# In[30]:


#for  i in noisy_train[:10]:
#    print(len(i))


# In[31]:


#maxt = max([len(sentence) for sentence in noisy_train])
#print(maxt)
#print(noisy_train[0])
#print(train_sort[0])


# In[32]:




# In[33]:


def pad_sentence(batch):
    """Pad sentences with <PAD> so that each sentence of a batch has the same length"""
    max_sentence = max([len(sentence) for sentence in batch])
    return [sentence + [vocab['<PAD>']] * (max_sentence - len(sentence)) for sentence in batch]


# In[34]:


pad_train= np.array(pad_sentence(train_sort))
pad_noisy_train = np.array(pad_sentence(noisy_train))


# In[35]:


print(pad_train[2].shape)
print(pad_noisy_train[2].shape)


# In[36]:
from keras.models import Sequential 
from keras.layers import LSTM, Dense, TimeDistributed



model = Sequential()
model.add(LSTM(40, return_sequences=True, input_shape=(None, 1)))
model.add(LSTM(20, return_sequences=True))
model.add(TimeDistributed(Dense(1, activation='sigmoid')))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['acc']) 
print(model.summary())



# In[37]:


from sklearn  import preprocessing
pd_train = preprocessing.normalize(pad_train)
pd_noisy_train = preprocessing.normalize(pad_noisy_train)
y = pd_train.shape

batch_size = 64
steps_per_epoch = len(pd_train) // batch_size

# In[40]:


a = pd_train.reshape(y[0],y[1],1)
#print(a[1][:10])


# In[42]:


# similarly with noise data 
z = pd_noisy_train.shape
b = pd_noisy_train.reshape(z[0],z[1],1)
#print(b[1][:10])


# In[ ]:


model.fit(a,b, batch_size=10, epochs=10, verbose=2)


# In[68]:


#  now similar whole procedure for testing data 


# In[ ]:


test_sort = []
min_length = 10 
max_length = 300
for i in range( min_length,max_length+2):
    for j in train:
        if (len(j) == i ):
            test_sort.append(j)


# In[ ]:


noisy_test = []
b= 0.9
for sentence in test_sort:
    f = nois(sentence,b)
    noisy_test.append(f)


# In[ ]:


pad_test= np.array(pad_sentence(test_sort))
pad_noisy_test = np.array(pad_sentence(noisy_test))


# In[ ]:


pd_test = preprocessing.normalize(pad_test)
pd_noisy_test = preprocessing.normalize(pad_noisy_test)
y = pd_test.shape
a1 = pd_test.reshape(y[0],y[1],1)
z = pd_noisy_test.shape
b1 = pd_noisy_test.reshape(z[0],z[1],1)



# In[ ]:


loss, acc = model.evaluate(a1, b1, verbose=0) 
print('Loss: %f, Accuracy: %f' % (loss, acc*100))


# In[ ]:

