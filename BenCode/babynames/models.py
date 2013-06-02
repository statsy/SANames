from django.db import models

class Name(models.Model):
	name_text=models.CharField(max_length=100)
	male_num=models.IntegerField(default=0)
	female_num=models.IntegerField(default=0)
	total_num=models.IntegerField(default=0)

	def __unicode__(self):
		return self.name_text

class Year(models.Model):
	year_date=models.DateField()
	male_num=models.IntegerField(default=0)
	female_num=models.IntegerField(default=0)
	total_num=models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.year_date.year)

class nameInstance(models.Model):
	MALE=1
	FEMALE=2
	sexChoices=(
		(MALE,'Male'),
		(FEMALE,'Female'),
		)
	name=models.ForeignKey(Name)
	year=models.ForeignKey(Year)
	sex=models.IntegerField(choices=sexChoices)
	frequency=models.IntegerField(default=0)
	name_text=models.CharField(max_length=100)
	year_val=models.IntegerField()
	proportion=models.FloatField()
	rank=models.IntegerField()

class mortNameInstance(models.Model):
	MALE=1
	FEMALE=2
	sexChoices=(
		(MALE,'Male'),
		(FEMALE,'Female'),
		)
	name=models.ForeignKey(Name)
	age=models.IntegerField()
	sex=models.IntegerField(choices=sexChoices)
	frequency=models.FloatField(default=0)
	name_text=models.CharField(max_length=100)
	total_frequency=models.FloatField()
	proportion=models.FloatField()

	def __unicode__(self):
		return "Name: {0} \n Year: {1} \n Sex: {2} \n Frequency: {3}".format(name,year,sex,frequency)

