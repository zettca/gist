N = 5

def iter_linear(l, c):
	return (l, c+1) if c < N-1 else (l+1, 0)

def get_init_dir(rot, p):
	if rot == "r":
		if p == (0, 0):
			return "R"
		if p == (0, N-1):
			return "D"
		if p == (N-1, N-1):
			return "L"
		if p == (N-1, 0):
			return "U"
	elif rot == "c":
		if p == (0, 0):
			return "D"
		if p == (0, N-1):
			return "L"
		if p == (N-1, N-1):
			return "U"
		if p == (N-1, 0):
			return "R"

def next_dir(rot, d):
	dirs = 'RDLU' if rot == 'r' else 'DRUL'
	return dirs[(dirs.index(d)+1)%len(dirs)]

def iter_spiral(d, l, c):
	if d == "L":
		return (l, c-1)
	if d == "R":
		return (l, c+1)
	if d == "U":
		return (l-1, c)
	if d == "D":
		return (l+1, c)

def order_msg(l, mgc):
	mgc_unique = ''
	l_restantes = ''.join(l)

	for c in mgc:
		if c == ' ': continue
		if c not in l: raise ValueError("invalid character")
		if c != ' ' and c not in mgc_unique:
			mgc_unique += c
			l_restantes = l_restantes.replace(c, '')
	return mgc_unique + l_restantes


# ========= #
#  POSICAO  #
# ========= #

# Construtores
def faz_pos(l, c):
	if l<0 or c<0:
		raise ValueError("invalid arguments")
	return (l, c)

# Seletores
def linha_pos(p):
	return p[0]
def coluna_pos(p):
	return p[1]

# Reconhecedores
def e_pos(arg):
	return type(arg) is tuple and len(arg) == 2 and all(isinstance(n, int) for n in arg) and all(n >= 0 for n in arg)

# Testes
def pos_iguais(p1, p2):
	return p1 == p2


# ======= #
#  CHAVE  #
# ======= #

# Construtores
def gera_chave_linhas(l, mgc):
	if set(l) != set('ABCDEFGHIKLMNOPQRSTUVWXYZ'):
		raise ValueError("invalid arguments")

	chave = [[[] for _ in range(N)] for _ in range(N)]

	p = (0, 0)
	for c in order_msg(l, mgc):
		pl, pc = linha_pos(p), coluna_pos(p)
		chave[pl][pc] = c
		p = iter_linear(pl, pc) # next position

	return chave


def gera_chave_espiral(l, mgc, s, pos):
	if set(l) != set('ABCDEFGHIKLMNOPQRSTUVWXYZ') or s not in ('r', 'c') or not e_pos(pos):
		raise ValueError("invalid arguments")

	chave = [[[] for _ in range(N)] for _ in range(N)]

	d = get_init_dir(s, pos)
	for c in order_msg(l, mgc):
		pl, pc = linha_pos(pos), coluna_pos(pos)
		chave[pl][pc] = c
		pos = iter_spiral(d, pl, pc) # get next position

		# look ahead
		pal, pac = linha_pos(pos), coluna_pos(pos)
		if pal < 0 or pac < 0 or pal > N-1 or pac > N-1 or chave[pal][pac]:
			d = next_dir(s, d)
			pos = iter_spiral(d, pl, pc) # get next position

	return chave

# Seletores
def ref_chave(c, p):
	return c[linha_pos(p)][coluna_pos(p)]

# Modificadores
def muda_chave(c, p, l):
	c[linha_pos(p)][coluna_pos(p)] = l
	return c

# Reconhecedores
def e_chave(arg):
	if type(arg) is not list: return False

	for linha in arg:
		if type(arg) is not list: return False
		for l in linha:
			if l not in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
				return False

	return True

# Transformadores
def string_chave(c):
	s = ''
	for linha in c:
		s += ' '.join(linha) + ' \n'
	return s

# ========= #
#  FUNCOES  #
# ========= #

def digramas(msg):
	dig = msg.replace(' ', '')
	i = 0

	while i < len(dig)-1:
		if dig[i] == dig[i+1]:
			dig = dig[:i+1]+'X'+dig[i+1:]
		i += 2

	return dig if len(dig)%2 == 0 else dig+'X'

def figura(digrm, chave):
	for i in range(len(chave)): # linhas
		if digrm[0] in chave[i] and digrm[1] in chave[i]:
			return ('l', faz_pos(i, chave[i].index(digrm[0])), faz_pos(i, chave[i].index(digrm[1])))

	chave_t = [[chave[j][i] for j in range(len(chave[i]))] for i in range(len(chave))]
	for i in range(len(chave_t)): # colunas (da transposta)
		if digrm[0] in chave_t[i] and digrm[1] in chave_t[i]:
			return ('c', faz_pos(chave_t[i].index(digrm[0]), i), faz_pos(chave_t[i].index(digrm[1]), i))

	res = ['r', None, None]
	for i in range(len(chave)): # rectangular
		for j in range(len(chave[i])):
			if chave[i][j] == digrm[0]:
				res[1] = faz_pos(i, j)
			elif chave[i][j] == digrm[1]:
				res[2] = faz_pos(i, j)
	return tuple(res)

def codifica_l(pos1, pos2, inc):
	return (faz_pos(linha_pos(pos1), (coluna_pos(pos1)+inc)%N),
			faz_pos(linha_pos(pos2), (coluna_pos(pos2)+inc)%N))

def codifica_c(pos1, pos2, inc):
	return (faz_pos((linha_pos(pos1)+inc)%N, coluna_pos(pos1)),
			faz_pos((linha_pos(pos2)+inc)%N, coluna_pos(pos2)))

def codifica_r(pos1, pos2):
	return (faz_pos(linha_pos(pos1), coluna_pos(pos2)),
			faz_pos(linha_pos(pos2), coluna_pos(pos1)))

def codifica_digrama(digrm, chave, inc):
	fig = figura(digrm, chave)
	if fig[0] == 'l':
		poss = codifica_l(fig[1], fig[2], inc)
	elif fig[0] == 'c':
		poss = codifica_c(fig[1], fig[2], inc)
	elif fig[0] == 'r':
		poss = codifica_r(fig[1], fig[2])

	return chave[linha_pos(poss[0])][coluna_pos(poss[0])] + chave[linha_pos(poss[1])][coluna_pos(poss[1])]

def codifica(mens, chave, inc):
	s = ''
	digrms = digramas(mens)
	for i in range(0, len(mens)-1, 2):
		digrm = digrms[i:i+2]
		s += codifica_digrama(digrm, chave, inc)
	return s
