# coding: utf8

import os
import csv
import urllib
import xmltodict
import shutil
import pprint
import json
import glob
#import os.path.basename

#Etape 1 : Recuperer le fichier CSV
#Ici on recupere le chemin du fichier contenant les valeurs CSV

reponse = raw_input("(a) CSV - Grobid , (b) JSON - TXT, (c) CSV - JSON , (d) JSON Generation\n")
print(reponse)

#Menu de navigation
if reponse == 'a':
	#CSV vers XML avec recuperation des PDF en ligne
	print("Transformation CSV -> XML")
	#nomFichier = reponse + ".csv
	data = open("Data.csv" , "r")

	#indice des colonnes contenant les informations qui nous interesse
	indiceColPDF = 8
	indiceColMS = 9

	#Param definissant les delimiteurs dans le document CSV
	#print(nomFichier)
	reader = csv.reader(data,delimiter=';')

	#Boucle principale
	#Etape 2 : Trier ce CSV pour ne recuperer que les lignes avec les bons MS
	#Etape 3 : Parmis ces lignes on ne recup que les valeurs lignes par lignes 
	#de la colonne contenant le lien vers le fichier PDF
	#Etape 4 : (a)On va recuperer un par un les PDF
	#les telecharger et (b) les passer individuellement sur GroBid TEI
	#pour obtenir un .XML par ligne
	#Etape 5 : Ces .XML vont ensuite etre transformes au format .JSON
	for row in reader:
		if(row[indiceColMS] != 'MS'):
			if float(row[indiceColMS]) >= 1 and float(row[indiceColMS]) <= 9:
				valeur = row[indiceColPDF]
				#apres cela on a plus que les lignes triees par MS
				#print(row)test recup des lignes
				#Etape 3 :
				#valeur contient desormais l'adr du lien PDF du CSV
				print(valeur)
				#Etape 4 (a):
				chaineNom = "pdfArticle"+row[0]+".pdf"
				print(chaineNom)
				chaineNom = "./in/"+chaineNom
				urllib.urlretrieve(valeur,chaineNom)

	#Etape 4 (b) :
	#on passe le document pdf sur l'API de Grobid pour obtenir un .XML TEI

	#reponse = input("Appliquer la transfo TEI ? (oui/non)")
	#if reponse == "o":
	os.system('python3.5 ./grobid-client.py --input ./in/ --output ./out/ processHeaderDocument')

	#rep = input('Presser une fois la transfo effectuee')

	#Etape 5 : JSON et Affinement
	chemin = './out/*.tei.xml'
	cheminMary = './out/json/*.json'
	fichiersTEI = glob.glob(chemin)
	i = 1
	print('Avant la boucle de transformation')
	for nom in fichiersTEI:
		with open(nom) as f:
			print('Pendant la transfo')
			doc = xmltodict.parse(f.read(),encoding='utf-8')
			chaineNomBis = "./out/json/jsonArticle"+str(i)+".json"
			f2 = open(chaineNomBis,"w")
			f2.write(json.dumps(doc,sort_keys=True))
			f2.close()
			#Recuperation des informations necessaires
			#fluxDon = json.dumps(doc,sort_keys=True)
			#auteur = fluxDon['persName']['forename']['#text']
			#settlement = 
			#Une fois les donnees recuperees on recreer un doc json clone
			#Permettant de ne garder que les champs qui nous interesse dans la structure que l'on souhaite
			pp = pprint.PrettyPrinter(indent=4)
			pp.pprint(json.dumps(doc))
			i = i+1

if reponse == 'b':
	#JSON vers TXT (avec sauvegarde en csv)
	print("Transformation JSON -> txt (champs abstract et id")
	cheminJSON = './out/refract/*.json'
	i = 1
	fichiersJSON = glob.glob(cheminJSON)
	print('Debut de la chaine de transformation')
	chaineCSV = "id;annee\n"
	for nom in fichiersJSON:
		with open(nom) as f:
			#extraire a partir d une liste de json une liste au format txt (id et abstract)
			#recuperation des JSON
			valeurs = json.load(f)
			idArt = str(valeurs['idArt'].encode('utf-8','strict'))
			abstract = str(valeurs['abstract'].encode('utf-8','strict'))
			annee = str(valeurs['year'].encode('utf-8','strict'))
			print('Transformation article_'+str(idArt)+' : en cours . . .')
			chaineEcritureTXT = "./out/refract/txt/article_" + str(idArt) + ".txt"
			#test
			#chaine = "Id de l'Article : "+idArt+"\nResume de l'Article : "+abstract
			#ecriture dans txt
			f2 = open(chaineEcritureTXT,"w")
			f2.write(abstract)
			f2.close()
			print('Transformation : '+str(i)+' terminee !')
			chaineCSV = chaineCSV + "article_" + str(i) + "," + annee + "\n"
			idArt = ""
			abstract = ""
			annee = ""
			i = i+1
	print('Transformations terminees !('+str(i-1)+')')
	print('Sauvegarde des données : id et annees effectuee dans out/refract/csv !')
	#test ecriture csv
	#print(chaineCSV)
	f3 = open("./out/refract/csv/metadata.csv","w")
	f3.write(chaineCSV)
	f3.close()

if reponse == 'c':
	#CSV vers JSON
	print("Transformation CSV -> JSON (tout les champs")
	cheminCSV = './out/CSVToJSON/*.csv'
	i = 1
	fichiersCSV = glob.glob(cheminCSV)
	print('Debut de la chaine de transformation')
	indiceColMS = 9
	for nom in fichiersCSV:
		with open(nom) as f:
			reader = csv.reader(f,delimiter=';')
			for row in reader:
				if(row[indiceColMS] != 'MS'):
					if float(row[indiceColMS]) >= 1 and float(row[indiceColMS]) <= 9:
						idArticle = str(row[0].encode('utf-8','strict'))
						series = str(row[1].encode('utf-8','strict'))
						booktitle = str(row[2].encode('utf-8','strict'))
						year = str(row[3].encode('utf-8','strict'))
						#title = str(row[4].encode('utf-8','strict'))
						title = "pb encodage"
						abstract = "pb encodage"
						authors = "pb encodage"
						#abstract = str(row[5])
						#authors = str(row[6].encode('utf-8','strict'))
						pdf1page = str(row[7].encode('utf-8','strict'))
						pdfarticle = str(row[8].encode('utf-8','strict'))
						
						chaineNom = "article_"+row[0]+".json"
						print(chaineNom)
						chaineNom = "./out/CSVToJSON/json/" + chaineNom
						f2 = open(chaineNom,"w")
						f2.write('{\n"idArt": "'+str(idArticle)+ '",\n"series": "'+str(series)+'",\n"booktitle": "' + str(booktitle)+ '",\n"year": "'+str(year)+ '",\n"title": "'+str(title)+ '",\n"abstract": "'+str(abstract)+'",\n"authors": "'+str(authors)+'",\n"pdf1page": "' + str(pdf1page)+'",\n"pdfarticle": "'+str(pdfarticle)+'"\n}')
						f2.close()

if reponse == 'd':
	#Generation JSON
	print("Generation de JSON fusionnes\n")
	#Repertoires des JSON qui serront a fusionner
	cheminJSON1 = './out/assemble/listeArticles/*.json'
	cheminJSON2 = './out/assemble/listeArticles_complement_metaSession/*.json'
	i = 1
	fichiersJSON1 = glob.glob(cheminJSON1)
	fichiersJSON2 = glob.glob(cheminJSON2)
	print('Debut de la chaine de transformation')
	for nom in fichiersJSON1:
		with open(nom) as f:
			#extraire les donnees du repertoire 1			
			valeurs = json.load(f)
			if 'year' not in valeurs:
				print("Pas de champs 'year' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				year1 = ""
			else:
				year1 = str(valeurs['year'].encode('utf-8','strict'))

			if 'metaSession' not in valeurs:
				#raise ValueError("Pas de champs 'metaSession' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				metaSession1 = ""
			else:
				metaSession1 = str(valeurs['metaSession'].encode('utf-8','strict'))
			
			if 'pdf1page' not in valeurs:
				#raise ValueError("Pas de champs 'pdf1page' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				pdf1page1 = ""
			else:
				pdf1page1 = str(valeurs['pdf1page'].encode('utf-8','strict'))

			if 'pdfarticle' not in valeurs:
				#raise ValueError("Pas de champs 'pdfarticle' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				pdfarticle1 = ""
			else: 
				pdfarticle1 = str(valeurs['pdfarticle'].encode('utf-8','strict'))
			
			if 'abstract' not in valeurs:
				#raise ValueError("Pas de champs 'abstract' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				abstract1 = ""
			else: 
				abstract1 = str(valeurs['abstract'].encode('utf-8','strict'))

			if 'title' not in valeurs:
				#raise ValueError("Pas de champs 'title' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				title1 = ""
			else:
				title1 = str(valeurs['title'].encode('utf-8','strict'))
			
			#partie auteur
			if 'placeAut' not in valeurs:
				#raise ValueError("Pas de champs 'placeAut' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				placeAut1 = ""
			else: 
				placeAut1 = str(valeurs['placeAut'])	
			
			
			if 'series' not in valeurs:
				#raise ValueError("Pas de champs 'series' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				series1 = ""
			else: 
				series1 = str(valeurs['series'].encode('utf-8','strict'))
			
			if 'location' not in valeurs:
				#raise ValueError("Pas de champs 'location' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				location1 = ""
			else: 
				location1 = str(valeurs['location'])	
	
			if 'place' not in valeurs:
				#raise ValueError("Pas de champs 'place' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				place1 = ""
			else: 
				place1 = str(valeurs['place'].encode('utf-8','strict'))	
			
			if 'booktitle' not in valeurs:
				#raise ValueError("Pas de champs 'booktitle' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				booktitle1 = ""
			else: 
				booktitle1 = str(valeurs['booktitle'].encode('utf-8','strict'))	

			if 'idArt' not in valeurs:
				#raise ValueError("Pas de champs 'idArt' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				idArt1 = ""
			else:
				idArt1 = str(valeurs['idArt'].encode('utf-8','strict'))

			if 'authors' not in valeurs:
				#raise ValueError("Pas de champs 'authors' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
				authors1 = ""
			else: 
				authors1 = str(valeurs['authors'])
			
			#Verification dans le repertoire 2
			print(os.path.basename(f.name))
			chaineVerif = str("./out/assemble/rep2/" + os.path.basename(f.name))
			if(os.path.isfile(chaineVerif)):
				#alors le fichier concerne par le repertoire1 existe dans repertoire2
				f2 = open(chaineVerif)
				#recuperation de ses valeurs
				valeurs = json.load(f2)
				if 'year' not in valeurs:
					#raise ValueError("Pas de champs 'year' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					year2 = ""
				else:
					year2 = str(valeurs['year'].encode('utf-8','strict'))

				if 'metaSession' not in valeurs:
					#raise ValueError("Pas de champs 'metaSession' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					metaSession2 = ""
				else: 
					metaSession2 = str(valeurs['metaSession'].encode('utf-8','strict'))
			
				if 'pdf1page' not in valeurs:
					#raise ValueError("Pas de champs 'pdf1page' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					pdf1page2 = ""
				else: 
					pdf1page2 = str(valeurs['pdf1page'].encode('utf-8','strict'))

				if 'pdfarticle' not in valeurs:
					#raise ValueError("Pas de champs 'pdfarticle' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					pdfarticle2 = ""
				else: 
					pdfarticle2 = str(valeurs['pdfarticle'].encode('utf-8','strict'))
			
				if 'abstract' not in valeurs:
					#raise ValueError("Pas de champs 'abstract' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					abstract2 = ""
				else: 
					abstract2 = str(valeurs['abstract'].encode('utf-8','strict'))

				if 'title' not in valeurs:
					#raise ValueError("Pas de champs 'title' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					title2 = ""
				else: 
					title2 = str(valeurs['title'].encode('utf-8','strict'))
			
				#partie auteur
				if 'placeAut' not in valeurs:
					#raise ValueError("Pas de champs 'placeAut' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					placeAut2 = ""
				else: 
					placeAut2 = str(valeurs['placeAut'])	
			
			
				if 'series' not in valeurs:
					#raise ValueError("Pas de champs 'series' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					series2 = ""
				else: 
					series2 = str(valeurs['series'].encode('utf-8','strict'))
			
				if 'location' not in valeurs:
					#raise ValueError("Pas de champs 'location' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					location2 = ""
				else: 
					location2 = str(valeurs['location'])	
	
				if 'place' not in valeurs:
					#raise ValueError("Pas de champs 'place' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					place2 = ""
				else: 
					place2 = str(valeurs['place'].encode('utf-8','strict'))	
			
				if 'booktitle' not in valeurs:
					#raise ValueError("Pas de champs 'booktitle' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					booktitle2 = ""
				else: 
					booktitle2 = str(valeurs['booktitle'].encode('utf-8','strict'))	

				if 'idArt' not in valeurs:
					#raise ValueError("Pas de champs 'idArt' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					idArt2 = ""
				else: 
					idArt2 = str(valeurs['idArt'].encode('utf-8','strict'))

				if 'authors' not in valeurs:
					#raise ValueError("Pas de champs 'authors' dans les json a l'iteration  : " + str(i) + " du repertoire 2")
					authors2 = ""
				else: 
					authors2 = str(valeurs['authors'])

				#Une fois les valeurs recuperees on va creer le fichier json fusionne dans rep3
				chaineEcritureJSON = "./out/assemble/rep3/" + os.path.basename(f.name)
				if(year1 == ""):
					fusion_year = year2
				else:
					fusion_year = year1

				if(metaSession1 == ""):
					fusion_metaSession = metaSession2
				else:
					fusion_metaSession = metaSession1

				if(pdf1page1 == ""):
					fusion_pdf1page = pdf1page2
				else:
					fusion_pdf1page = pdf1page1

				if(pdfarticle1 == ""):
					fusion_pdfarticle = pdfarticle2
				else:
					fusion_pdfarticle = pdfarticle1
				
				if(abstract1 == ""):
					fusion_abstract = abstract2
				else:
					fusion_abstract = abstract1

				if(title1 == ""):
					fusion_title = title2
				else:
					fusion_title = title1

				if(placeAut1 == ""):
					fusion_placeAut = placeAut2
				else:
					fusion_placeAut = placeAut1

				if(series1 == ""):
					fusion_series = series2
				else:
					fusion_series = series1
			
				if(location1 == ""):
					fusion_location = location2
				else:
					fusion_location = location1

				if(place1 == ""):
					fusion_place = place2
				else:
					fusion_place = place1

				if(booktitle1 == ""):
					fusion_booktitle = booktitle2
				else:
					fusion_booktitle = booktitle1

				if(idArt1 == ""):
					fusion_idArt = idArt2
				else:
					fusion_idArt = idArt1

				if(authors1 == ""):
					fusion_authors = authors2
				else:
					fusion_authors = authors1
				
				#Maintenant que l'on a toutes les valeurs on peut creer le fichier JSON
				chaineEcritureJSON = "./out/assemble/rep3/" + os.path.basename(f.name)
				f3 = open(chaineEcritureJSON,"w")
				f3.write('{\n"year": "'+str(fusion_year)+ '",\n"metaSession": "'+str(fusion_metaSession)+'",\n"pdf1page": "' + str(fusion_pdf1page)+ '",\n"pdfarticle": "'+str(fusion_pdfarticle)+ '",\n"abstract": "'+str(fusion_abstract)+ '",\n"title": "'+str(fusion_title)+'",\n"placeAut": "'+str(fusion_placeAut)+'",\n"series": "' + str(fusion_series)+'",\n"location": "' + str(fusion_location)+'",\n"place": "' + str(fusion_place)+'",\n"booktitle": "' + str(fusion_booktitle)+'",\n"idArt": "' + str(fusion_idArt)+'",\n"authors": "'+str(fusion_authors)+'"\n}')
				f3.close()

			else:
				#Dans le cas où il n'existe pas dans le repertoire2
				#alors le fichier concerne par le repertoire1
				#recuperation de ses valeurs
				valeurs = json.load(f)
				if 'year' not in valeurs:
					#raise ValueError("Pas de champs 'year' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					year1 = ""
				else:
					year1 = str(valeurs['year'].encode('utf-8','strict'))

				if 'metaSession' not in valeurs:
					#raise ValueError("Pas de champs 'metaSession' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					metaSession1 = ""
				else:
					metaSession1 = str(valeurs['metaSession'].encode('utf-8','strict'))
			
				if 'pdf1page' not in valeurs:
					#raise ValueError("Pas de champs 'pdf1page' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					pdf1page1 = ""
				else:
					pdf1page1 = str(valeurs['pdf1page'].encode('utf-8','strict'))

				if 'pdfarticle' not in valeurs:
					#raise ValueError("Pas de champs 'pdfarticle' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					pdfarticle1 = ""
				else: 
					pdfarticle1 = str(valeurs['pdfarticle'].encode('utf-8','strict'))
			
				if 'abstract' not in valeurs:
					#raise ValueError("Pas de champs 'abstract' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					abstract1 = ""
				else: 
					abstract1 = str(valeurs['abstract'].encode('utf-8','strict'))

				if 'title' not in valeurs:
					#raise ValueError("Pas de champs 'title' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					title1 = ""
				else:
					title1 = str(valeurs['title'].encode('utf-8','strict'))
			
				#partie auteur
				if 'placeAut' not in valeurs:
					#raise ValueError("Pas de champs 'placeAut' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					placeAut1 = ""
				else: 
					placeAut1 = str(valeurs['placeAut'])	
			
			
				if 'series' not in valeurs:
					#raise ValueError("Pas de champs 'series' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					series1 = ""
				else: 
					series1 = str(valeurs['series'].encode('utf-8','strict'))
			
				if 'location' not in valeurs:
					#raise ValueError("Pas de champs 'location' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					location1 = ""
				else: 
					location1 = str(valeurs['location'])	
	
				if 'place' not in valeurs:
					raise ValueError("Pas de champs 'place' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					place1 = ""
				else: 
					place1 = str(valeurs['place'].encode('utf-8','strict'))	
			
				if 'booktitle' not in valeurs:
					#raise ValueError("Pas de champs 'booktitle' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					booktitle1 = ""
				else: 
					booktitle1 = str(valeurs['booktitle'].encode('utf-8','strict'))	

				if 'idArt' not in valeurs:
					#raise ValueError("Pas de champs 'idArt' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					idArt1 = ""
				else:
					idArt1 = str(valeurs['idArt'].encode('utf-8','strict'))

				if 'authors' not in valeurs:
					#raise ValueError("Pas de champs 'authors' dans les json a l'iteration  : " + str(i) + " du repertoire 1")
					authors1 = ""
				else: 
					authors1 = str(valeurs['authors'])

				#Une fois les valeurs recuperees on va creer le fichier json dans rep3
				chaineEcritureJSON = "./out/assemble/rep3/" + os.path.basename(f.name)
				fusion_year = year1
				fusion_metaSession = metaSession1
				fusion_pdf1page = pdf1page1
				fusion_pdfarticle = pdfarticle1
				fusion_abstract = abstract1
				fusion_title = title1
				fusion_placeAut = placeAut1
				fusion_series = series1
				fusion_location = location1
				fusion_place = place1
				fusion_booktitle = booktitle1
				fusion_idArt = idArt1
				fusion_authors = authors1

				#Maintenant que l'on a toutes les valeurs on peut creer le fichier JSON
				f3 = open(chaineEcritureJSON,"w")
				f3.write('{\n"year": "'+str(fusion_year)+ '",\n"metaSession": "'+str(fusion_metaSession)+'",\n"pdf1page": "' + str(fusion_pdf1page)+ '",\n"pdfarticle": "'+str(fusion_pdfarticle)+ '",\n"abstract": "'+str(fusion_abstract)+ '",\n"title": "'+str(fusion_title)+'",\n"placeAut": "'+str(fusion_placeAut)+'",\n"series": "' + str(fusion_series)+'",\n"location": "' + str(fusion_location)+'",\n"place": "' + str(fusion_place)+'",\n"booktitle": "' + str(fusion_booktitle)+'",\n"idArt": "' + str(fusion_idArt)+'",\n"authors": "'+str(fusion_authors)+'"\n}')
				f3.close()
