from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class events(models.Model):
    name_event = models.TextField(blank=True)
    city = models.CharField(max_length=150, blank=True)
    region = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    cp = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=250, blank=True)
    date_event = models.DateField(blank=True)
    time_event = models.TimeField(blank=True)
    price = models.TextField(blank=True)
    web = models.TextField(blank=True)
    email = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    facebook = models.TextField(blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    lat = models.TextField(blank=True)
    long = models.TextField(blank=True)
    link_register = models.TextField(blank=True)
    description = models.TextField(blank=True)
    type_event = models.TextField(blank=True)
    day_event = models.IntegerField(blank=True)
    month_event = models.IntegerField(blank=True)
    currency = models.CharField(max_length=20, blank=True)
    year_event = models.IntegerField(blank=True)
    short_desc = models.TextField(blank=True)
    distan_txt = models.CharField(max_length=200, blank=True)
    region_l = models.TextField(blank=True)
    category = models.TextField(blank=True)


class users(models.Model):
    id_user_admin = models.ForeignKey(User)
    email = models.TextField(blank=True)
    user = models.CharField(max_length=150, blank=True)
    password = models.TextField(blank=True)
    picture = models.TextField(blank=True)
    name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    date_register = models.DateField(blank=True)
    birth = models.DateField(blank=True)
    favorite = models.CharField(max_length=150,blank=True)
    mailing = models.BooleanField()
    id_facebook = models.TextField(blank=True)
    usr_facebook = models.TextField(blank=True)
    status = models.BooleanField()
    gender = models.CharField(max_length=50, blank=True)
    prefer_km_type =  models.CharField(max_length=50, blank=True)
    prefer_km =  models.CharField(max_length=50, blank=True)
    locale_facebook=models.CharField(max_length=50, blank=True)
    firtsFacebookPic=models.TextField(blank=True)
    auxData=models.TextField(blank=True)
    pic_url=models.TextField(blank=True)
    city=models.TextField(blank=True)
    region=models.TextField(blank=True)
    country=models.TextField(blank=True)
    about=models.TextField(blank=True)





class photos(models.Model):
    id_event = models.ForeignKey(events)
    id_user_admin = models.ForeignKey(User)
    file = models.TextField(blank=True)
    pic_url = models.TextField(blank=True)
    date = models.DateField(blank=True)
    title = models.TextField(blank=True)
    subtitle = models.TextField(blank=True)
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    status = models.IntegerField(blank=True)
    json = models.TextField(blank=True)


class comments_events(models.Model):
    id_event = models.ForeignKey(events)
    id_user_admin = models.ForeignKey(User)
    calif = models.IntegerField(blank=True)
    title_comment = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    date = models.DateField(blank=True)
    year_run = models.IntegerField(blank=True)
    hidr = models.IntegerField(blank=True)
    org = models.IntegerField(blank=True)
    route = models.IntegerField(blank=True)
    toilets = models.IntegerField(blank=True)
    parking = models.IntegerField(blank=True)
    enviroment = models.IntegerField(blank=True)
    music = models.IntegerField(blank=True)
    medl = models.IntegerField(blank=True)
    meta = models.IntegerField(blank=True)
    salida = models.IntegerField(blank=True)
    cer = models.IntegerField(blank=True)
    status=models.IntegerField(blank=True)
    participado = models.IntegerField(blank=True)
    seguridad = models.IntegerField(blank=True)



class events_favorites(models.Model):
     id_event = models.ForeignKey(events)
     id_user_admin = models.ForeignKey(User)
     date = models.DateField(blank=True)


class countries(models.Model):

        country_id = models.IntegerField(blank=True)
        name_en = models.TextField(blank=True)

class Meta:
    ordening = ('created',)