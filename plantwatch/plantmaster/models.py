# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Plants(models.Model):
    plantid = models.TextField(primary_key=True, unique=True)
    plantname = models.TextField(blank=True, null=True)
    federalstate = models.TextField(blank=True, null=True)
    energysource = models.TextField(blank=True, null=True)
    chp = models.TextField(blank=True, null=True)
    latestexpanded = models.IntegerField(blank=True, null=True)
    initialop = models.IntegerField(blank=True, null=True)
    totalpower = models.FloatField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    blockcount = models.IntegerField(blank=True, null=True)
    company = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    activepower = models.FloatField(blank=True, null=True)
    energy_2015 = models.IntegerField(blank=True, null=True)
    energy_2016 = models.IntegerField(blank=True, null=True)
    energy_2017 = models.IntegerField(blank=True, null=True)
    energy_2018 = models.IntegerField(blank=True, null=True)
    energy_2019 = models.IntegerField(blank=True, null=True)
    energy_2020 = models.IntegerField(blank=True, null=True)
    energy_2021 = models.IntegerField(blank=True, null=True)
    #energy_2022 = models.IntegerField(blank=True, null=True)
    co2_2007 = models.IntegerField(blank=True, null=True)
    co2_2008 = models.IntegerField(blank=True, null=True)
    co2_2009 = models.IntegerField(blank=True, null=True)
    co2_2010 = models.IntegerField(blank=True, null=True)
    co2_2011 = models.IntegerField(blank=True, null=True)
    co2_2012 = models.IntegerField(blank=True, null=True)
    co2_2013 = models.IntegerField(blank=True, null=True)
    co2_2014 = models.IntegerField(blank=True, null=True)
    co2_2015 = models.IntegerField(blank=True, null=True)
    co2_2016 = models.IntegerField(blank=True, null=True)
    co2_2017 = models.IntegerField(blank=True, null=True)
    co2_2018 = models.IntegerField(blank=True, null=True)
    co2_2019 = models.IntegerField(blank=True, null=True)
    co2_2020 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plants'

class Blocks(models.Model):
    blockid = models.TextField(unique=True, primary_key=True, db_column="blockid")
    plantid = models.ForeignKey(Plants, models.DO_NOTHING, db_column='plantid', related_name='blocks')
    blockname = models.TextField(blank=True, null=True)
    federalstate = models.TextField(blank=True, null=True)
    energysource = models.TextField(blank=True, null=True)
    initialop = models.IntegerField(blank=True, null=True)
    chp = models.TextField(blank=True, null=True)
    # = models.TextField(blank=True, null=True)
    netpower = models.FloatField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    endop = models.IntegerField(blank=True, null=True)
    company = models.TextField(blank=True, null=True)
    reserveyear = models.IntegerField(null=True)
    
    class Meta:
        managed = False
        db_table = 'blocks'

class Addresses(models.Model):
    blockid = models.OneToOneField(Blocks, models.DO_NOTHING, db_column='blockid', unique=True, primary_key=True)  # Field name made lowercase.
    federalstate = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    plz = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    street = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'

class Power(models.Model):
    powerid = models.IntegerField(unique=True, primary_key=True)
    producedat = models.DateTimeField()
    blockid = models.OneToOneField(Blocks, models.DO_NOTHING, db_column='blockid', unique=True)  # Field name made lowercase.
    power = models.IntegerField(null=False)
    
    class Meta:
        managed = False
        db_table = 'power'

class Month(models.Model):
    monthid = models.IntegerField(unique=True, primary_key=True)
    year = models.IntegerField()
    month = models.IntegerField()
    blockid = models.OneToOneField(Blocks, models.DO_NOTHING, db_column='blockid', unique=True)  # Field name made lowercase.
    power = models.IntegerField(null=False)
    
    class Meta:
        managed = False
        db_table = 'month'
        unique_together = ('blockid', 'year', 'month')

class Pollutions(models.Model):
    pollutionsid = models.IntegerField(unique=True, primary_key=True)
    year = models.IntegerField()
    plantid = models.ForeignKey(Plants, models.DO_NOTHING, db_column='plantid')
    pollutant = models.TextField()
    releasesto = models.TextField(blank=True, null=True)
    amount = models.FloatField(db_column="amount", blank=True, null=True)
    amount2 = models.FloatField(db_column="amount2", blank=True, null=True)
    unit2 = models.TextField(db_column="unit2", blank=True, null=True)
    exponent = models.IntegerField(db_column="potency", blank=True, null=True)
    pollutant2 = models.TextField()

    class Meta:
        managed = False
        db_table = 'pollutions'
        unique_together = ('plantid', 'releasesto', 'pollutant', 'year')

'''
class Mtp(models.Model):
    mtpid = models.IntegerField(unique=True, primary_key=True)
    plantid = models.ForeignKey(Plants, models.DO_NOTHING, db_column='plantid', unique=True)  # Field name made lowercase.
    power = models.IntegerField(null=False)
    producedat = models.DateTimeField()
    
    class Meta:
        managed = False
        db_table = 'mtp'
        unique_together = ('plantid', 'producedat')

class Monthp(models.Model):
    monthpid = models.IntegerField(unique=True, primary_key=True)
    year = models.IntegerField()
    month = models.IntegerField()
    plantid = models.ForeignKey(Plants, models.DO_NOTHING, db_column='plantid')  # Field name made lowercase.
    power = models.IntegerField(null=False)
    
    class Meta:
        managed = False
        db_table = 'monthp'
        unique_together = ('plantid', 'year', 'month')

'''

class Yearly(models.Model):
    yid = models.IntegerField(unique=True, primary_key=True)
    year = models.IntegerField()
    plantid = models.OneToOneField(Plants, models.DO_NOTHING, db_column='plantid', unique=True)  # Field name made lowercase.
    power = models.IntegerField(null=False)
    
    class Meta:
        managed = False
        db_table = 'yearly'
        unique_together = ('plantid', 'year')


