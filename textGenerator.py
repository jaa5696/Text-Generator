############################################################
# Imports
############################################################

import string
import random
import os
import math
import collections

############################################################
# Code
############################################################

def tokenize(text):
    for pun in string.punctuation:
        if pun in text:
            text = (" " + pun + " ").join(text.split(pun))
    return text.split()


def ngrams(n, tokens):
    ngram = []
    context = tokens.copy()
    for x in range(n-1):
        context.insert(0, "<START>")

    tokens.append("<END>")

    increment = 0

    for token in tokens:
        if n == 1:
            y = ()

        else:
            y = tuple(context[increment:(increment + n-1)])
            increment += 1

        ngram.append((y, token))
    return ngram


class NgramModel(object):

    def __init__(self, n):
        self.order = n
        self.n_grams = []
        self.ct_dict = collections.Counter()
        self.c_dict = collections.Counter()

    def update(self, sentence):
        tokens = tokenize(sentence)
        n_grams = ngrams(self.order, tokens)

        self.n_grams += [x for x in n_grams]

        for (x, y) in n_grams:
            self.ct_dict[x, y] += 1
            self.c_dict[x] += 1

    def prob(self, context, token):
        probability = self.ct_dict[context, token] / self.c_dict[context]
        return probability

    def random_token(self, context):

        prob_b = 0
        tokens = {t for (c, t) in self.n_grams if c == context}

        r = random.random()

        for token in sorted(tokens):

            prob_a = prob_b

            prob_b += self.prob(context, token)

            if prob_a <= r < prob_b:
                return token

        return "ERROR!"

    def random_text(self, token_count):
        i = 0
        sentence = ""
        context = self.n_grams[0][0]
        while i < token_count:
            word = self.random_token(context)
            sentence += word + " "
            i += 1
            if word == "<END>" or context == ():
                context = self.n_grams[0][0]
            else:
                con_list = list(context)
                con_list.pop(0)
                con_list.append(word)
                context = tuple(con_list)
        return sentence

    def perplexity(self, sentence):
        sum_p = 0
        m = 0
        tokens = tokenize(sentence)
        ngram = ngrams(self.order, tokens)

        for (context, token) in ngram:
            sum_p -= math.log(self.prob(context, token))
            m += 1

        print(m)
        perplex = pow(pow(math.e, sum_p), (1/m))
        return perplex


def create_ngram_model(n, path):
    x = NgramModel(n)
    file_path = os.path.join(os.getcwd(), path)
    with open(file_path, 'r', encoding='utf-8') as token_file:
        line = token_file.readline()
        while line:
            x.update(line)
            line = token_file.readline()
        token_file.close()
    return x

