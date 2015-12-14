#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Tokenizer():

    def tokenize(self, str):
        #Realiza el proceso de tokenizacion
        str = self.normalize(str)
        tokens = str.split(' ')
        tokens = map(lambda t: t.strip(), tokens)
        tokens = filter(lambda t: t, tokens)
        return tokens

    def normalize(self, str):
        #Normaliza el str
        str=unicode(str, 'utf-8')
        sustitucion = ( u'áéíóúü\n\r\t()\{\}!¡?¿\'\"[]', u'aeiouu   ' )
        str = str.lower()
        translation = dict(zip(
            map(ord, sustitucion[0]),
            map(ord, sustitucion[1])))
        str = str.translate(translation)
        return str
