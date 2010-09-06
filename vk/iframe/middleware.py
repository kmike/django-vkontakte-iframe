#coding: utf-8
import re
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden
from django.conf import settings
from vk.iframe.forms import VkontakteIframeForm
from django.shortcuts import render_to_response

class AuthenticationMiddleware(object):

    def process_request(self, request):

        # все неправильно настроено
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The vk.middleware.AuthenticationMiddleware requires the"
                " Django authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the vk.middleware.AuthenticationMiddleware class.")

        # не было попытки авторизоваться через Вконтакте
        if 'viewer_id' not in request.GET:
            return

        # пользователь уже залогинен под тем же именем
        if request.user.is_authenticated():
            if request.user.username == request.GET['viewer_id']:
                return

        # пользователь не залогинен или залогинен под другим именем
        vk_form = VkontakteIframeForm(request.GET)
        user = auth.authenticate(vk_form = vk_form)
        if user:
            request.user = user
            auth.login(request, user)
        else:
            request.META['VKONTAKTE_LOGIN_ERRORS'] = vk_form.errors


PUBLIC_URLS = [re.compile(url) for url in getattr(settings, 'PUBLIC_URLS', [])]

class LoginRequiredMiddleware(object):
    def process_request(self, request):

        if request.path.startswith(settings.MEDIA_URL):
            return

        if request.user.is_anonymous():
            path = request.path.lstrip('/')
            for url in PUBLIC_URLS:
                if re.match(url, path):
                    return
            return HttpResponseForbidden(render_to_response(['vk/403.html', '403.html', 'vk/default/403.html']))
