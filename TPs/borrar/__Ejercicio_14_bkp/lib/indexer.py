# -*- coding: UTF-8 -*-


class Index(object):

    def __init__(self, tokenizer):
        self._tokenizer = tokenizer
        self._index = {}

    def index_str(self, str):
        'Actualiza el índice con la cadena pasada com parámetro.'
        tokens = self._tokenizer.tokenize(str)
        for term in tokens:
            self._index[term] = self._index.get(term, 0) + 1

    def iteritems(self):
        'Permite iterar en los elementos del índice.'
        return self._index.iteritems()

    def dict(self):
        'Devuelve el índice como un diccionario término:frecuencia.'
        return self._index


class Tokenizer(object):

    def __init__(self, stopwords):
        self._stopwords = stopwords
        self._substitutions = (
            u'áéíóúü\n\r\t()\{\}!¡?¿\'\"[]', u'aeiouu   '
        )

    def tokenize(self, str):
        '''Devuelve una lista de tokens normalizados.

        Los tokens son convertidos a minúscula, sin acentuación, etc.
        '''
        str = self._normalize(str)
        tokens = str.split(' ')
        tokens = map(lambda t: t.strip(), tokens)
        tokens = filter(lambda t: t, tokens)
        return tokens

    def _normalize(self, str):
        '''Devuelve la cadena str normalizada.

        La cadena es convertida a minúsculas, se eliminan los caracteres
        configurados en deletions y reemplaza las vocales acentuadas son
        reemplazadas por las mismas sin acento.
        '''
        str = str.lower()
        translation = dict(zip(
            map(ord, self._substitutions[0]),
            map(ord, self._substitutions[1])))
        str = str.translate(translation)
        return str
