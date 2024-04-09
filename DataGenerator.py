import random
import string
import pickle


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def shuffle_string(s):
    char_list = list(s)
    random.shuffle(char_list)
    shuffled_string = ''.join(char_list)
    return shuffled_string


def generateData():
    data = []
    initial_size = 10
    size = initial_size
    number_of_inputs = 1000
    for i in range(number_of_inputs):
        rep = random.randint(1, 100)
        match = generate_random_string(size)
        s = ''
        for j in range(rep):
            noise = generate_random_string(1) * random.randint(1, size)
            shuffledString = shuffle_string(match)
            s += shuffledString + noise
        size += 10
        data.append([match, s, rep])
    data.sort(key=lambda x: len(x[1]))
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)

