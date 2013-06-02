import csv, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "babyexplorer.settings")
from models import Name, Year, nameInstance

yearDic=dict()




with open('babynames.csv','rb') as csvfile:
	rdr=csv.reader(csvfile,delimiter=' ',quotechar='"')
	for row in rdr:
		print row[2]