# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Addresses(models.Model):
    blockid = models.ForeignKey('Blocks', models.DO_NOTHING, db_column='BlockID', unique=True)  # Field name made lowercase.
    federalstate = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    plz = models.IntegerField(db_column='PLZ', blank=True, null=True)  # Field name made lowercase.
    street = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'


class Blocks(models.Model):
    kraftwerkid = models.TextField(db_column='KraftwerkID', blank=True, null=True)  # Field name made lowercase.
    blockid = models.TextField(db_column='BlockID', unique=True)  # Field name made lowercase.
    blockname = models.TextField(blank=True, null=True)
    federalstate = models.TextField(blank=True, null=True)
    energysource = models.TextField(blank=True, null=True)
    initialop = models.IntegerField(blank=True, null=True)
    chp = models.TextField(blank=True, null=True)
    netpower = models.FloatField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    endop = models.TextField(blank=True, null=True)
    company = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blocks'
