# _*_coding:utf-8_*
import string
from random import *
import codecs
import time

fichier = open("Results.txt", "w")
fichier.write("Ce fichier contient les messages publiques que l'utilisateur a généré avec le chiffre de Vernam.\n\n")

def Xor(s1, s2):
    if not s1 or not s2:
        return ''

    maxlen = max(len(s1), len(s2))

    s1 = s1.zfill(maxlen)
    s2 = s2.zfill(maxlen)

    result  = ''

    i = maxlen - 1
    while(i >= 0):
        s = int(s1[i]) + int(s2[i])
        if s == 2: #1+1
            result = "%s%s" % (result, '0')
        elif s == 1: # 1+0
            result = "%s%s" % (result, '1')
        else: # 0+0
            result = "%s%s" % (result, '0') 

        i = i - 1;
    return result[::-1]

def KeyGen(message):
	print "\nGénération d'une clef..."
	key=""
	dic=string.ascii_uppercase
	for x in range(0,len(message)):
		letter=dic[randint(0,25)]
		key=key+letter
	key=key.upper()
	print "\n    La clef :          "+key
	return key

def KeyGenSecured(message):
	key=""
	for x in range(0,len(message)):
		letter=str(randint(0,511))
		while len(letter)<3:
			letter="0"+letter
		key=key+str(letter)
	print "\n    La clef :          "+key
	return key

def Create(message,key):
	code=""
	for x in range(0,len(message)):
		lettre=(((ord(message[x])-64+ord(key[x])-64))%26)+64
		if lettre==64:
			lettre=90
		code=code+chr(lettre)
	return code

def CreateBin(message,key):
	message=message.upper()
	code=""
	for x in range(0,len(message)):
		lettreM=bin(ord(message[x])-64)[2:]
		lettreK=bin(ord(key[x])-64)[2:]
		lettreC=Xor(lettreM,lettreK)
		print lettreM+" xor "+lettreK+" = "+lettreC
		lettreC=(int(lettreC,2)+64)
		code=code+chr(lettreC)
	return code

def CreateBinSecured(message,key):
	code=""
	for x in range(0,len(message)):
		lettreM=bin(ord(message[x]))[2:]
		lettreK=bin(int(key[x*3:(x*3)+3]))[2:]
		lettreC=Xor(lettreM,lettreK)
		print lettreM+" xor "+lettreK+" = "+lettreC
		lettreC=int(lettreC,2)
		code=code+str(lettreC)
	return code

def CreateBinSecuredBis(mes1,mes2):
	code=""
	for x in range(0,(len(mes1)/3)):
		lettreM=bin(int(mes1[x*3:(x*3)+3]))[2:]
		lettreK=bin(int(mes2[x*3:(x*3)+3]))[2:]
		lettreC=Xor(lettreM,lettreK)
		lettreC=str(lettreC)
		while len(lettreC)<3:
			lettreC="0"+lettreC
		print lettreM+" xor "+lettreK+" = "+lettreC
		lettreC=int(lettreC,2)
		code=code+str(lettreC)
	return code

def Vernam():
	print"------------------------------------------\n\n"
	
	#Creation de la clef

	print "\n    Let's code !\n"
	message=raw_input("Votre message à chiffrer : ")
	print "\n    Votre message :    "+message
	#key=range(0,len(message))
	key=KeyGenSecured(message)

	#Cration du code
	print "\nAddition des lettres..."
	code=CreateBinSecured(message,key)

	print "\n    Le code :          "+code+"\n"
	print "Le message publique créé vient d'etre écrit dans le fichier Results.txt\n"
	print "Terminé\n--------------------------------\n"
	fichier.write("Le message "+message+" devient "+code+" par la clef "+key+"\n\n")
	choice = raw_input("    Appuyer sur entrer pour terminer. \n")



def Crack():
	print"------------------------------------------\n\n"
	print "\n    Let's crack !\nNous allons démontrer la faiblesse de ce code si la meme clef est utilisée à deux reprises\nPar soucis de performance nous allons nous limiter à des mots de la langue française.\n"
	ok=False
	while ok==False:
		message1=raw_input("Votre premier mot à chiffrer : ")
		message2=raw_input("Votre second mot à chiffrer (de meme longueur) : ")
		if len(message1)==len(message2):
			ok=True
		else:
			print "Les messages doivent etre de meme longueur puisqu'on utilise la meme clef!"
	key=KeyGenSecured(message1)
	choice = raw_input("\n    Appuyer sur entrer pour continuer... \n")
	code1=CreateBinSecured(message1,key)
	print "\n    "+message1+" devient :  "+code1+"\n"
	code2=CreateBinSecured(message2,key)
	print "\n    "+message2+" devient : "+code2+"\n"
	print "\nLes deux messages publiques viennent d'être générés avec la meme clef.\nMaintenant nous allons retrouver les deux messages en clair en utilisant seulement les deux codes publiques que nous venons de créer et un dictionnaire qui contient les mots de la langue française.\n"
	fichier.write("Crackage : les deux messages interceptes codés avec la même clef : "+code1+" et "+code2+"\n\n")
	choice = raw_input("\n    Appuyer sur entrer pour continuer... \n")
	print "Nous combinons par 'OU Exclusif' les deux messages publiques : \n..."
	codeSumm=CreateBinSecuredBis(code1,code2)
	print "\n    "+code1+" xor "+code2+" = "+codeSumm
	
	choice = raw_input("\n    Appuyer sur entrer pour continuer... \n")

	start_time=time.time()
	filepath = "wordsFR.txt"
	dico = []
	with codecs.open(filepath, "r", "utf-8_") as lines:
		final=""
		#i=0
		for l in  lines:
			l=l[:-1]
			if len(l)==len(codeSumm):
				dico.append(l)
				#dico[i]=(l[:-1])
				#i=i+1
		for m in dico:
			codeFinal=CreateBinSecured(m,codeSumm)
			if codeFinal in dico:
				founded=True
				final+=""+codeFinal+" et "+m+"\n"
		interTime=str(time.time() - start_time)
		if founded==True:
			print '    Annalyse terminée en '+interTime+' secondes.\n\n    Combinaisons possibles:'
			print final
		else:
			print '    Première annalyse terminée en '+interTime+' secondes.\n\n    Aucune combinaison trouvée.\n'
			choice = raw_input("    Voulez-vous lancer le générateur de mots ? (yes/no) \n")
			if choice=='yes':
				print 'lancement du générateur'
			else:
				print 'pareil'
		fichier.write("    Annalyse terminee en "+interTime+" secondes.\n    Combinaisons possibles:\n\n"+final+"\n")
        print "Les messages découverts viennent d'etre écrit dans le fichier Results.txt\n"
	print "Terminé\n--------------------------------\n"
	choice = raw_input("    Appuyer sur entrer pour terminer. \n")

#Menu de l'application-------------------------------------
print"------------------------------------------\n\n"

print "Chiffre de Vernam (masque à clef jettable):\n\nCe programme va vous permettre de suivre la création d'un message cripté et de constater l'importance de l'utilistion unique de sa clef.\n"
quit=False
while quit==False:
	
	print "'1' Créer un chiffre de Vernam\n'2' Craquer le chiffre de Verman\n\n('q' pour quitter)\n"
	choice = raw_input("Votre choix : ")
	#Controle de la réponse utilisateur
	if (choice=='1' or choice=='2'):
		if choice=='1':
			Vernam()
		elif choice=='2':
			Crack()
	elif choice=='q':
		fichier.write("\n					Fait par Alex Fabre.")
		fichier.close()
		quit=True
	else:
		print "\nRéponse non valide! ('1' '2' ou 'q')\n"
