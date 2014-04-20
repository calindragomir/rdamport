from django.db import models

class Ship(models.Model):
        
    uid = models.CharField(primary_key=True, max_length=50)

    def __unicode__(self):
        return "Ship {ship_id}".format(ship_id=self.uid)

class Container(models.Model):

    uid = models.CharField(primary_key=True, max_length=50)
    is_flamable = models.BooleanField()
    is_chemical_hazard = models.BooleanField()
    ship = models.ForeignKey(Ship, blank=True, null=True)

    def __unicode__(self):
        return "Container {container_id}".format(container_id=self.uid)

class Dock(models.Model):

    name = models.CharField(max_length=100, blank=False)
    ship = models.OneToOneField(Ship, blank=True, null=True)
  
    def __unicode__(self):
        return self.name

class DockHistory(models.Model):

    dock = models.ForeignKey(Dock)
    ship = models.ForeignKey(Ship)
    date_in = models.DateTimeField(blank=True, null=True)
    date_out = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "{dock} {ship}".format(dock=self.dock, ship=self.ship)

class Employee(models.Model):
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=30)
    is_supervisor = models.BooleanField()
    assigned_to = models.ForeignKey(Dock, blank=True, null=True)

    def __unicode__(self):
        return self.first_name + " " + self.last_name
    

    