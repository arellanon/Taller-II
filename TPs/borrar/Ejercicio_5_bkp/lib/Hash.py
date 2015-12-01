#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Crypto.Random
from Crypto.Cipher import AES
import hashlib
from Crypto.PublicKey import RSA

class Hash():
#Método generar_clave. Para generar la clave, la contraseña y la semilla se concatenan. Esta combinación se hashea tantas veces como sea solicitada.
   def generar_clave(self,clavePublica, semilla, iteraciones):
      assert iteraciones > 0 
      clave = clavePublica + semilla
      for i in range(iteraciones):
        clave = hashlib.sha256(clave).digest() #Funcion hash 
      return clave

#Método rellenar_texto. Toma como argumento el texto y el numero de multiplo  Rellena el texto con los bytes faltantes y lo retorna.
   def rellenar_texto(self,texto, multiplo):
     bytes_extra = len(texto) % multiplo
     tam_relleno = multiplo - bytes_extra
     relleno = chr(tam_relleno) * tam_relleno
     texto_rellenado = texto + relleno
     return texto_rellenado

#Método extraer_texto. Toma como argumento el texto rellenado y devuelve el texto normal sacando el relleno.
   def extraer_texto(self,texto_rellenado):
      tam_relleno = ord(texto_rellenado[-1])
      texto = texto_rellenado[:-tam_relleno]
      return texto

#Método cifrar. Toma como argumento el texto plano, la clave publica, el numero de semilla, el numero de iteraciones y el numero de multiplo. Devuelve el texto cifrado.
   def cifrar(self,textoPlano, clavePublica, semilla_tamano,num_iteraciones,aes_multiplo):
      semilla = Crypto.Random.get_random_bytes(semilla_tamano)
      clave = self.generar_clave(clavePublica, semilla, num_iteraciones)
      cifrador = AES.new(clave, AES.MODE_ECB)
      texto_rellenado = self.rellenar_texto(textoPlano, aes_multiplo)
      textoCifrado = cifrador.encrypt(texto_rellenado)
      textoCifradoSemilla = semilla + textoCifrado
      return textoCifradoSemilla

#Método descifrar descifrar. Toma como argumento el texto cifrado, la clave publica, el numero de semilla y el numero de iteraciones. Genera la clave para descifrar el texto. Retorna el texto plano
   def descifrar(self,textoCifradoSemilla, clavePublica,semilla_tamano,num_iteraciones):
      semilla = textoCifradoSemilla[0:semilla_tamano]
      textoCifrado = textoCifradoSemilla[semilla_tamano:]
      clave = self.generar_clave(clavePublica, semilla, num_iteraciones)
      cifrador = AES.new(clave, AES.MODE_ECB)
      texto_rellenado = cifrador.decrypt(textoCifrado)
      textoPlano = self.extraer_texto(texto_rellenado)
      return textoPlano
