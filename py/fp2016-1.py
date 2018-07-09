from math import sqrt, ceil

def gera_chave1(letras):
	res = []
	size = 5
	for i in range(0, size*size, size):
		res.append(letras[i:i+size])
	return tuple(res)

def obtem_codigo1(car, chave):
	for i in range(len(chave)):
		for j in range(len(chave[i])):
			if chave[i][j] == car:
				return str(i)+str(j)

def codifica1(cad, chave):
	res = ""
	for c in cad:
		res += obtem_codigo1(c, chave)
	return res

def obtem_car1(cod, chave):
	return chave[int(cod[0])][int(cod[1])]

def descodifica1(cad_codificada, chave):
	res = ""
	for i in range(0, len(cad_codificada), 2):
		res += obtem_car1(cad_codificada[i:i+2], chave)
	return res

def gera_chave2(letras):
	res = []
	tups = ceil(sqrt(len(letras)))
	l = ceil(len(letras)/tups)
	for i in range(tups):
		res.append(letras[(l*i):(l*(i+1))])
	return tuple(res)

def obtem_codigo2(car, chave):
	return obtem_codigo1(car, chave) or "XX"

def codifica2(cad, chave):
	res = ""
	for c in cad:
		res += obtem_codigo2(c, chave)
	return res

def obtem_car2(cod, chave):
	return "?" if (cod == "XX") else obtem_car1(cod, chave)

def descodifica2(cad_codificada, chave):
	res = ""
	for i in range(0, len(cad_codificada), 2):
		res += obtem_car2(cad_codificada[i:i+2], chave)
	return res
