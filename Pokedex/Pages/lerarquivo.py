def ler():
	i = 1;
	rf = open('pokedex.txt','w');
	while i<100:
		pokemon = ''
		if(i<10):
			file = 'page00'+str(i)+'.html';
		elif(i<100):
			file = 'page0'+str(i)+'.html';
		f = open(file,mode='r');
		pokemon += pegarNumero(f)+pegarNome(f) +'§'+pegarStats(f)+pegarTipos(f)+'§'+pegarHabilidades(f)+'§'+pegarCaractGerais(f);
		if(temMega(f)):
			print('TEEEEEEEEEEM MEEEEEEEGAAAAAAAAAAA')
		f.close();
		print(pokemon);
		rf.write(pokemon+'\n');
		i+=1;
	rf.close();

def pegarNumero(f):
	f.seek(0);
	num =''
	tabcorreta = '<td class="fooinfo" rowspan="3" align="center">'
	f = achar(f,tabcorreta)
	tabcorreta = '<td class="fooinfo">'
	f = achar(f,tabcorreta)
	f = achar(f,tabcorreta)
	f = achar(f,tabcorreta)
	for x in range(1,6):
		tabcorreta = '<b>'
		f = achar(f,tabcorreta)
		tabcorreta = '<td>'
		f = achar(f,tabcorreta)
		num += pegarValor(f,'<') + '§'
	return num
def pegarNome(f):
	f.seek(0);
	tabcorreta = '<td class="fooinfo" rowspan="3" align="center">'
	f = achar(f,tabcorreta)
	tabcorreta = '<td class="fooinfo">'
	f = achar(f,tabcorreta)
	return pegarValor(f,'<');

def pegarStats(f):
	f.seek(0);
	stats = '';
	tabcorreta = '<a name="stats">'
	f = achar(f,tabcorreta)
	tabcorreta = '<td align="center" class="fooinfo">'
	for x in range(1,7):
		f = achar(f,tabcorreta)
		stats+= pegarValor(f,'<')+'§';
	return stats;

def pegarTipos(f):
	f.seek(0);
	tipourl = '';
	tabcorreta = '<td class="cen">'
	f = achar(f,tabcorreta)
	tipourl = pegarValor(f,'>');
	tipo = trabalharUrl(tipourl)+'§';
	f = achar(f,'</a>');
	tipourl = pegarValor(f,'>');
	tipo += trabalharUrl(tipourl);
	return tipo;

def pegarHabilidades(f):
	f.seek(0);
	tabcorreta = '<td align="left" colspan="6" class="fooleft">'
	f = achar(f,tabcorreta)
	tabcorreta = '<b>';
	f = achar(f,tabcorreta)
	f = achar(f,tabcorreta)
	habilidade1 = pegarValor(f,'<');
	f = achar(f,tabcorreta)
	habilidade2 = pegarValor(f,'<');
	f = achar(f,tabcorreta);
	habilidade3 = pegarValor(f,'<');
	if(habilidade3 == habilidade1):
		return habilidade1+'§'+'§'+habilidade2;
	else:
		return habilidade1+'§'+habilidade2+'§'+habilidade3;

def pegarCaractGerais(f):
	f.seek(0);
	num =''
	tabcorreta = '<td class="cen">'
	f = achar(f,tabcorreta)
	tabcorreta = '<td class="fooinfo">'
	f = achar(f,tabcorreta)
	classif = pegarValor(f,'<');
	tabcorreta = '</td>'
	f = achar(f,tabcorreta)
	f.seek(f.tell()-13);
	altura = pegarValor(f,'<').lstrip()
	f = achar(f,tabcorreta)
	f.seek(f.tell()-13);
	peso = pegarValor(f,'<').lstrip()
	tabcorreta = '<td class="fooinfo">'
	f = achar(f,tabcorreta)
	taxaCaptura = pegarValor(f,'<');
	tabcorreta = '<td class="fooinfo">'
	f = achar(f,tabcorreta)
	passosOvos = pegarValor(f,'<');
	return classif+'§'+altura+'§'+peso+'§'+taxaCaptura+'§'+passosOvos
	
def temMega(f):
		f.seek(0);
		tabcorreta = '<a name="mega">'
		f = achar(f,tabcorreta);
		if f is not None:
			return 1;
		return 0;

def trabalharUrl(url):
	string = '';
	true = 1;
	false = 0;
	tipo = false;
	cont = 0;
	ponto = false
	for c in url:
		if (c == '/'):
			cont+=1;
		elif (c == '.'):
			ponto = true;
		elif (cont == 2 and ponto == false):
			string += c;
	return string.capitalize();

def achar(f,tabcorreta):
	string ='';
	true = 1;
	false = 0;
	c = f.read(1);
	abriu = false;
	while(c):
		if(abriu == false and c =='<'):
			abriu = true;
		elif (abriu == true and c == '>' ):
			abriu = false;
			string +=c;
			if(string == tabcorreta):
##				print(string)
				return f;
			string = '';
		if (abriu == true):
			string+=c;
		try:
			c = f.read(1);
		except UnicodeDecodeError:
			print('Erro estranho');


def achar2(text,tabcorreta):
	string ='';
	true = 1;
	false = 0;
	abriu = false;
	i = 0
	for c in text:
		if(abriu == false and c =='<'):
			abriu = true;
		elif (abriu == true and c == '>' ):
			abriu = false;
			string +=c;
			if(string == tabcorreta):
##				print(string)
				return i;
			string = '';
		if (abriu == true):
			string+=c;
		i+=1
			
def pegarValor(f,char):
	string ='';
	true = 1;
	false = 0;
	c = f.read(1);
	abriu = false;
	while(c!=char):
		string+=c;
		c = f.read(1);
	return string
