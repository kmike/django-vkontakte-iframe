#coding: utf-8
import re
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response
from vk_iframe.forms import VkontakteIframeForm

try:
    import vkontakte
    use_vkontakte_pkg = True
except ImportError:
    use_vkontakte_pkg = False

DEFAULT_P3P_POLICY = 'IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT'
P3P_POLICY = getattr(settings, 'VK_P3P_POLICY', DEFAULT_P3P_POLICY)

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

        def patch_request_with_vkapi(user):
            if hasattr(request, 'session') and use_vkontakte_pkg:
                token = request.session['vk_startup_vars']['access_token']
                setattr(request,'vk_api',vkontakte.API(token = token))

        # не было попытки авторизоваться через Вконтакте
        if 'viewer_id' not in request.GET:
            patch_request_with_vkapi(request.user)
            return

        # пользователь уже залогинен под тем же именем
        if request.user.is_authenticated():
            if request.user.username == request.GET['viewer_id']:
                patch_request_with_vkapi(request.user)
                return

        # пользователь не залогинен или залогинен под другим именем
        vk_form = VkontakteIframeForm(request.GET)

        user = auth.authenticate(vk_form=vk_form)
        if user:
            request.user = user
            auth.login(request, user)

            if hasattr(request, 'session'):
                # устанавливаем язык пользователя
                lang_code = vk_form.language_code()
                if lang_code:
                    request.session['django_language'] = lang_code

                # сохраняем начальные параметры, тк там точно есть что то полезное
                startup_vars = vk_form.cleaned_data
                del startup_vars['api_result'] # этот большой кусок сохранять в сессию не будем, он уже есть в vk_profile
                request.session['vk_startup_vars'] = startup_vars

            patch_request_with_vkapi(request.user)

        else:
            request.META['VKONTAKTE_LOGIN_ERRORS'] = vk_form.errors


class IFrameFixMiddleware(object):

    def process_request(self, request):
        """
        Safari and Opera default security policies restrict cookie setting in first request in iframe.
        Solution is to create hidden form to preserve GET variables and REPOST it to current URL.

        Inspired by https://gist.github.com/796811 and https://gist.github.com/1511039.
        """
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        browser_is_safari = 'Safari' in user_agent and 'Chrome' not in user_agent
        browser_is_opera = 'Opera' in user_agent
        first_request = 'sessionid' not in request.COOKIES and 'cookie_fix' not in request.GET
        iframe_auth = 'api_id' in request.GET

        if (browser_is_safari or browser_is_opera) and first_request and iframe_auth:
            html = """<html><body><form name='cookie_fix' method='GET' action='.'>"""
            for item in request.GET:
                html += "<input type='hidden' value='%s' name='%s' />" % (request.GET[item], item)
            html += "<input type='hidden' name='cookie_fix' value='1' />"
            html += "</form>"
            html += '''<script type="text/javascript">document.cookie_fix.submit()</script></html>'''
            return HttpResponse(html)

    def process_response(self, request, response):
        """
        P3P policy for Internet Explorer.
        """
        response["P3P"] = 'CP="%s"' % P3P_POLICY
        return response


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
            return HttpResponseForbidden(render_to_response(['vk_iframe/403.html', '403.html', 'vk_iframe/default/403.html']))
