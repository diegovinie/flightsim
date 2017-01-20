#! /usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Consta de funciones generadoras de terreno aleatorias. El terreno se almacena
en una lista donde cada posición es la coordenada x y cada dato la altura, esta
lista es la que interactuará con las aeronaves. Luego se crea una matriz donde 
los datos expresan el contorno del terreno y posteriormente son sustituidos por 
símbolos. Se debe utilizar una fuente monospace para que tengan coherencia el 
mapa.
'''

import random
import sys	


#-----GENERADOR DE TERRENO-----

def genTerr():
	w = 0	# Altura inicial es 0
	n = 60	# Tamaño del terreno
	terr = range(n)
	terr[1] = 0	# Se dejan los 2 primeros en 0 para que pueda despegar
	terr[2] = 0

	p = 3
	while p < n:
		R1 = random.randint(0,9)
		if 0 <= R1 < 3:
			w += 1
			if w > 4: w = 4
		elif 3 <= R1 < 7: pass
		else: w -= 1
		if w < 0: w += 1
				
		terr[p] = w 	
		p +=1
	return terr




#-----GENERADOR DE VISTA-------


def genMap(terr):
	M=[]
	filas = 6
	columnas = len(terr)
	for i in range (0,filas):
		M.append([' ']*columnas)	# vacia la matriz

	for j in range (0, 6):			# Genera el terreno	
		for i in range (0, len(terr)):
			if terr[i] == j:
				M[j][i] = '_'
	return M

def genMap2(terr):

	M=[]
	filas = 7
	columnas = len(terr)
	for i in range (0,filas):
		M.append([' ']*columnas)	# vacia la matriz

	for j in range (0, filas):			# Genera el terreno	
		for i in range (0, len(terr)):
			if terr[i] == j:
				M[j][i] = '_'

	for j in range (0, filas):
		for i in range (0, len(terr)):
			if (terr[i] > terr[i-1]) & (terr[i] == j):
				M[j-1][i-1] = '/'
#				M[j][i] = ' '
			elif (terr[i] < terr[i-1]) & (terr[i] == j):
				M[j][i-1] = '\\'
				M[j+1][i-1] = ' '			
			else: pass
	M[0][len(terr)-1] = ' '	# Problema de frontera

	return M

def printMap(M, terr):
	
	h0 = '  0_ '
	for i in range (0, len(terr)):
		h0 += '%s' % M[0][i]

	h1 = '100_ '
	for i in range (0, len(terr)):
		h1 += '%s' % M[1][i]

	h2 = '200_ '
	for i in range (0, len(terr)):
		h2 += '%s' % M[2][i]

	h3 = '300_ '
	for i in range (0, len(terr)):
		h3 += '%s' % M[3][i]

	h4 = '400_ '
	for i in range (0, len(terr)):
		h4 += '%s' % M[4][i]

	h5 = '500_ '
	for i in range (0, len(terr)):
		h5 += '%s' % M[5][i]

	h6 = '     '
	for i in range (0, len(terr)):
		h6 += '%s' % M[6][i]


	print '%s\n%s\n%s\n%s\n%s\n%s\n%s' % (h6, h5, h4, h3, h2, h1, h0)



