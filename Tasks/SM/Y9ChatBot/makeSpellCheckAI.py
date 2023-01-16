import numpy as np
import os
from os.path import isfile, join
import re
import io
import pandas as pd
from sklearn.model_selection import train_test_split

def load_book(path):
    input_file = os.path.join(path)
    print(input_file)
    with io.open(input_file, mode="r", encoding="utf-8") as f:
        data = f.read()
    return data

def clean_text(text):
    '''Remove unwanted characters and extra spaces from the text'''
    banned_chars = '[#$%+@<=>&,-:;()*^_`{|}~]'
    text = re.sub(r'\n', ' ', text) 
    text = re.sub('&', 'and', text)
    text = re.sub(r'[{}@_*>()\\#%+=\[\]]','', text)
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

class CharacterTable(object):
    """Given a set of characters:
    + Encode them to a one-hot integer representation
    + Decode the one-hot integer representation to their character output
    + Decode a vector of probabilities to their character output
    """
    def __init__(self, chars):
        """Initialize character table.
        # Arguments
          chars: Characters that can appear in the input.
        """
        self.chars = sorted(chars)
        self.char2index = dict((c, i) for i, c in enumerate(self.chars))
        self.index2char = dict((i, c) for i, c in enumerate(self.chars))
        self.size = len(self.chars)
    
    def encode(self, C, nb_rows):
        """One-hot encode given string C.
        # Arguments
          C: string, to be encoded.
          nb_rows: Number of rows in the returned one-hot encoding. This is
          used to keep the # of rows for each data the same via padding.
        """
        x = np.zeros((nb_rows, len(self.chars)), dtype=np.float32)
        for i, c in enumerate(C):
            try:
                x[i, self.char2index[c]] = 1.0
            except KeyError:
                print(f"KeyError: {c}")  
        return x

    def decode(self, x, calc_argmax=True):
        """Decode the given vector or 2D array to their character output.
        # Arguments
          x: A vector or 2D array of probabilities or one-hot encodings,
          or a vector of character indices (used with `calc_argmax=False`).
          calc_argmax: Whether to find the character index with maximum
          probability, defaults to `True`.
        """
        if calc_argmax:
            indices = x.argmax(axis=-1)
        else:
            indices = x
        chars = ''.join(self.index2char[ind] for ind in indices)
        return indices, chars

    def sample_multinomial(self, preds, temperature=1.0):
        """Sample index and character output from `preds`,
        an array of softmax probabilities with shape (1, 1, nb_chars).
        """
        # Reshaped to 1D array of shape (nb_chars,).
        preds = np.reshape(preds, len(self.chars)).astype(np.float64)
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probs = np.random.multinomial(1, preds, 1)
        index = np.argmax(probs)
        char  = self.index2char[index]
        return index, char

path = "./books/"
book_files = [f for f in os.listdir(path) if isfile(join(path, f))]
testing_book = ["19839.txt"]
for book in testing_book:
    book_files.remove(book)

books = []
for book in book_files:
    books.append(load_book(path+book))
clean_books = []
for book in books:
    clean_books.append(clean_text(book))

testing_books = []
for book in testing_book:
    testing_books.append(load_book(path+book))
clean_testing_books = []
for book in testing_books:
    clean_testing_books.append(clean_text(book))

sentences = []
for book in clean_books:
    for sentence in book.split('. '):
        sentences.append(sentence + '.')
print(f"There are {len(sentences)} sentences in the corpus.")
testing_sentences = []
for book in clean_testing_books:
    for sentence in book.split('. '):
        testing_sentences.append(sentence + '.')
print(f"There are {len(testing_sentences)} sentences in the testing corpus.")   

maxLength = 200
minLength = 5

validSentences = []
for sentence in sentences:
    if len(sentence) <= maxLength and len(sentence) >= minLength:
        validSentences.append(sentence)
valid_testing_sentences = []
for sentence in testing_sentences:
    if len(sentence) <= maxLength and len(sentence) >= minLength:
        valid_testing_sentences.append(sentence)

print(f"We will use {len(validSentences)} sentences to train our model.")
print(f"We will use {len(valid_testing_sentences)} sentences to test our model.")

SOS = "\t"
EOS = "*"
PAD = "*"
codes = [PAD, EOS, SOS]
def transform(sentences, maxLength, threshold=0.9, shuffle=True):
    if shuffle:
        np.random.shuffle(sentences)
    encoder_tokens = []
    decoder_tokens = []
    target_tokens = []
    for sentence in sentences:
        encoder = makeNoise(sentence, threshold)
        encoder = PadSentence([encoder], maxLength)[0]
        encoder_tokens.append(encoder)
        
        decoder = SOS + sentence
        decoder = PadSentence([decoder], maxLength)[0]
        decoder_tokens.append(decoder)
        
        target = decoder[1:]
        target = PadSentence([target], maxLength)[0]
        target_tokens.append(target)
    return encoder_tokens, decoder_tokens, target_tokens

letters = "abcdefghijklmnopqrstuvwxyz"
letters = [letter for letter in letters]
def makeNoise(sentence, threshold):
    noisySentence = []
    i = 0
    while i < len(sentence):
        random = np.random.uniform(0,1,1)
        if random < threshold:
            noisySentence.append(sentence[i])
        else:
            new_random = np.random.uniform(0,1,1)
            if new_random > 0.67:
                if i == (len(sentence) - 1):
                    continue
                else:
                    noisySentence.append(sentence[i+1])
                    noisySentence.append(sentence[i])
                    i += 1
            elif new_random < 0.33:
                randomLetter = np.random.choice(letters, 1)[0]
                noisySentence.append(randomLetter)
                noisySentence.append(sentence[i])
                i += 1
            else:
                pass
        i += 1
    return "".join(noisySentence)

def PadSentence(batch, maxLength):
    return [sentence + PAD * (maxLength - len(sentence)) for sentence in batch]

def batch(sentences, maxLength, ctable, batch_size=128, reverse=False):
    def generate(sentences, reverse):
        while True:
            for sentence in sentences:
                if reverse:
                    sentence = sentence[::-1]
                yield sentence
    
    sentence_iterator = generate(sentences, reverse)
    data_batch = np.zeros((batch_size, maxLength, ctable.size), 
                          dtype=np.float32)
    
    while True:
        for i in range(batch_size):
            sentence = next(sentence_iterator)
            data_batch[i] = ctable.encode(sentence, maxLength)
        yield data_batch

def dataGen(encoder_iterator, decoder_iterator, target_iterator):
    inputs = zip(encoder_iterator, decoder_iterator)
    while True:
        encoder_input, decoder_input = next(inputs)
        target = next(target_iterator)
        yield ([encoder_input, decoder_input], target)
        
def decode_sequences(inputs, targets, input_ctable, target_ctable,
                    maxLength, reverse, encoder_model,
                    decoder_model, number_samples, 
                    sample_mode='argmax', random=True):
    input_sentences = []
    target_sentences = []
    
    if random:
        indices = np.random.randint(0, len(inputs), number_samples)
    else:
        indices = range(number_samples)
        
    for index in indices:
        input_sentences.append(inputs[index])
        target_sentences.append(targets[index])
    input_sequences = batch(input_sentences, maxLength, input_ctable,
                            number_samples, reverse)
    input_sequences = next(input_sequences)
    
    states_value = encoder_model.predict(input_sequences)
    
    target_sequences = np.zeros((number_samples, 1, target_ctable.size))
    target_sequences[:, 0, target_ctable.char2index['\t']] = 1.0
    decoded_sentences = [""] * number_samples
    print(decoded_sentences)
    for _ in range(maxLength):
        char_probs, h, c = decoder_model.predict(
            [target_sequences] + states_value)
        
        target_sequences = np.zeros((number_samples, 1, target_ctable.size))
        
        sampled_chars = []
        for i in range(number_samples):
            if sample_mode == 'argmax':
                next_index, next_char = target_ctable.decode(
                    char_probs[i], calc_argmax=True)
            elif sample_mode == 'multinomial':
                next_index, next_char = target_ctable.sample_multinomial(
                    char_probs[i], temperature=0.5)
            else:
                raise Exception('Invalid sample mode: ' + sample_mode)
            decoded_sentences[i] += next_char
            sampled_chars.append(next_char)
            target_sequences[i, 0, next_index] = 1.0
        
        stop_char = set(sampled_chars)
        if len(stop_char) == 1 and stop_char.pop() == EOS:
            break
        states_value = [h, c]
    
    input_sentences = [re.sub(f'[{EOS}]', "", sentence) for sentence in input_sentences]
    target_sentences = [re.sub(f'[{EOS}]', "", sentence) for sentence in target_sentences]
    decoded_sentences = [re.sub(f'[{EOS}]', "", sentence) for sentence in decoded_sentences]
    return input_sentences, target_sentences, decoded_sentences

maxLength = max([len(sentence) for sentence in validSentences]) + 2
train_encoder, train_decoder, train_target = transform(
    validSentences, maxLength, threshold=0.9, shuffle=False)
input_chars = set(' '.join(train_encoder))
target_chars = set(' '.join(train_decoder))
nb_input_chars = len(input_chars)
nb_target_chars = len(target_chars)

testing_maxLength = max([len(sentence) for sentence in valid_testing_sentences]) + 2
testing_encoder, testing_decoder, testing_target = transform(
    valid_testing_sentences, maxLength, threshold=0.9, shuffle=False)

input_ctable = CharacterTable(input_chars)
target_ctable = CharacterTable(target_chars)
 





from keras.models import Sequential, Model
from keras.layers import LSTM, Dense, TimeDistributed, Bidirectional, DropoutWrapper, Input
from keras import optimizers, metrics, backend as K
import tensorflow as tf

def truncated_accuracy(y_true, y_pred):
    y_true = y_true[:, :16, :]
    y_pred = y_pred[:, :16, :]
    acc = metrics.categorical_accuracy(y_true, y_pred)
    return K.mean(acc, axis=-1)

def truncated_loss(y_true, y_pred):
    y_true = y_true[:, :16, :]
    y_pred = y_pred[:, :16, :]
    loss = K.categorical_crossentropy(target=y_true, output=y_pred,
                                      from_logits=False)
    return K.mean(loss, axis=-1)

epochs = 100
num_layers = 2
rnn_size = 512
embedding_size = 128
learning_rate = 0.0005
recurrrent_dropout = 0.2
keepProb = 0.2
sample_mode = "argmax"
reverse = True
test_batch_size = 256
train_batch_size = 128
training_steps = len(validSentences) // train_batch_size
testing_steps = len(valid_testing_sentences) // test_batch_size
model = Sequential()
encoder_inputs = Input(shape=(None, nb_input_chars), name='encoder_inputs')
encoder_LSTM = LSTM(rnn_size, recurrent_dropout=recurrrent_dropout,
                    return_state=False, return_sequences=True,
                    dtype=tf.float32, name='encoder_LSTM_1')
encoder_outputs = encoder_LSTM(encoder_inputs)

encoder_LSTM = LSTM(rnn_size, recurrent_dropout=recurrrent_dropout,
                    return_state=True, return_sequences=False,
                    name='encoder_LSTM_2')
outputs, state_h, state_c = encoder_LSTM(encoder_outputs)
encoder_states = [state_h, state_c]

decoder_inputs = Input(shape=(None, nb_target_chars), name='decoder_inputs')
decoder_LSTM = LSTM(rnn_size, dropout=keepProb,
                    return_state=True, return_sequences=True,
                    name='decoder_LSTM_1')
decoder_outputs, _, _ = decoder_LSTM(decoder_inputs,
                                     initial_state=encoder_states)
decoder_softmax = Dense(nb_target_chars, activation='softmax',
                        name='decoder_softmax')
decoder_outputs = decoder_softmax(decoder_outputs)

model = Model(inputs=[encoder_inputs, decoder_inputs],
              outputs=decoder_outputs)
adam = optimizers.Adam(lr=learning_rate, decay=0.0)
model.compile(optimizer=adam, loss='categorical_crossentropy',
              metrics=['accuracy', truncated_accuracy, truncated_loss])

encoder_model = Model(inputs=encoder_inputs, outputs=encoder_states)

# Define the decoder model separately.
decoder_state_input_h = Input(shape=(rnn_size,))
decoder_state_input_c = Input(shape=(rnn_size,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_LSTM(
    decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_softmax(decoder_outputs)
decoder_model = Model(inputs=[decoder_inputs] + decoder_states_inputs,
                        outputs=[decoder_outputs] + decoder_states)

print(model.summary())



for epoch in range(epochs):
    print(f"Main Epoch {epoch+1}/{epochs}")
    train_encoder, train_decoder, train_target = transform(
        validSentences, maxLength, threshold=0.9, shuffle=True)
    
    train_encoder_batch = batch(train_encoder, maxLength, input_ctable,
                                batch_size=train_batch_size,
                                reverse=reverse)
    train_decoder_batch = batch(train_decoder, maxLength, target_ctable,
                                batch_size=train_batch_size)
    train_target_batch = batch(train_target, maxLength, target_ctable,
                               batch_size=train_batch_size)
    
    testing_encoder_batch = batch(testing_encoder, maxLength, input_ctable,
                                batch_size=test_batch_size,
                                reverse=reverse)
    testing_decoder_batch = batch(testing_decoder, maxLength, target_ctable,
                                batch_size=test_batch_size)
    testing_target_batch = batch(testing_target, maxLength, target_ctable,
                                batch_size=test_batch_size)
    print("Finished batching")
    train_loader = dataGen(train_encoder_batch, train_decoder_batch,
                           train_target_batch)
    testing_loader = dataGen(testing_encoder_batch, testing_decoder_batch,
                          testing_target_batch) 
    print("Finished making generators")
    model.fit(train_loader, 
            steps_per_epoch=training_steps,
            epochs=1, verbose=1, 
            validation_data=testing_loader,
            validation_steps=testing_steps)
    
    number_sentences = 5
    input_sentences, target_sentences, decoded_sentences = decode_sequences(
        testing_encoder, testing_target, input_ctable, target_ctable, maxLength, reverse, 
        encoder_model, decoder_model, number_sentences, 
        sample_mode=sample_mode, random=True)
    
    print("-")
    print(f"Input sentences: {input_sentences}")
    print(f"Decoded sentences: {decoded_sentences}")
    print(f"Target sentences: {target_sentences}")
    print("-")
    
    model_file = "_".join(["epoch", str(epoch+1), "model.h5"])
    save_dir = "checkpoints"
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, model_file)
    print("Saving model to: ", save_path)
    model.save(save_path)
                                      
    
    




        
            
            
            
