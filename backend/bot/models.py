from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from plans.models import Quota
from plans.models import Plan
import uuid
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=16, blank=True, null=True)
    justeatemail = models.CharField(max_length=255, blank=True, null=True)
    justeatpw = models.CharField(max_length=255, blank=True, null=True)
    mon_time_from = models.TimeField(default=datetime.time(00, 00))
    mon_time_to   = models.TimeField(default=datetime.time(23, 59))
    tue_time_from = models.TimeField(default=datetime.time(00, 00))
    tue_time_to = models.TimeField(default=datetime.time(23, 59))
    wed_time_from = models.TimeField(default=datetime.time(00, 00))
    wed_time_to = models.TimeField(default=datetime.time(23, 59))
    thu_time_from = models.TimeField(default=datetime.time(00, 00))
    thu_time_to = models.TimeField(default=datetime.time(23, 59))
    fri_time_from = models.TimeField(default=datetime.time(00, 00))
    fri_time_to = models.TimeField(default=datetime.time(23, 59))
    sat_time_from = models.TimeField(default=datetime.time(00, 00))
    sat_time_to = models.TimeField(default=datetime.time(23, 59))
    sun_time_from = models.TimeField(default=datetime.time(00, 00))
    sun_time_to = models.TimeField(default=datetime.time(23, 59))
    mon_time_toggle = models.BooleanField(default=True)
    tue_time_toggle = models.BooleanField(default=True)
    wed_time_toggle = models.BooleanField(default=True)
    thu_time_toggle = models.BooleanField(default=True)
    fri_time_toggle = models.BooleanField(default=True)
    sat_time_toggle = models.BooleanField(default=True)
    sun_time_toggle = models.BooleanField(default=True)
    email_notif = models.CharField(max_length=255, blank=True, null=True)
    email_notif_toggle = models.BooleanField(default=True)
    mobile_notif = models.CharField(max_length=16, blank=True, null=True)  
    mobile_notif_toggle = models.BooleanField(default=True)
    referral_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, related_name="referrals", on_delete=models.SET_NULL)
    open_runs_toggle = models.BooleanField(default=True)
    overflows_toggle = models.BooleanField(default=True)    
    stripe_customer_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    thread_toggle = models.BooleanField(default=False)
    bw_count = models.IntegerField(default=0)
    bm_count = models.IntegerField(default=0)
    pw_count = models.IntegerField(default=0)
    pm_count = models.IntegerField(default=0)
    def get_referred_by(self):
        # You can generate a custom referral code here if needed
        return self.referred_by


class Zone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zones')  # Relationship to the User model    
    id = models.AutoField(primary_key=True)
    zone_id = models.CharField(max_length=50, unique=False)  # non Unique identifier for the zone
    zone_name = models.CharField(max_length=255)  # Name of the zone
    zone_toggle = models.BooleanField(default=True)  # Boolean field for toggling the zone (True/False)

    def __str__(self):
        return f"{self.zone_name} ({self.zone_id}) - {'Active' if self.zone_toggle else 'Inactive'}"
