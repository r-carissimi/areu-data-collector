import requests
import csv
import os

SORTED_PROPERTIES = [
	"aat",
	"soreu",
	"aggiornato_alle",
	"day_data",
	"msb",
	"msi",
	"msa",
	"elisoccorso",
	"soccorso_alpino",
	"soccorso_acqua",
	"missioni",
	"rosso",
	"giallo",
	"verde",
	"bianco",
	"totale_missioni",
	"medico_acuto",
	"caduta",
	"incidente_stradale",
	"infortunio",
	"evento_violento",
	"intossicazione",
	"animali",
	"calamita_naturale",
	"evento_massa",
	"incidente_acqua",
	"incidente_montano",
	"incidente_speleo",
	"soccorso_persona",
	"non_noto",
	"altri_motivi",
	"soccorsi",
	"soccorso_primario",
	"soccorso_secondario",
	"guardia_medica",
	"informazioni",
	"consulenza",
	"trasporto_organi",
	"trasporto_prenotato",
	"prestazione_ambulatoriale",
	"da_richiamare",
	"mezzi_altro",
	"altro",
	"totale_traffico_tel",
]

class Collector:

	def __init__(self):
		self.refreshToken()

	def get(self):
		API_URL = "https://www.areu.lombardia.it/api/jsonws/areu-eventi-regione-portlet.regioneeventijson/statistiche-regione"

		if(self.token is not None):
			parameters = {
				'p_auth': self.token
			}

			response = requests.get(API_URL, params=parameters)
		else:
			response = requests.get(API_URL)
		
		if (response.status_code == 200):
			return response.json()["in_corso"]
		else:
			print("Error: " + response.reason)
			return None				

	def refreshToken(self):
		TOKEN_URL = "https://www.areu.lombardia.it/web/home/missioni-aat-real-time"
		TOKEN_KEY = "Liferay.authToken="
		TOKEN_LENGTH = 8

		response = requests.get(TOKEN_URL)
		if(response.status_code == 200):
			text = response.text
			position = text.find(TOKEN_KEY)+len(TOKEN_KEY)+1
			self.token = text[position:position+TOKEN_LENGTH]
		else:
			print("ERROR: Cannot obtain token")
			self.token = None

	def save(self):
		DATA_DIR = "./data/"

		if(not os.path.isdir(DATA_DIR)):
			os.mkdir(DATA_DIR)

		data = self.get()
		for row in data:
			row = self.sort_row(row)
			filename = DATA_DIR + row['aat'].lower().strip() + ".csv"
			if(self.file_empty(filename)):
				self.write_file_header(filename, row)
			self.append_file_data(filename, row)

	def write_file_header(self, filename, row):
		try:
			with open(filename, 'w') as f:
				writer = csv.writer(f)
				writer.writerow(row.keys())	
		except IOError:
			print("ERROR: Cannot write file")
	
	def append_file_data(self, filename, row):
		if(not self.equals_last_row(filename, row)):
			try:
				with open(filename, 'a') as f:
					writer = csv.writer(f)
					writer.writerow(row.values())
			except IOError:
				print("ERROR: Cannot write file")

	def file_empty(self, filename):
		return not os.path.isfile(filename) or os.stat(filename).st_size == 0

	def equals_last_row(self, filename, row):
		try:
			with open(filename, 'r') as f:
				last_line = f.readlines()[-1].split(",")
				return last_line[SORTED_PROPERTIES.index('aat')] == row['aat'] and last_line[SORTED_PROPERTIES.index('aggiornato_alle')] == row['aggiornato_alle']
				
		except IOError:
			print("ERROR: Cannot read file " + filename)
			return False

	def sort_row(self, row):
		new_row = dict()
		for key in SORTED_PROPERTIES:
			new_row[key] = row[key]
		return new_row

c = Collector()
c.save()