from django.db import models

# Create your models here.
from django.db.models import CharField, DateField, DateTimeField, AutoField, OneToOneField, ForeignKey, BigIntegerField, PositiveSmallIntegerField


class BloodType(models.Model):
    bloodtypeid = AutoField(primary_key=True)
    bloodtype = CharField(max_length=4, unique=True)

    class Meta:
        db_table = "donor_bloodtype"

    def __str__(self):
        return u"bloodtypeid:{}".format(self.bloodtypeid)


class BloodVolume(models.Model):
    bloodvolumeid = AutoField(primary_key=True)
    bloodvolume = PositiveSmallIntegerField(unique=True)

    class Meta:
        db_table = "donor_bloodvolume"

    def __str__(self):
        return u"bloodvolumeid:{}".format(self.bloodvolumeid)


class BloodComponent(models.Model):
    bloodcomponentid = AutoField(primary_key=True)
    bloodcomponent = CharField(max_length=4, unique=True)

    class Meta:
        db_table = "donor_bloodcomponent"

    def __str__(self):
        return u"bloodcomponentid:{}".format(self.bloodcomponentid)


class Donor(models.Model):
    donorid = CharField(primary_key=True, max_length=18)
    donorname = CharField(max_length=4)
    sex = CharField(max_length=1)
    birth = DateField(auto_now=False, auto_now_add=False)
    bloodtype = ForeignKey(BloodType, on_delete=models.CASCADE)
    create = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "donor_donor"

    def __str__(self):
        return u"donorid:{}".format(self.donorid)


class Person(models.Model):
    donor = OneToOneField(Donor, on_delete=models.CASCADE)
    mobile = BigIntegerField(unique=True)
    address = CharField(max_length=50)
    modify = DateTimeField(auto_now=True)
    personresponsible = CharField(max_length=50)

    class Meta:
        db_table = "donor_person"

    def __str__(self):
        return u"donor:{}".format(self.donor.donorid)


class Blood(models.Model):
    bloodid = AutoField(primary_key=True)
    blooddonor = ForeignKey(Donor, on_delete=models.CASCADE)
    bloodplace = CharField(max_length=50)
    bloodvolume = ForeignKey(BloodVolume, on_delete=models.CASCADE)
    bloodcomponent = ForeignKey(BloodComponent, on_delete=models.CASCADE)
    bloodcreate = DateField(auto_now=False, auto_now_add=False)
    bloodmodify = DateTimeField(auto_now=True)
    bloodresponsible = CharField(max_length=50)

    class Meta:
        db_table = "donor_blood"

    def __str__(self):
        return u"donor:{}".format(self.bloodid)


# 各整数类型取值范围
# class BaseDatabaseOperations(object):
#     """
#     This class encapsulates all backend-specific differences, such as the way
#     a backend performs ordering or calculates the ID of a recently-inserted
#     row.
#     """
#     compiler_module = "django.db.models.sql.compiler"
#
#     # Integer field safe ranges by `internal_type` as documented
#     # in docs/ref/models/fields.txt.
#     integer_field_ranges = {
#         'SmallIntegerField': (-32768, 32767),
#         'IntegerField': (-2147483648, 2147483647),
#         'BigIntegerField': (-9223372036854775808, 9223372036854775807),
#         'PositiveSmallIntegerField': (0, 32767),
#         'PositiveIntegerField': (0, 2147483647),
#     }