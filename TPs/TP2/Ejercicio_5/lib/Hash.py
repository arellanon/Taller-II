#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Crypto.Random
from Crypto.Cipher import AES
import hashlib
from Crypto.PublicKey import RSA

class Hash():
#Devuelve el texto cifrado.
    def cifrar(self, textoPlano, clavePublica, semilla_tamano, num_iteraciones, aes_multiplo):
        semilla = Crypto.Random.get_random_bytes(semilla_tamano)
        clave = self.gen_key(clavePublica, semilla, num_iteraciones)
        cifrador = AES.new(clave, AES.MODE_ECB)
        #padding
        tam_relleno = aes_multiplo - len(textoPlano) % aes_multiplo
        relleno = chr(tam_relleno) * tam_relleno
        texto_rellenado = textoPlano + relleno
        #cifrar
        textoCifrado = cifrador.encrypt(texto_rellenado)
        textoCifradoSemilla = semilla + textoCifrado
        return textoCifradoSemilla
      
#Retorna el texto plano
    def descifrar(self, textoCifradoSemilla, clavePublica, semilla_tamano, num_iteraciones):
        semilla = textoCifradoSemilla[0:semilla_tamano]
        clave = self.gen_key(clavePublica, semilla, num_iteraciones)      
        cifrador = AES.new(clave, AES.MODE_ECB)

        textoCifrado = textoCifradoSemilla[semilla_tamano:]
        #descifrar
        texto_rellenado = cifrador.decrypt(textoCifrado)
        textoPlano = texto_rellenado[:-ord(texto_rellenado[-1])]     
        return textoPlano

    def gen_key(self,clavePublica, semilla, iteraciones):
        assert iteraciones > 0 
        clave = clavePublica + semilla
        for i in range(iteraciones):
            clave = hashlib.sha256(clave).digest()
        return clave
