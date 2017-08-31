#!/usr/bin/env python3

'''
Programme génétique pour définir un colloscope.
J'ai découvert la couche objet de python avec ce programme et l'ai écrit comme une preuve de concept au fur et à mesure de mes élucubrations.
Il est donc difficile à lire et mériterait maintenant une ré-écriture complète surtout pour quelqu'un qui a plus de recul sur les classes
Ceci dit il semble bien fonctionner chez moi.
Il est formé d'un seul script pour des raisons de simplification de diffusion et d'usage.
Le colloscope affiche à chaque génération une ligne avec les erreurs cummulées des 4 meilleurs colloscope."
'''

#####################################################################################
# VARIABLES A DEFINIR
# variables globales de définition collocope 
# Ces variables doivent correspondre au colloscope à définir et doivent donc être renseignées
# je les ai mises en tête de script pour qu'il n'y ait rien à modifier ensuite (sauf pour les plus aventureux)
#####################################################################################

#Le nombre de générations à produire 100 est rapide (mais certainement insuffisant). On peut aller à 1000 ou plus. Ce n'est pas parce que la génération semble se stabiliser qu'elle ne peut plus s'améliorer.
nbgen=100

#lm : la liste des matières
lm=["maths","phys","LVG1","LVG2","info"]

#nbl : le nombre de lignes = normalement le nombre de groupes sinon ça risque de donner n'importe quoi
nbl=14

#variable matp
'''matp : la liste des matières (celles de lm) avec leur TYPE et les PLAGES  horaires utilisées
Une plage horaire est formée d'un élément de j concaténé à un élément de h avec
j=["lu","ma","me","je","ve","sa"]
h=['8','9','10','11','12','13','14','15','16','17','18','19','20']
par exemple mercredi de 14 à 15 s'écrit me14
ATTENTION à définir le type t associé
	t est dans =[0,1,2,3,4]	#les types pour la matière
	t:type de matière
		0 si il y a une colle toutes les semaines dans cette matière
		1 si colle toutes les deux semaines
		2 si c'est une liste de groupe avec une colle toutes les semaines (non implémenté)
		3 si c'est une liste de groupe avec une colle toutes les semaines (non implémenté)
		4 si c'est une liste de groupe avec une colle une semaine sur 2 qui a une plage de deux heures --> info'''
#exemple pour une MPSI		
matp=[
["maths",0,['me16','ma15','ma12','me11','lu18','me18','lu18','ma17','me17','lu18','me12','ma12','me19','lu19']],
["phys",1,['ma15','ma15','je10','me17','ma17','ve17','ma15']],
["LVG1",1,['ma15','me16','me18','je18','me17']],
["LVG2",1,['lu19','lu18','lu19']],
#pour une matière de type 4 les plages de deux heures sont regroupées en liste
["info",4,[['je10','je11'],['je10','je11'],['je10','je11']]],
]

#noperm : pas de permutation : si une matière doit conserver les permutations du colloscope initial. Il n'y aura aucun changement dans les groupes pour ces matières par rapport au colloscope initial.
#pour l'instant non implementé
noperm=[]

#Les couples de matières pour lesquelles aucune vérification ne sera faite car les choix initiaux pour les groupes garantissent qu'il n'y aura pas de collisions dans ces matières (par exemple par des bons choix de parité des numéros de groupes dans le colloscope).
lib=[("phys","LVG1"),("phys","LVG2"),("info1","info2"),("info1","info3"),(("info2","info3"))]

########### passons aux groupes
#la liste des groupes
liste_groupe=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,14]
# la première ligne du colloscope
ligne1=[
["maths",[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,14]],
["phys", [1, 3, 5, 7, 9, 11, 13]],
["LVG1", [6,8,10,12,14]],
["LVG2", [2,4]],
["info", [[1, 2, 3, 9]]] #
]
# la deuxième ligne du colloscope
ligne2=[
["maths", [14,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]],
["phys",[2, 4, 6, 8, 10, 12, 14]],
["LVG1", [7,9,11,13]],
["LVG2",  [1,3,5]],
["info", [[4, 5, 6, 7, 8],[10, 11, 12, 13]]]
]

######### les contraintes supplémentaires (autre que les collisions inter-matières) qui seront calculées par le programme.
#attention toutes ne sont peut être pas encore implémentées

#cofo_p : contrainte forte par plage : plage dont les groupes explicités doivent être absent
cofo_p=[
['me11',[1,2,3,4,5]],
['me12',[1,2,3,4,5]],
]

#cofo_c : contrainte forte par colonne un élément de cette liste est de la forme 
# [matière,num_colonne_dans_la_matière,[groupes à éviter]]
# la première colonne est comptée avec le numéro 1 

#cofa_c : comme cofo_c mais c'est une contrainte faible, ce qui veut dire qu'on va simplement chercher à éviter ces groupes.
cofa_c=[
['maths',12 ,[4,5,12,13,14]],
['maths',13 ,[4,5,12,13,14]],
]

# plus généralement la liste des contraintes supplémentaires que l'on peut définir est 
#cofo_p=[] #liste des contraintes fortes définies par l'utilisateur pour une plage horaire
cofa_p=[] #liste des contraintes faibles définies par l'utilisateur pour une plage horaire
soufo_p=[] #liste des souhaits forts définis par l'utilisateur pour une plage horaire
soufa_p=[] #liste des souhaits faibles définis par l'utilisateur pour une plage horaire

#### contraintes et souhaits pour une colonne :
#### elt = classe Cdi ["nom_matiere",index de la matiere (en commencant par 0)),[liste groupe])
cofo_c=[] #liste des contraintes fortes définies par l'utilisateur pour une colonne
#cofa_c=[] #liste des contraintes faibles définies par l'utilisateur pour une colonne
soufo_c=[] #liste des souhaits forts définis par l'utilisateur pour une colonne
soufa_c=[] #liste des souhaits faibles définis par l'utilisateur pour une colonne


#### contrainte sur groupes fantômes pas encore implementées

#### plages horaire à éviter pour des groupes fantômes [liste de plages]
cofo_p_f=[] 
cofa_p_f=[] 
soufo_p_f=[]
soufa_p_f=[] 
#### colonnes souhaitées pour des groupes fantômes [nom de matière, numéro dans le collomètre en commencant à 0]
cofo_c_f=[] #contraintes fortes définies par l'utilisateur pour une colonne
cofa_c_f=[] #contraintes faibles définies par l'utilisateur pour une colonne
soufo_c_f=[] #souhaits forts définis par l'utilisateur pour une colonne
soufa_c_f=[] #souhaits faibles définis par l'utilisateur pour une colonne


############# FIN DES VARIABLES A DEFINIR ####################################################


#################################################################################################
#Le programme de colloscope en version ?ALPHA ?BETA
#################################################################################################
from itertools import *
import copy
import random

class Mbase():
	'''quelques méthodes de bases utiles'''
	def sub1(liste): 
		'''Programme récursif qui retranche 1 à tous les entiers présents dans la liste ainsi que toutes les sous-listes quelque soit le niveau'''
		if type(liste) == int:
			return(liste-1)
		if type(liste)== list:
			for (i,l) in enumerate(liste):
				nl=copy.deepcopy(l)
				liste[i]=Mbase.sub1(nl)
		return(liste)		

	def submat(liste): 
		'''Programme récursif qui ne conserve que les entiers et supprime tous les éléments chaînes de caractères présents dans la liste ainsi que toutes les sous-listes quelque soit le niveau'''
		if type(liste) == int:
			return(liste)
		elif type(liste)== list:
			for (i,l) in enumerate(liste):
				nl=copy.deepcopy(l)
				if type(nl)==str:
					del liste[i]
				else:	
					liste[i]=Mbase.submat(nl)
		return(liste)	

class MC(type):
	'''Une méta classe pour pouvoir mettre les variables globales données par l'utilisateur comme variables de la classe Ini'''
	def __init__(cls, name, bases, dict):
		super(MC, cls).__init__(name, bases, dict)

class Ini(metaclass=MC):
	'''initialisation des constantes globales dans la classe Ini (pour le futur ?).
	Ce sont toutes les constantes globales définies en début de programme qui caractérisent un colloscope (matières, plages etc) qu'on va initialiser comme constantes de classe dans Ini.
	fanto est la liste des groupes fantômes et sera créée avec le premier colloscope.
	On rajoute quelques méthodes pour récupérer des valeurs dans ces variables globales
	On garde le nom des variables globales du début.
	par exemple lm se récupère avec Ini.lm etc...
	Voir leur définition au début du programme.
	'''
			
	@classmethod
	def initpython(cls):
		''' initialisation des variables sans numéro de groupes'''
		for nom in ['lm','matp','nbl','noperm','lib']:
			#on récupère les valeurs avec le dictionnaire des variables globales
			setattr(MC, nom, globals()[nom])
			#super(MC, cls).__init__(name, bases, dict)
		''' initialisation des variables avec des numéros de groupes : on retranche 1 au numéro'''			
		for nom in ['liste_groupe','ligne1','ligne2','cofo_p','cofa_p','soufo_p','soufa_p','cofo_c','cofa_c','soufo_c','soufa_c','cofo_p_f','cofa_p_f','soufo_p_f','soufa_p_f','cofo_c_f','cofa_c_f','soufo_c_f','soufa_c_f']:
			#on récupère les valeurs avec le dictionnaire des variables globales et on retranche 1 au numéro de groupes avec sub1
			setattr(MC, nom, Mbase.sub1(globals()[nom]))
			#super(MC, cls).__init__(name, bases, dict)	

	def init(self):
		#si non définie, le nombre de lignes = nombre maximal de plage horaire
		if self.nbl<=0 and self.matp[0]!=0:
			self.nbl=max([len(elt[2]) for elt in self.matp])
		Ini.nbl=self.nbl	
		#soustraire 1 à tous les numéros de groupes
		
	@classmethod
	def plage_mat(cls,matiere):#retourne la liste des plages correspondant à une matière
		i=0
		while i<len(cls.matp) and matiere !=cls.matp[i][0] :
			i+=1
		if i==len(cls.matp):
			print("la matière ",matiere, "ne fait pas partie des matières\n")
		else:
			return(cls.matp[i][2:][0])
	@classmethod
	def num_mat(self,matiere):
		'''numéro de la matière dans le lm avec première matière num=0'''
		i=0
		while i<len(self.matp) and matiere !=self.matp[i][0] :
			i+=1
		if i==len(self.matp):
			print("la matière",matiere, "ne fait pas partie des matières\n")
		else:
			return(i)
	@classmethod	
	def type_mat(cls,matiere):
		'''retourne le type de matière : 0,1,2,3,ou 4'''
		i=0
		while i<len(cls.matp) and matiere !=cls.matp[i][0] :
			i+=1
		if i==len(cls.matp):
			print("la matière ",matiere, "ne fait pas partie des matières\n")
		else:
			return(cls.matp[i][1])		
	def verif_plage(L):
		pass
	def verif_index(L):
		pass	

class Coef():
	'''les coefficients de contraintes pour les calculs'''
	fo=500 #coeff fort
	fa=100 #coeff faible 
	fo_f=200
	fa_f=20
	doublon=100 #doublon (deux cases qui se suivent dans une colonne)
	rep=100	#mauvaise répartition d'un groupe dans une colonne (souvent impossible de faire mieux)
	#contrainte : coeff=plus
	#souhait: réalisé contrainte négative ?
	cofo_p=fo
	cofa_p=fa
	soufo_p=-fo 
	soufa_p=-fa 
	#### contraintes et souhaits pour une colonne :
	cofo_c=fo 
	cofa_c=fa
	soufo_c=-fo
	soufa_c=-fa
	### plages horaire à éviter pour des groupes fantômes [liste de plages]
	cofo_p_f=fo_f 
	cofa_p_f=fa_f
	soufo_p_f=-fo_f
	soufa_p_f=-fa_f
	### colonnes souhaitées pour des groupes fantômes [nom de matière, numéro dans le collomètre en commencant à 0]
	cofo_c_f=fo_f
	cofa_c_f=fa_f
	soufo_c_f=-fo_f
	soufa_c_f=-fa_f

class Collo():
	'''La classe collo pour colloscope, avec les différentes méthodes associées'''
	def __init__(self):
		self.c=[] #le tableau
		self.d={} #le dictionnaire calculé des pénalités
	
	def retd(collo):
		'''Décorateur retourne le dictionnaire si objet=collo'''
		def wrap(arg):
			#print(type(arg))
			if type(arg)!=dict:
				collo(arg.d)
		return wrap
	
	def retc(collo):
		'''Décorateur retourne le tableau collo'''		
		def wrap(arg):
			#print(type(arg))
			if type(arg)!=list:
				collo(arg.c)
		return wrap	

	#@retd
	#modifierle décorateur pour le return
	def jauge(self):
		'''une jauge pour évaluer le colloscope'''	
		return(sum([val for val in self.values()]))
		
	
	def csv(self):
		'''transformation en csv en retirant les groupes fantômes et en rajoutant 1 à tous les groupes'''
		C=self.c
		F=Ini.fanto
		texte=""
		for (numl,ligne) in enumerate(C):
			L=""
			L=str(numl+1)+";" #numéro de semaine +1
			for (numg,groupe) in enumerate(ligne):
				#print("Ini.matp[numg][1]",numg,groupe)
				if Ini.matp[numg][1] not in [2,3,4]: #pas regroupement de groupe
					#print("groupe",groupe)
					for val in groupe:
						if val in F:#groupe fantome
							L=L+";"
						else:
							L=L+str(val+1)+";"
				if Ini.matp[numg][1]==4: #regroupement de groupes dans les cases
					#print("groupe",groupe)
					for val in groupe: #val est une liste de groupes
						case=""
						#print("groupe",groupe)
						if val in F:#groupe fantome
							L=L+";"
						else:	
							for i in val:
								case=case+str(i+1)+','
							L=L+case[:-1]+";"	
					#L=L+case[:-1]+";" #enlever la dernière virgule
			texte=texte+L[:-1]+"\n" #enlever le dernier ; puis saut de ligne
		return(texte)
	
	@retc #pour récupérer le tableau (ou pas)
	def affiche(self):
		'''affiche un colloscope (au sens de python) ligne par ligne'''
		for ligne in self:
			print(ligne)

	def tri(self): #par coefficients décroissants
		return(sorted(self.d.items(), key=lambda t: t[1], reverse=True))			

	def termine(self):
		print("\n#######################\nLe colloscope :\n")
		self.affiche()
		print("\n#######################\nLe colloscope en csv :\n")
		print(self.csv())
		print("\n#######################\nDictionnaire des erreurs :")
		print("Le dictionnaire des erreurs affiche les cases du colloscope qui contiennent des erreurs.")
		print("Les cases sont triées de la plus grosse erreur à la plus petite.")
		print("Une case à la forme (ligne,matière,colonne dans la matière).")
		print("Les numéros de lignes sont au sens de python (première ligne : Num=0). Il faut donc rajouter 1, de même pour le numéro de matière et de colonne dans la matière.")
		print("Si il reste des cases de valeur supérieure à ",Coef.fo,",il se peut que le colloscope ne soit pas valide, mais cela peut aussi venir de multiples contraintes additionnées et il est difficile de faire mieux !\n")
		print(self.tri())
		

class Collo_init(Collo):
	'''Calcul du tout premier colloscope avec initialisation des groupes fantômes'''
	C=[] #on garde le tableau du colloscope initialisé comme variable de classe
	
	def creation_c(self):
		'''Création du tableau colloscope'''
		C=[]
		nbl=Ini.nbl #nbr ligne du colloscope
		lm=Ini.lm #liste des matière
		fanto=[] #pour créer les groupes fantômes. Cette liste peut contenir des valeurs de groupes ou bien des listes à un élément si la matière contient plusieurs groupes à coller par plages (par ex info)
		maxifanto=max(liste_groupe)
		if (set(lm) != {l[0] for l in ligne1})  :
			print("initialisation des groupes avec des matières autres que : ",lm )
			exit()
		for l in Ini.ligne1+Ini.ligne2:
			if Ini.type_mat(l[0])!=4: #type de matière normal
				nblf=(len(Ini.plage_mat(l[0]))-len(l[1])) #nbr de fantomes nécessaires
				if nblf>0:
					lfanto=[maxifanto+i+1 for i in range(nblf)] #liste des fantômes à rajouter
					l[1]=l[1]+lfanto
					maxifanto=lfanto[-1] #dernier élément
					fanto=fanto+lfanto
					#print("maxifanto",maxifanto)
			if Ini.type_mat(l[0])==4: #type à plage de deux heures on rajoute deux fois le groupe
				nblf=len(Ini.plage_mat(l[0]))-len(l[1]) #nbr de fantomes nécessaires
				#print("plage",Ini.plage_mat(l[0]),"len(l[1])",len(l[1]))
				if nblf>0:
					lfanto=[[maxifanto+i+1] for i in range(nblf)] #liste des fantomes à rajouter
					l[1]=l[1]+lfanto
					maxifanto=lfanto[-1][0]
					#print("maxifanto",maxifanto)
					fanto=fanto+lfanto
				#print("l1",l[1])	
		#la fabrication du groupe fantom est finie
		#on l'initialise dans la classe Ini
		Ini.fanto=fanto
		#suppression des string "matières" et adaptation pour colloscope
		cligne0,cligne1=[],[]
		def sub1(intouliste):
			if type(intouliste)==int:
				return(intouliste)
			if type(intouliste)==list:
				return([i for i in intouliste])
		for l in Ini.ligne1:	
			cligne0.append([sub1(i) for i in l[1]])
		for l in Ini.ligne2:
			cligne1.append([sub1(i) for i in l[1]])	
		C.append(cligne0)
		C.append(cligne1)
		#print("ligne0\n",cligne0,"\nligne1\n",cligne1,"\n\n")
		def perm_circ_d(NL):
			'''retourne la permutation circulaire (0 1 ... n-1) sur les éléments d'une ligne'''
			return NL[-1:]+NL[:-1]
		def ligne_suite():
			'''On teste une permutation de base'''
			ader_ligne=C[len(C)-2] # avant dernière ligne
			der_ligne=C[len(C)-1] #dernière ligne
			#print("ader_ligne",ader_ligne)
			#print("der_ligne",der_ligne)
			ligne=[] #la ligne à créer
			for (i,elt) in enumerate(Ini.matp):
				if elt[1]==0: #colle toutes les semaines
					ligne.append(perm_circ_d(der_ligne[i]))
				if elt[1]==1: #colle toutes les deux semaines 
					#simple permutation circulaire 
					ligne.append(perm_circ_d(ader_ligne[i]))
				if elt[1]==2: #on conserve le groupe der_ligne
					ligne.append(der_ligne[i])
				if elt[1]==3: #on conserve le groupe ader__ligne
					ligne.append(perm_circ_d(ader_ligne[i]))
				if elt[1]==4: #on conserve le groupe ader__ligne
					ligne.append(perm_circ_d(ader_ligne[i]))		
			#print(ligne,"\n")		
			C.append(ligne)		
		for i in range(nbl-2):
			ligne_suite()
		Collo_init.C=C #tableau du colloscope initial conservé comme variable de classe
		self.c=C
		print("\nColloscope de départ à optimiser :\n")
		self.affiche()
		print("\nLe même en csv : \n")
		print(self.csv())
		return(self)
	
	def creation_d(self):
		'''création du dictionnaire n'a de sens qu'après l'initialisation des groupes fantômes'''
		de=DE()
		self.d=de.calcul(self)
		return(self)

	def creation(self):
		'''Création du premier colloscope'''
		self.creation_c()
		#calcul de toutes les contraintes éventuellement dépendantes des groupes fantômes 
		cons=Cons()
		cons.contrainte()
		#puis calcul du dictionnaire des contraintes du premier colloscope
		self.creation_d()
		return(self)


class Cons():
	'''Calcul de la structure des contraintes : on calcul à l'avance un certain nombres de contraintes ce qui va nous donner tableaux et dictionnaires de contraintes '''
	
	###ATTENTION les contraintes sur les groupes fantômes ne sont pas encore gérées
	DC1={} 
	'''dictionnaire des contraintes de collisions entre plages identiques, un élément du dictionnaire est de la forme
	clef = ((i,j,k),(x,y,z)) avec i=ligne,j=matiere,k=num_plage_dans la matière
	valeur= le coefficient fort de collision à affecter aux deux cases du colloscope s'il y a collision des cases (i,j,k) et (x,y,z)'''
	DC2=[] 
	'''liste de toutes les contraintes du type liste de groupes à exclure ou favoriser dans la case
	un élément de la liste est de la forme ((i,j,k),[num des groupes], coeff)'''

	def entreplage(self):
		'''fabrique DC1 le dictionnaire des collisions par plage de matières'''
		lcomp=list(combinations(enumerate(Ini.lm),2))
		lverif=[] #matière à comparer entre elle : par ex lverif= [((0, 'maths'), (1, 'phys')),....]
		#on ne compare pas les matières qui sont données comme n'étant pas à comparer (par exemple choix de numéro pair/imapir sans collisions possibles)
		for elt in lcomp:
			if {elt[0][1],elt[1][1]} not in [set(c) for c in Ini.lib]:
				lverif.append(elt)
		#reste à comparer les plages pour chaque matière dans lverif, avec la subtilité des plages de type info (plage = liste de deux heures)
		#print("lverif\n",lverif)
		coeff=Coef.fo #coefficient fort
		#et on ne va pas optimiser ici avec les intersections ça n'est fait q'une fois et c'est pas gros!
		L=[] #les intersections sur la ligne
		for co_ind_mat in lverif: #couple indice matière
			mat1,mat2=co_ind_mat[0][1],co_ind_mat[1][1]
			#print("mat1mat2",mat1,mat2)
			lplage1=Ini.plage_mat(mat1) #liste des plages
			num1=Ini.num_mat(mat1) #numéro de la matière
			tipe1=Ini.type_mat(mat1)
			lplage2=Ini.plage_mat(mat2)
			tipe2=Ini.type_mat(mat1)
			num2=Ini.num_mat(mat2)
	
			#print("plage",lplage1,lplage2)
			def egal(plage1,plage2): #les plages se rencontre-telle	(cas de plage = listes de plage)
				if type(plage1)==str and type(plage2)==str:
					return (plage1==plage2)
				if type(plage1)==str and type(plage2)==list:
					return (plage1 in plage2)
				if type(plage1)==list and type(plage2)==str:
					return (plage2 in plage1)
				if type(plage1)==list and type(plage2)==list:
					return((set(plage1) | set(plage2)) == set())
				#pour chaque plage on cherche les indices de plages communes
				#mais on forme un couple en rajoutant le numéro de matière concernée
				#LI1=[(num1,ind) for ind,pl in L1 if pl==plage] #[ind,plage] 
			L1=[[ind,plage] for ind,plage in enumerate(lplage1)]
			L2=[[ind,plage] for ind,plage in enumerate(lplage2)]
			#print(list(product(L1,L2)))
			#print("avant égal plage")
			#L=[((num1,ind1),(num2,ind2)) for ((ind1,pl1),(ind2,pl2)) in product(L1,L2)]
			#print(L)
			#print("après égal plage")
			L=L+[((num1,ind1),(num2,ind2)) for ((ind1,pl1),(ind2,pl2)) in product(L1,L2) if egal(pl1,pl2)]
			#print(L)
			#print(list(product(list(range(Ini.nbl)),L)))
		lcomplete=[((nl,num1,ind1),(nl,num2,ind2)) for (nl,((num1,ind1),(num2,ind2))) in product(list(range(Ini.nbl)),L)]
		#print(L)
		#print(lcomplete)
		for elt in lcomplete:
			self.DC1[elt]=coeff
		#print(ltriple)
		#print(len(ltriple))
		#print(len(set(ltriple)))#pas de redondance
		#print("DC1",len(self.DC1),"\n",self.DC1)
		
	def contrainte_plage(self):
		'''Calcul de la liste de contraintes pour des groupes à exclure ou à souhaiter sur une plage horaire et insertion dans DC2'''
		lc=[Ini.cofo_p,Ini.cofa_p,Ini.soufo_p,Ini.soufa_p,Ini.cofo_p_f,Ini.cofa_p_f,Ini.soufo_p_f,Ini.soufa_p_f]
		#liste des coeffs correspondants
		lcoef=[Coef.cofo_p,Coef.cofa_p,Coef.soufo_p,Coef.soufa_p,Coef.cofo_p_f,Coef.cofa_p_f,Coef.soufo_p_f,Coef.soufa_p_f]
		for i in range(len(lc)):
			liste=lc[i] #ex : liste = [['me11',[1,2,3,4,5]],['me12',[1,2,3,4,5]]]
			coeff=lcoef[i]
			#print(liste)
			for (plage,lgroupe) in liste:
				#ex: plage='me11' lgroupe=[1,2,3,4,5]
				#print("plage","lgroupe",(plage,lgroupe))
				for mtp in Ini.matp: #cherchons cette plage partout
					mat,t,gplage=mtp[0],mtp[1],mtp[2]
					num_mat=Ini.num_mat(mat)
					lplage=Ini.plage_mat(mat) #liste des plages de la matière mat
					lip=list(enumerate(lplage)) #la même avec index 
					#print("lip",lip,"plage",plage)
					#liste_index = liste des index concernés par une plage pour une matière
					liste_index=[i for (i,m) in lip if m==plage] 
					if liste_index!=[]:
						#print("liste_index",liste_index)
						lnbl=list(range(Ini.nbl)) #liste des lignes
						triple=list(product(lnbl,[num_mat],liste_index)) #les triplets à contrainte 
						self.DC2=self.DC2+[(tri,lgroupe,coeff) for tri in triple]
		#print("DC2_entreplage\n",self.DC2,len(self.DC2))
		
	def contrainte_col(self):
		'''Comme contrainte_plage mais cette fois-ci avec des contraintes sur des colonnes
		On continue à insérer dans DC2'''
		lc=[Ini.cofo_c,Ini.cofa_c,Ini.soufo_c,Ini.soufa_c,Ini.cofo_c_f,Ini.cofa_c_f,Ini.soufo_c_f,Ini.soufa_c_f]
		#liste des coeffs correspondants
		lcoef=[Coef.cofo_c,Coef.cofa_c,Coef.soufo_c,Coef.soufa_c,Coef.cofo_c_f,Coef.cofa_c_f,Coef.soufo_c_f,Coef.soufa_c_f]
		for i in range(len(lc)):
			liste=lc[i] #ex : liste =[['maths',12 ,[4,5,12,13,14]],['maths',13 ,[4,5,12,13,14]]]
			coeff=lcoef[i]
			#print(liste)
			for (mat,index,lgroupe) in liste:
				num_mat=Ini.num_mat(mat)
				lnbl=list(range(Ini.nbl)) #liste des lignes
				triple=list(product(lnbl,[num_mat],[index])) #les triplets à contrainte 
				self.DC2=self.DC2+[(tri,lgroupe,coeff) for tri in triple]
				#print([(tri,lgroupe,coeff) for tri in triple])
		#modification de la variable de classe			
		Cons.DC2=self.DC2 #tordu mais initialise la variable de classe DC2!!!! 	
		#print("DC2_entre_plage_et_contrainte_col\n",self.DC2,len(self.DC2))
		
	def contrainte(self):
		'''calcul de toutes les contraintes'''
		self.entreplage()
		self.contrainte_plage()
		self.contrainte_col()
		return(self)

class Mutation(Collo):
	'''Différentes mutations à partir d'un colloscope de base'''
	
	def __init__(self,collo):
		self.c=copy.deepcopy(collo.c)
		self.d=collo.d
	
	def colonne(self,coord):
		'''retourne les éléments d'une colonne définie par ses coordonnées  (i,j) et la renvoie dans une liste'''
		(i,j)=coord
		#print(len(self))
		return([self.c[num][i][j] for num in range(len(self))])

	def transpose(self,triple): #on transpose aléatoirement avec le triplet (ligne,groupe,case)
		(l,g,c)=triple
		ind=random.randint(0,len(self.c[l][g])-1)
		#print((l,g,c),(l,g,ind))
		(self.c[l][g][ind],self.c[l][g][c])=(self.c[l][g][c],self.c[l][g][ind])
	
	def mutation_deb_ligne(self):
		'''On trie la liste des coefficients associés au colloscope par coefficients décroissants. On prend un certain nombre de valeurs aléatoires dans la première partie de cette liste puis on en extrait un petit nombre aléatoire qui correspond à des lignes toutes différentes, puis on transpose les cases correspondantes dans leur matière''' 
		nb_modif=random.randint(0,7)
		nb_max_coeff=10
		subdi=2 #le nombre de subdivisions : on prendra la première qui a les plus gros coeffs
		#Les plus gros coefficients dans l'ordre décroissants
		L=sorted(self.d.items(), key=lambda t: t[1], reverse=True) #liste avec elt  ((1, 0, 3), 500)
		#print("L",L[:30])
		if len(L)<4:
			self.termine(L)
		i=random.randint(0,len(L)//subdi) #on prend un nombre dans les gros coeffs
		ldic=[L[i][0]]  #on ajoute les coordonnées 
		lnuml=[L[i][0][0]] #numéro de ligne correspondant
		j=0
		while len(ldic)<nb_modif and j<3*nb_modif:
			i=random.randint(0,len(L)//subdi)
			j+=1
			numl=L[i][0][0]
			#print(L[i][0])
			if numl  not in lnuml:
				ldic.append(L[i][0])
				lnuml.append(numl)
		#maintenant la liste des cases à changer est dans ldic
		#application des transpositions (aléatoires)
		#print("ldic",ldic);
		for triple in ldic:
			self.transpose(triple)
		#print("Lchang",Lchang)
		de=DE()
		self.d=de.calcul(self)
		return(self)		

	def mutation_sur_ligne(self):
		'''On prend les plus gros coeffs de lignes qui sont choisies au hasard et c'est eux qu'on bouge''' 
		#print("entrée dans mutation",self.c,self.d)
		#print("self.c",self.c)
		nb_modif=random.randint(1,5)
		lnumli=[random.randint(0,len(self.c)) for i in range(nb_modif)] #on se force à toucher toutes les lignes
		#mais toute distincte
		#Classer par ordre de coeff croissant
		L=sorted(self.d.items(), key=lambda t: t[1], reverse=True) #liste avec elt  ((1, 0, 3), 500)
		print("L",L[:100])
		#L[0][0] donne le numéro d'une ligne i et on veut que i parcourt lnumli
		SL=[] #la liste des coordonnées faite à partir des éléments de L qu'on prend (au moins 1)
		while len(lnumli)>0 and len(L)>0:
			elt=L.pop(0) 
			if elt[0][0] in lnumli: 
				#print(lnumli,elt[0][0])
				SL.append(elt[0]) #on le prend
				lnumli.remove(elt[0][0])
		print("SL",SL)
		if len(L)==0:
			print(L)
			self.affiche()
			print("terminé")
			exit()
		#print("ldic",ldic);
		def transpose(triple): #on transpose aléatoirement avec le triplet (ligne,groupe,case)
			(l,g,c)=triple
			ind=random.randint(0,len(self.c[l][g])-1)
			#print((l,g,c),(l,g,ind))
			(self.c[l][g][ind],self.c[l][g][c])=(self.c[l][g][c],self.c[l][g][ind])
		for triple in SL:
			transpose(triple)
		de=DE()
		self.d=de.calcul(self)
		return(self)

	def mutation_minus_gros(self):
		'''On prend les plus gros coeffs de lignes qui sont choisies au hasard et c'est eux qu'on bouge''' 
		#print("entrée dans mutation",self.c,self.d)
		#print("self.c",self.c)
		nb_modif=random.randint(1,7) #le nombre de modification

		#Classer par ordre de coeff croissant
		L=sorted(self.d.items(), key=lambda t: t[1], reverse=True) #liste avec elt  ((1, 0, 3), 500)
		#print("L",L[:100])
		#L[0][0] donne le numéro d'une ligne i et on veut que i parcourt lnumli
		SL=[] #la liste des coordonnées faite à partir des éléments de L qu'on prend (au moins 1)
		lnumli=[] #liste des numéro de lignes
		while len(SL)<nb_modif and len(L)>0:
			elt=L.pop(0)
			if elt[0][0] not in lnumli: #si on n'a pas encore touché la ligne
				#print(lnumli,elt[0][0])
				SL.append(elt[0]) #on le prend
				lnumli.append(elt[0][0])
		#print("SL",SL)
		if len(L)==0:
			print(L)
			self.affiche()
			print("terminé")
			exit()
		#print("ldic",ldic);
		def transpose(triple): #on transpose aléatoirement avec le triplet (ligne,groupe,case)
			(l,g,c)=triple
			ind=random.randint(0,len(self.c[l][g])-1)
			#print((l,g,c),(l,g,ind))
			(self.c[l][g][ind],self.c[l][g][c])=(self.c[l][g][c],self.c[l][g][ind])
		for triple in SL:
			transpose(triple)
		de=DE()
		self.d=de.calcul(self)
		return(self)		

	def croisement(self,collo):
		'''renvoie un colloscope issu par croisement sur les lignes (mais il faut garder la parité)
		Autant croiser les paires et les impaires'''
		for i in range(0,Ini.nbl,2):
			self.c[i]=collo.c[i]
		de=DE()
		self.d=de.calcul(self)
		return(self)


class DE(dict): 
	'''Dictionnaire des Erreurs:
	une classe dictionnaire pour comptabiliser les erreurs dans une instance de colloscope
	les éléments du dictionnaire sont de la forme ((numligne,groupe,num_groupe),coeff) avec coeff le coefficient d'erreur relatif à la case (numligne,groupe,num_groupe),coeff) du collomètre on y ajoute les méthodes de calculs
	Finalement le dictionnaire sera initialisé avec l'objet colloscope. On ne garde que les méthodes de calcul'''
	__slots__ = ()
	
	def ajout(self,coord,penal):
		'''ajout d'une pénalité à la place coord on ajoute pas si penal ==  0'''
		if penal !=0:
			if coord in self.keys():
				self[coord]+=penal
				return(self)
			else:
				self[coord]=penal
				return(self)

	#@Collo.retd
	def jauge(self):
		return(sum([val for val in self.values()]))
	
	#@Collo.retd
	def tri(self): #par coefficients décroissants
		return(sorted(self.d.items(), key=lambda t: t[1], reverse=True))


	def calculDC1(self,col):
		'''calcul des contraintes à partir de DC1. col est la liste colloscope'''
		dc1=Cons.DC1
		#print("dc1",)
		def egal(coord1,coord2): 
			if type(coord1)==int and type(coord2)==int:
				return (coord1==coord2)
			if type(coord1)==int and type(coord2)==list:
				return (coord1 in coord2)
			if type(coord1)==list and type(coord2)==int:
				return (coord2 in coord1)
			if type(coord1)==list and type(coord2)==list:
				return((set(coord1) | set(coord2)) == set())
		for ((coord1,coord2),coeff) in dc1.items():
			(i,j,k)=coord1;(x,y,z)=coord2
			if egal(col[i][j][k],col[x][y][z]):
				self.ajout(coord1,coeff)
				self.ajout(coord2,coeff)
		#print("contrainte DE\n", self)
		#print(len(self))
		return(self)
	
	def calculDC2(self,col):
		'''calcul des contraintes à partir de DC2. col est la liste colloscope'''
		dc2=Cons.DC2
		#print("dc2",dc2)
		def appartient(case,lg):#lg est une liste de groupe, case est un groupe ou une liste
			if type(case)==int:
				return(case in lg)
			if type(case)==list:
				return((set(case)|set(lg)) == set())
		for (coord,lg,coeff) in dc2:
			(i,j,k)=coord
			#print("coord,case,lg,coeff",(i,j,k),collo[i][j][k],lg,coeff)
			if appartient(col[i][j][k],lg):
				#print("collision")
				self.ajout(coord,coeff)
		#print("contrainte après DC2\n",self)
		#print(len(self))
		return(self)

	def calculcol(self,C):
		'''Calcul par colonne : ici C est la liste colloscope. On  essaye d'avoir la meilleure répartition des groupes dans une colonne et on évite deux groupes qui collent deux fois de suite successivement = deux numéros qui se suivent
		Bien sûr on ne travaille pas sur des colonnes qui contiennent des groupes'''
		lnmat=[nmat for (nmat,elt) in enumerate(Ini.matp) if elt[1] in [0,1]] #les matières concernées données par numéro
		def coeff(case,casevois,col,fas):
			'''le coefficient à calculer pour case, étant donné une case, une autre case, une colonne, et la fréquence d'apparition souhaitée'''
			coef=0
			if case==casevois:
				coef+=Coef.doublon
			co=col.count(case)
			coef+=Coef.rep*max(co-fas,fas-co)
			return coef	
		def nb_gr_par_mat(nmat):
			if Ini.matp[nmat][1]==0: #math en mpsi
				return(len(Ini.matp[nmat][2]))
			if Ini.matp[nmat][1]==1: #phys ou langue
				return(2*len(Ini.matp[nmat][2]))
			if Ini.matp[nmat][1]==4: #info
				return(2*len(Ini.matp[nmat][2]))
		for nmat in lnmat:
			fas=int((Ini.nbl/nb_gr_par_mat(nmat))+0.5) #fréquence d'apparition souhaitée pour un groupe
			#on veut donc que la fréquence d'apparition soit fas ou fas+1
			for ncol in range(len(C[0][nmat])):
				col=[C[nl][nmat][ncol] for nl in range(Ini.nbl)] #colonne du colloscope à [nmat][ncol]
				#traitement de la première case
				coef=coeff(col[0],col[1],col,fas)
				coord=(0,nmat,ncol)
				self.ajout(coord,coef)
				#puis des suivantes
				casepre=col[0]
				for nl in range(1,Ini.nbl):
					case=col[nl]
					coord=(nl,nmat,ncol)
					self.ajout(coord,coeff(case,casepre,col,fas))
					casepre=case
		return(self)
			
		
	def calcul(self,collo):
		self.calculDC1(collo.c)
		self.calculDC2(collo.c)
		self.calculcol(collo.c)
		return(self)

class Gene():
	'''Il faut garder de la diversité sinon la liste générée se stabilise trop.
	A partir du colloscope initial : 4 mutations puis 4 mutations puis 4 mutations --> 256
		- on garde les 4 meilleurs :4
		- croisements entre eux : 6
		- 4 mutations chacun : 16
		- croisements des 4 meilleurs avec 32 autres : 128
		- 1 mutation des autres pris aléatoirement : 75
		- encore des mutations du colloscope initial : 27
		- on recommence un certain nombre de fois'''
	nb_genera=500
	nb_select=200
	def generation(self,colo,nb=nb_genera):
		'''renvoie une liste de nb_genera colloscopes mutés à partir de colo'''
		LC=[]
		if len(colo.d)==0:
			colo.termine()
		for i in range(nb):
			ncollo=Mutation(colo)
			LC.append(ncollo.mutation_deb_ligne())
		return(LC)
	
	
	def selection(self,LC,maxi=nb_select):
		'''On prend les meilleurs d'une liste de colloscope
		on retourne un liste avec les meilleurs puis une deuxième liste avec les autres'''
		nb=min(maxi,len(LC))
		#print(type(LC[0]))
		#exit()
		NL=sorted(LC,key= lambda collo: collo.d.jauge())
		return(NL[0:maxi],NL[maxi:])
	
	def generation1(self,colo,n=4):	
		'''Première génération'''
		LC=self.generation(colo,n)
		NLC=[]
		for colo in LC:
			NLC=NLC+self.generation(colo,n)
		NNLC=[]
		for colo in NLC:
			NNLC=NNLC+self.generation(colo,n)
		return(NNLC) #n=4 --> 64 colloscopes retournés	
		
	def evolution(self,colo,n):
		LC=self.generation1(colo,4) #on en récupère 256 : première génération
		(L4,Lautr)=self.selection(LC,4) #les 4 meilleurs et les autres (triés)
		for i in range(n):
			NL=copy.deepcopy(L4) #les 4 meilleurs à garder
			#mutation des 4 meilleurs
			for col in L4:
				NL=NL+self.generation(col,4)
			#croisement des 4 meilleurs
			for col1,col2 in combinations(L4,2):
				NL=NL+[col1.croisement(col2)]
			#croisement des 4 meilleurs avec des autres	
			#random.shuffle(Lautr) #mélange aléatoire ou pas ?
			#si pas d'aléatoire ça converge plus rapidement mais stagne à priori plus vite ?
			for col1 in L4:
				for col2 in Lautr[0:32]:
					NL=NL+[col1.croisement(col2)]
			for col in Lautr[32:107]:
				NL=NL+self.generation(col,1)
			NL=NL+self.generation1(colo,3)
			#listenl=[collo.d.jauge() for collo in NL]	
			#print("listenl",len(NL),"jauge",listenl)
			(L4,Lautr)=self.selection(NL,4)
			#liste=[collo.d.jauge() for collo in L4+Lautr]
			l4=[collo.d.jauge() for collo in L4]
			#print("apresS4",len(NL),min(liste),"jauge",listenl)
			print("Les 4 meilleurs de la novgen : ",l4)
			
		return(L4[0])		

	
Ini.initpython() #mettre à jour les variables globales de Ini
#création du colloscope initial
Ci=Collo_init()
Ci.creation()
#print(Ini.matp)
#print(Ini.ligne1)
#print(Ini.nbl)
#print(Ci.c)
#print(Ci.d)
#print("dir(Ci)",dir(Ci))
#print(Ci.c)
#Ci.affiche()
cons=Cons()
#calcul de toutes les contraintes
cons.contrainte()
#print(Cons.DC1)
#print(Cons.DC2)
#print("Ci.d",Ci.d)
ncollo=Mutation(Ci)
ncollo.mutation_minus_gros()
#Ci.affiche()
#print('-----------------------------------------------')
#ncollo.affiche()
#nncollo=Mutation(Ci)
#nncollo.croisement(ncollo)

#print('-----------------------------------------------')
#nncollo.affiche()
#print(type(ncollo))
#print(ncollo.c)
#print(ncollo.d)
#print(ncollo.d.jauge())
#ncollo.termine()
gene=Gene()
C=gene.evolution(Ci,nbgen)
C.termine()
