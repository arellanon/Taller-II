#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

def cronometro(funcion):
    def funcion_a_ejecutar(*argumentos):
        # Tiempo de inicio de ejecución.
        inicio = time.time()
        # Lanzamos función a ejecutar.
        ret = funcion(*argumentos)
        # Tiempo de fin de ejecución.
        fin = time.time()
        # Tiempo de ejecución.
        tiempo_total = fin - inicio
        # Devolvemos el tiempo de ejecución.
        return tiempo_total
    # Devolvemos la función que se ejecuta.
    return funcion_a_ejecutar
