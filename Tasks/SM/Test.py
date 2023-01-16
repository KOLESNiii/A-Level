import random
EOS = EOS
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .,;'-"
letters = [letter for letter in letters]
word = ""
for i in range(7):
    word += random.choice(letters)
word += EOS
for i in range(2):
    word += random.choice(letters)
for char in word:
    print(char)