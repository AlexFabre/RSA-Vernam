# _*_coding:utf-8_*
import string
from random import *
import codecs
from math import sqrt
import time

#fichier = open("ResultatsRSA.txt", "w")

def euclide(a,b):
	#Return the higher common divider of a and b. Used to test if a and b are firts together.
	if (b==0) :
		return a
	else :
		r=a%b
		return euclide(b,r)

def euclidextended(a,b):
	# r entier (naturel) et  u, v entiers relatifs tels que r = pgcd(a, b) et r = a*u+b*v
	# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return y

def premier(max):
	# The firsts 100 firsts are in range(0,548) (547 is number 100)
	listNPremiers=[]
	listNPremiers.append(2)
	start_time=time.time()
	for i in range(3,max):
		for prime in listNPremiers:
			if i%prime==0:
				event=False
				break
			if prime>sqrt(i):
				event=True
				break
		if event:
			listNPremiers.append(i)
	interTime=str(time.time() - start_time)
	#fichier.write("    Recherche des deux premiers terminee en "+interTime+" secondes.\n")
	return listNPremiers

def expmod(message,e,m):
	code=""
	for x in range(1,len(message)+1):
		lettre=ord(message[x-1])
		c=pow(lettre,e,m)
		print c
		while len(str(c))<len(str(m)):
			c='0'+str(c)
		code=code+str(c)
	return code

def expmodinverted(intarray,d,m):
	for i in intarray:
		message=""
		letter1=""
		letter2=""
		letters=pow(int(i),d,m)
		if len(str(letters))>3:
			letter1=str(letters)[:3]
			print letter1,
			letter2=str(letters)[3:]
			mot=chr(int(letter1))+chr(int(letter2))
			print mot,
			message=message+mot
		else:
			letter=chr(letters)
			print letter,
			message=message+letter
	return message

def expmodsecured(message,e,m):
	#Fonctionne parfaitement ! Le problème c'est que lorsqu'on fait le modulo on peut etre ecarté de la valeur de départ...
	#Problème résolu ! Il faut pas que la valeur du truc à coder soit supérieur au modulo dans l'exponentiation modulaire !
	code=""
	i=0
	blocs=(len(message)/2)
	r=(len(message)%2)
	while(i<blocs*2):
		c=ord(message[i])
		k=ord(message[i+1])
		while len(str(c))<3:
			c='0'+str(c)
		while len(str(k))<3:
			k='0'+str(k)
		b6=str(c)+str(k)
		b6=pow(int(b6),e,m)
		while len(str(b6))<len(str(m)):
			b6='0'+str(b6)
		code=code+str(b6)
		print b6
		i=i+2
	if r==1:	
		c=ord(message[i])
		while len(str(c))<3:
				c='0'+str(c)
		b6=pow(int(c),e,m)
		while len(str(b6))<len(str(m)):
			b6='0'+str(b6)
		code=code+str(b6)
		print b6
	return code

def expmodinvertedsecured(intarray,d,m):
	message=""
	for i in intarray:
		letter1=""
		letter2=""
		letters=pow(int(i),d,m)
		while ((len(str(letters))%2)!=0):
			letters='0'+str(letters)
		letters=int(letters)
		width=len(str(letters))/2
		if len(str(letters))>3:
			letter1=str(letters)[:width]
			letter2=str(letters)[width:]
			mot=chr(int(letter1))+chr(int(letter2))
			message=message+mot
		else:
			letter=chr(letters)
			message=message+letter

	return message

def RSA():
	print"------------------------------------------\n\n"
	b1=randint(200,660)
	b2=randint(200,660)
	while b2<b1:
		b2=randint(200,660)
	listNPremiers=premier(5000) 
	print 'p=		'+str(listNPremiers[b1])
	print 'q=		'+str(listNPremiers[b2])+'\n'
	b0=listNPremiers[b1]*listNPremiers[b2]
	print 'Module de chiffrement : n=p*q => '+str(b0)
	choice = raw_input("\n    	Appuyer sur entrer pour continuer. \n")
	r=(listNPremiers[b1]-1)*(listNPremiers[b2]-1)
	print 'Indicatrice d\'Euler : phi=(p-1)*(q-1) => '+str(r)
	print '\n\nRecherche de l\'exposant de chiffrement e premier avec phi...'
	choice = raw_input("\n    	Appuyer sur entrer pour lancer la recherche. \n")
	start_time=time.time()
	b3=2
	while euclide(b3,r)!=1:
		print '.',
		b3=b3+1
	interTime=str(time.time() - start_time)
	print '\n    Recherche de e terminé en '+interTime+' secondes\n\n 	e='+str(b3)+' est premier avec phi='+str(r)
	#fichier.write("    Recherche de l\'exposant de chiffrement terminé en "+interTime+" secondes\n 	e="+str(b3)+" est premier avec phi="+str(r))
	print '\nRecherche de l\'exposant de déchiffrement d inverse de e modulo phi...'
	choice = raw_input("\n    	Appuyer sur entrer pour lancer la recherche. \n")
	b4=euclidextended(r,b3)
	while b4<0:
		b4=b4+r
	print '\n 	d='+str(b4)+' est un inverse de e modulo phi.'
	print '\nOn a bien (e * d) = '+str(b4*b3)+' congru à 1 modulo phi ('+str(r)+')'
	choice = raw_input("\n    	Appuyer sur entrer pour continuer. \n")
	print 'Nous avons donc généré notre couple de clef:\n 	La clef publique (n,e) = ('+str(b0)+','+str(b3)+')\n 	La clef privée (n,d) = ('+str(b0)+','+str(b4)+')'
	#fichier.write('Nous avons donc notre couple de clef:\n 	La clef publique (n,e) = ('+str(b0)+','+str(b3)+')\n 	La clef privee (n,d) = ('+str(b0)+','+str(b4)+')')
	choice = raw_input("\n    	Appuyer sur entrer pour continuer... \n")
	message=''
	while message=='':
		message=raw_input("\nVotre message à chiffrer : ")
	print "\n    Votre message :    "+message
	b5=expmod(message,b3,b0)
	print "\n    Le code :          "+b5+"\n"
	#print "Le message publique créé vient d'etre écrit dans le fichier Results.txt\n"
	print "\nTerminé\n--------------------------------\n"
	#fichier.write("Le message "+message+" devient "+b5+" par la clef "+str(b0)+"\n\n")
	choice = raw_input("    Appuyer sur entrer pour terminer. \n")

def RSAsecure():
	print"------------------------------------------\n\n"
	print 'Génération des clefs...'
	p=randint(100,78498)
	q=randint(100,78498)
	print '.',
	while q<p:
		print '.',
		q=randint(100,78498)
	listNPremiers=premier(1000000)
	print '.',
	n=listNPremiers[p]*listNPremiers[q]
	print '.',
	phi=(listNPremiers[p]-1)*(listNPremiers[q]-1)
	print '.',
	e=2
	while euclide(e,phi)!=1:
		print '.',
		e=e+1
	d=euclidextended(phi,e)
	while d<0:
		d=d+phi
	print '\n\nVotre clef publique (n,e) = ('+str(n)+','+str(e)+')'
	message=''
	while message=='':
		message=raw_input("\nVotre message à chiffrer : ")
	print "\n    Votre message :    "+message
	c=expmodsecured(message,e,n)
	print "\n    Le code :          "+c+"\n"
	print "Le message publique créé vient d'etre écrit dans le fichier Results.txt\n"
	print "Terminé\n--------------------------------\n"
	#fichier.write("Le message "+message+" devient "+c+" par la clef "+str(n)+"\n\n")
	choice = raw_input("    Appuyer sur entrer pour terminer. \n")

def Crack():
	print"------------------------------------------\n\n"
	p=randint(200,270)
	q=randint(200,270)
	while q<p:
		q=randint(200,270)
	listNPremiers=premier(5000)
	n=listNPremiers[p]*listNPremiers[q]
	phi=(listNPremiers[p]-1)*(listNPremiers[q]-1)
	e=2
	while euclide(e,phi)!=1:
		e=e+1
	d=euclidextended(phi,e)
	while d<0:
		d=d+phi
	print 'Votre clef publique (n,e) = ('+str(n)+','+str(e)+')'
	message=''
	while message=='':
		message=raw_input("\nVotre message à chiffrer : ")
	print "\n    Votre message :    "+message
	c=expmodsecured(message,e,n)
	print "\n    Le code :          "+c
	choice = raw_input("\n    	Appuyer sur entrer pour continuer... \n")
	print"------------------------------------------\n"
	print "\nNous allons maitenant chercher l'indice de déchifrement d en utilisant seulement la clef publique (n,e) = ("+str(n)+','+str(e)+')'
	print "\nOn commence par chercher le couple unique (p,q) tel que p*q=n. Cette opération peut être longue est solicite au maximum le processeur."
	choice = raw_input("\n    	Appuyer sur entrer pour lancer la recherche... \n")
	nok=True
	while nok:
		for x in range(200,270):
			for y in range(200,270):
				if ((listNPremiers[x]*listNPremiers[y])==int(n)):
					print "p="+str(listNPremiers[x])
					print "q="+str(listNPremiers[y])
					print "\n"
					nok=False
					phicrack=((listNPremiers[x]-1)*(listNPremiers[y]-1))
					dcrack=euclidextended(phicrack,e)
					while dcrack<0:
						dcrack=dcrack+phicrack
					break
	print "On va recalculer l'indicatrice d'euler phi=(p-1)(q-1) pour trouver 'd' indice de déchifrement premier avec 'e' modulo n"
	print "phi="+str(listNPremiers[x]*listNPremiers[y])
	print "\n    On trouve d="+str(dcrack)
	print "\nNous allons maintenant retrouver le message d'origine en utilisant la clef privée reconstituée."
	bloc=[]
	n=str(n)
	g1=""
	for x in c:
		g1=g1+x
		if len(g1)%len(n)==0:
			bloc.append(g1)
			g1=""
	n=int(n)
	print "\n Le message déchifré : "+expmodinvertedsecured(bloc,dcrack,n)+"\n"
	choice = raw_input("    Appuyer sur entrer pour terminer. \n")


#Menu de l'application-------------------------------------

print"------------------------------------------\n\n"
print "Chiffrement R.S.A. (Rivest, Shamir, Adleman) :\n\nCe programme va vous permettre de suivre la création d'un message à chiffrement assymétrique et de constater l'importance de l'utilistion de très grands nombres premiers pour générer les clefs.\n"
quit=False
while quit==False:
	
	print "'1' Créer un couple de clef RSA naïf\n'2' Craquer le RSA \n'3' Chiffrer avec plus de sécurité\n\n('q' pour quitter)\n"
	choice = raw_input("Votre choix : ")
	#Controle de la réponse utilisateur
	if (choice=='1' or choice=='2' or choice=='3'):
		if choice=='1':
			RSA()
		elif choice=='2':
			Crack()
		elif choice=='3':
			RSAsecure()
	elif choice=='q':
		print("\n					Fait par Damien D, Alex F, Vincent F & Rémi C.")
		#fichier.close()
		quit=True
	else:
		print "\nRéponse non valide! ('1' '2' '3' ou 'q')\n"
		choice = raw_input("\n    	Appuyer sur entrer pour continuer. \n")


