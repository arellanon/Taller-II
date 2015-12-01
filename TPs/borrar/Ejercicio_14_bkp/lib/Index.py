#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tokenizer import Tokenizer

class Index():

    def indexar(self, str):
        index = {}
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(str)
        for term in tokens:
            index[term] = index.get(term, 0) + 1
        return index
