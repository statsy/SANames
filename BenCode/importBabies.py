import csv, os, datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "babyexplorer.settings")
from babynames.models import Name, Year, nameInstance, mortNameInstance

yearDic=dict()
nameDic=dict()

# with open('babynames3.csv','rb') as csvfile:
# 	rdr=csv.reader(csvfile,delimiter=' ',quotechar='"')
# 	for row in rdr:
# 		year=row[5]
# 		name=row[1]
# 		freq=row[2]
# 		rank=row[3]
# 		sex=row[4]
# 		yrTot=row[6]
# 		yrProp=row[7]
# 		if yearDic.get(row[5]) is None:
# 			yearDic[year]={'male':0,'female':0}
# 		if yearDic[year][sex]==0:
# 			yearDic[year][sex]=int(yrTot)

# 		if nameDic.get(name) is None:
# 			nameDic[name]={'male':0,'female':0}
# 		nameDic[name][sex]+=int(freq)

# 		if sex=='male':
# 			sexMade=1
# 		else:
# 			sexMade=2
# 		ni=nameInstance(name=Name.objects.filter(name_text__exact=name)[0],year=Year.objects.filter(year_date__year=year)[0],sex=sexMade,frequency=freq,proportion=yrProp,year_val=year,name_text=name,rank=rank)
# 		ni.save()

with open('babynamesmortality2.csv','rb') as csvfile:
	rdr=csv.reader(csvfile,delimiter=' ',quotechar='"')
	for row in rdr:
		age=row[3]
		name=row[1]
		sex=row[2]
		freq=row[4]
		total_freq=row[5]
		prop=row[6]

		if sex=='male':
			sexMade=1
		else:
			sexMade=2
		ni=mortNameInstance(name=Name.objects.filter(name_text__exact=name)[0],age=age,sex=sexMade,frequency=freq,proportion=prop,name_text=name,total_frequency=total_freq)
		ni.save()

# for yr in yearDic:
# 	y=Year(year_date=datetime.date(int(yr),1,1),male_num=yearDic[yr]['male'],female_num=yearDic[yr]['female'],total_num=int(yearDic[yr]['male'])+int(yearDic[yr]['female']))
# 	y.save()

# for nm in nameDic:
# 	n=Name(name_text=nm,male_num=nameDic[nm]['male'],female_num=nameDic[nm]['female'],total_num=nameDic[nm]['male']+nameDic[nm]['female'])
# 	n.save()