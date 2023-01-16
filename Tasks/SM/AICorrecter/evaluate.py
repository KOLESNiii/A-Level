import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from utils import CharacterTable, transform
from utils import restore_model, decode_sequences
from utils import read_text, tokenize
import pickle

error_rate = 0.6
reverse = True
model_path = './models/seq2seq.h5'
hidden_size = 512
sample_mode = 'argmax'

with (open("modelVariables.pickle", "rb")) as f:
        input_ctable, target_ctable, maxlen = pickle.load(f)
encoder_model, decoder_model = restore_model(model_path, hidden_size)
if __name__ == '__main__':
    while True:
        test_sentence = str(input(">>"))
        tokens = tokenize(test_sentence)
        tokens = list(filter(None, tokens))
        nb_tokens = len(tokens)
        misspelled_tokens, _, target_tokens = transform(
            tokens, maxlen, error_rate=error_rate, shuffle=False)
        
        
        
        input_tokens, target_tokens, decoded_tokens = decode_sequences(
            misspelled_tokens, target_tokens, input_ctable, target_ctable,
            maxlen, reverse, encoder_model, decoder_model, nb_tokens,
            sample_mode=sample_mode, random=False)
        
        print(' '.join([token for token in decoded_tokens]))
