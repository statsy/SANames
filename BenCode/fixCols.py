import csv, os, datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "babyexplorer.settings")
from babynames.models import Name, Year, nameInstance

# allInstances=nameInstance.objects.all()

# allCool=Name.objects.all()

# for nam in allCool:
# 	nameText=nam.name_text
# 	nameInstance.objects.filter(name__name_text=nameText).update(name_text=nameText)

allYarr=Year.objects.all()

for yar in allYarr:
	maley=yar.male_num
	femaley=yar.female_num
	nameInstance.objects.filter(year__year_date__year=yearText).update()

# for ai in allInstances:
# 	aiyearval=ai.year.year_date.year
# 	ainametext=ai.name.name_text
# 	ai.year_val=ai.year.year_date.year
# 	ai.name_text=ai.name.name_text
# 	ai.save(force_update=True)