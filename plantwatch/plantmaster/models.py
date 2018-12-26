# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Addresses(models.Model):
    blockid = models.TextField(unique=True, primary_key=True)
    federalstate = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    plz = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    street = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'


class Blocks(models.Model):
    plantid = models.TextField(blank=True, null=True)
    # plantid = models.ForeignKey related_name="ablockstest")  # Field name made lowercase.
    blockid = models.OneToOneField(Addresses, models.DO_NOTHING, db_column='blockid', unique=True, primary_key=True)  # Field name made lowercase.
    federalstate = models.TextField(blank=True, null=True)
    energysource = models.TextField(blank=True, null=True)
    initialop = models.IntegerField(blank=True, null=True)
    chp = models.TextField(blank=True, null=True)
    blockname = models.TextField(blank=True, null=True)
    netpower = models.FloatField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    endop = models.TextField(blank=True, null=True)
    company = models.TextField(blank=True, null=True)
    fullload = models.FloatField(blank=True, null=True)
    ophours = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blocks'


class Plants(models.Model):
    plantid = models.OneToOneField(Blocks, models.DO_NOTHING, db_column='plantid', unique=True, primary_key=True)
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

    class Meta:
        managed = False
        db_table = 'plants'


class Pollutions(models.Model):
    plantid = models.ForeignKey(Plants, models.DO_NOTHING, db_column='plantid')
    releases_to = models.TextField(blank=True, null=True)
    pollutant = models.TextField()
    amount = models.FloatField(blank=True, null=True)
    potency = models.IntegerField(blank=True, null=True)
    unit = models.TextField(db_column="unit_2", blank=True, null=True)
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pollutions'
        unique_together = (('plantid', 'releases_to', 'pollutant', 'year'),)
