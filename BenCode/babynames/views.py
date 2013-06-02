# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

import json

from babynames.models import Name, nameInstance, Year, mortNameInstance

def index(request):
	return HttpResponse("Hello world. You're at the babynames index.")

def namepage(request,name):
	name=name.upper()
	name_info=Name.objects.filter(name_text__exact=name)
	name_list=nameInstance.objects.filter(name__name_text__exact=name)

	name_list_sorted=name_list.order_by('rank')

	best_year=name_list_sorted[0].year_val

	year_list=Year.objects.order_by('year_date').all()

	yearDist={'males':[],'females':[]}

	if name_list_sorted[0].sex==1:
		popSex='men'
	else:
		popSex='women'

	for yar in year_list:
		yearDist['males'].append(yar.male_num)
		yearDist['females'].append(yar.female_num)

	if len(name_info)==0:
		name_found=False
	else:
		name_found=True
	context={'name_resp': name_info[0],'name_found':name_found,'name_list':name_list,'name':name,'male_dic':yearDist['males'],'female_dic':yearDist['females'],'most_popular':name_list_sorted[0],'popSex':popSex}
	
	return render(request,'babynames/namepage_fin.html',context)

def namejson(request,name):
	name_info=Name.objects.filter(name_text__exact=name)
	name_list=nameInstance.objects.order_by('sex','year_val').filter(name_text__exact=name)

	mort_list=mortNameInstance.objects.order_by('sex','age').filter(name_text__exact=name)

	if len(name_info)==0:
		name_found=False
	else:
		name_found=True

	yearRange=range(1944,2013)
	ageRange=range(1,70)

	retDic=dict()

	currSex=1
	currYearInd=0
	sexChar='males'
	prevSexChar='males'

	for nameo in name_list:
		prevSexChar=sexChar
		if nameo.sex==1:
			sexChar='males'
		else:
			sexChar='females'
		if retDic.get(nameo.name_text) is None:
			retDic[nameo.name_text]={'males':{'years':[],'ages':[],'ranks':[]},'females':{'years':[],'ages':[],'ranks':[]},'names':[nameo.name_text]}
		if nameo.sex!=currSex:
			currSex=2
			if currYearInd<len(yearRange):
				for j in range(yearRange[currYearInd],2013):
					retDic[nameo.name_text][prevSexChar]['years'].append(0)
					retDic[nameo.name_text][prevSexChar]['ranks'].append(0)
					currYearInd+=1
			currYearInd=0
		if nameo.year_val!=yearRange[currYearInd]:
			for j in range(yearRange[currYearInd],nameo.year_val):
				retDic[nameo.name_text][sexChar]['years'].append(0)
				retDic[nameo.name_text][sexChar]['ranks'].append(0)
				currYearInd+=1
		currYearInd+=1
		retDic[nameo.name_text][sexChar]['years'].append(nameo.frequency)
		retDic[nameo.name_text][sexChar]['ranks'].append(nameo.rank)

	if currYearInd<len(yearRange):
		for j in range(yearRange[currYearInd],2013):
				retDic[name][sexChar]['years'].append(0)
				retDic[name][sexChar]['ranks'].append(0)
				currYearInd+=1

	if len(retDic[name]['males']['years'])==0:
		retDic[name]['males']['years']=[0]*len(yearRange)
		retDic[name]['males']['ranks']=[0]*len(yearRange)

	if len(retDic[name]['females']['years'])==0:
		retDic[name]['females']['years']=[0]*len(yearRange)
		retDic[name]['females']['ranks']=[0]*len(yearRange)

	currSex=1
	currYearInd=0
	sexChar='males'
	prevSexChar='males'

	for nameo in mort_list:
		prevSexChar=sexChar
		if nameo.sex==1:
			sexChar='males'
		else:
			sexChar='females'
		if nameo.sex!=currSex:
			currSex=2
			if currYearInd<len(ageRange):
				for j in range(ageRange[currYearInd],70):
					retDic[nameo.name_text][prevSexChar]['ages'].append(0)
					currYearInd+=1
			currYearInd=0
		if nameo.age!=ageRange[currYearInd]:
			for j in range(ageRange[currYearInd],nameo.age):
				retDic[nameo.name_text][sexChar]['ages'].append(0)
				currYearInd+=1
		currYearInd+=1
		retDic[nameo.name_text][sexChar]['ages'].append(100*nameo.proportion)

	if currYearInd<len(ageRange):
		for j in range(ageRange[currYearInd],70):
				retDic[name][sexChar]['ages'].append(0)
				currYearInd+=1

	if len(retDic[name]['males']['ages'])==0:
		retDic[name]['males']['ages']=[0]*len(yearRange)

	if len(retDic[name]['females']['ages'])==0:
		retDic[name]['females']['ages']=[0]*len(yearRange)

	return HttpResponse(json.dumps(retDic), content_type="application/json")
