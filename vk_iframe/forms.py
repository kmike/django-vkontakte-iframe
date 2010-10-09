#coding: utf-8
from hashlib import md5
from django import forms
from django.conf import settings
from django.utils import simplejson as json
from vk_iframe.languages import LANGUAGES

VIEWER_TYPES_GROUP = (
    (3, u'пользователь является администратором группы'),
    (2, u'пользователь является руководителем группы'),
    (1, u'пользователь является участником группы'),
    (0, u'пользователь не состоит в группе'),
)

VIEWER_TYPES_USER = (
    (3, u'пользователь является администратором группы'),
    (2, u'пользователь является руководителем группы'),
    (1, u'пользователь является участником группы'),
    (0, u'пользователь не состоит в группе'),
)

REFERRER_CHOICES = (
    ('menu', u'приложение запущено в результате перехода через левое меню'),
    ('wall_post_inline', 'приложение запущено через меню публикации новой записи на стене'),
    ('wall_post', 'приложение запущено через меню публикации новой записи на стене и развернуто в новом окне'),
    ('wall_view_inline', 'приложение запущено со стены пользователя для просмотра ранее размещенной записи'),
    ('wall_view', 'приложение запущено со стены пользователя для просмотра ранее размещенной записи и развернуто в новом окне'),
)

class VkontakteIframeForm(forms.Form):

    # адрес сервиса API, по которому необходимо осуществлять запросы
    api_url = forms.CharField()

    # id запущенного приложения
    api_id = forms.IntegerField()

    # id пользователя, со страницы которого было запущено приложение.
    # Если приложение запущено не со страницы пользователя, то значение равно 0.
    user_id = forms.IntegerField()

    # id сессии для осуществления запросов к API
    sid = forms.CharField()

    # Секрет, необходимый для осуществления подписи запросов к API
    secret = forms.CharField()

    # id группы, со страницы которой было запущено приложение.
    # Если приложение запущено не со страницы группы, то значение равно 0.
    group_id = forms.IntegerField()

    # id пользователя, который просматривает приложение.
    viewer_id = forms.IntegerField()

    # если пользователь установил приложение – 1, иначе – 0.
    is_app_user = forms.BooleanField(required=False)

    # тип пользователя, который просматривает приложение
    viewer_type = forms.IntegerField()

    # ключ, необходимый для авторизации пользователя на стороннем сервере
    auth_key = forms.CharField()

    # id языка пользователя, просматривающего приложение
    language = forms.ChoiceField(LANGUAGES)

    # результат первого API-запроса, который выполняется при загрузке приложения
    api_result = forms.CharField(required = False)

    # битовая маска настроек текущего пользователя в данном приложении
    # TODO: подробнее см. в описании метода getUserSettings
    api_settings = forms.CharField()

    # строка с информацией о том, откуда было запущено приложение
    referrer = forms.ChoiceField(REFERRER_CHOICES, required=False)

    # id пользователя, разместившего запись на стене
    poster_id = forms.IntegerField(required=False)

    # id сохраненной на стене записи
    post_id = forms.IntegerField(required=False)

    def get_auth_key(self):
        api_id = self.cleaned_data['api_id']
        viewer_id = self.cleaned_data['viewer_id']
        api_secret = settings.VK_APP_SECRET
        return md5(str(api_id) + '_' + str(viewer_id) + '_' + str(api_secret)).hexdigest()

    def clean_app_id(self):
        if str(self.cleaned_data['app_id']) != str(settings.VK_APP_ID):
            raise forms.ValidationError(u'app_id - от другого приложения')
        return self.cleaned_data['app_id']

    def clean_auth_key(self):
        correct_key = self.get_auth_key().lower()
        key = self.cleaned_data['auth_key'].lower()
        if correct_key != key:
            raise forms.ValidationError(u'Неверный ключ авторизации: %s != %s' % (key, correct_key,))
        return self.cleaned_data['auth_key']

    def profile_api_result(self):
        # в настройках нужно указать "Первый запрос к API":
        # method=getProfiles&uids={viewer_id}&format=json&v=3.0&fields=uid,first_name,last_name,nickname,domain,sex,bdate,city,country,timezone,photo,photo_medium,photo_big,has_mobile,rate,contacts,education
        api_result = self.cleaned_data['api_result']
        if api_result:
            return json.loads(api_result)['response'][0]
        return {}
