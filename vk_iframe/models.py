#coding: utf-8
from django.db import models
from django.db.models import CharField, URLField, ForeignKey, NullBooleanField, IntegerField
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

class Country(models.Model):
    title = CharField(u'Название', max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.title or u'[%s]' % self.pk

    class Meta:
        verbose_name = u'[vk] Страна'
        verbose_name_plural = u'[vk] Страны'
        ordering = ['id']


class City(models.Model):
    title = CharField(u'Название', max_length=100, null=True, blank=True)
    country = ForeignKey(Country, null=True, blank=True)

    def __unicode__(self):
        return self.title or u'[%s]' % self.pk

    class Meta:
        verbose_name = u'[vk] Город'
        verbose_name_plural = u'[vk] Города'
        ordering = ['id']


class Profile(models.Model):
    GENDER_CHOICES = (
        (2, u'Мужской',),
        (1, u'Женский',),
        (0, u'Без указания пола',),
    )
    user =          AutoOneToOneField(User, primary_key=True, related_name = 'vk_profile')
    nickname =      CharField(u'nick', max_length=100, blank=True, null=True)
    domain =        CharField(u'Адрес в url', max_length=50, blank=True, null=True)
    sex =           IntegerField(u'Пол', blank=True, null=True, choices = GENDER_CHOICES)
    bdate =         CharField(u'Дата рождения', max_length=10, blank=True, null=True)

    city =          ForeignKey(City, blank=True, null=True)
    country =       ForeignKey(Country, blank=True, null=True)
    timezone =      IntegerField(u'Часовой пояс', blank=True, null=True)

    photo =         URLField(blank=True, null=True, verify_exists=False)
    photo_medium =  URLField(blank=True, null=True, verify_exists=False)
    photo_big =     URLField(blank=True, null=True, verify_exists=False)
    photo_rec =     URLField(blank=True, null=True, verify_exists=False)

    rate =          IntegerField(u'Рейтинг', blank=True, null=True)
    has_mobile =    NullBooleanField(u'Есть сотовый', blank=True, null=True)
    home_phone =    CharField(u'Домашний телефон', max_length=30, blank=True, null=True)
    mobile_phone =  CharField(u'Сотовый телефон', max_length=30, blank=True, null=True)

    university =    IntegerField(u'Университет (id)', blank=True, null=True)
    university_name = CharField(u'Университет', max_length=50, blank=True, null=True)
    faculty =       IntegerField(u'Факультет (id)', blank=True, null=True)
    faculty_name =  CharField(u'Факультет', max_length=50, blank=True, null=True)
    graduation =    CharField(u'Год выпуска', max_length=4, blank=True, null=True)

    class Meta:
        verbose_name = u'[vk] Данные о пользователе'
        verbose_name_plural = u'[vk] Данные о пользователях'
