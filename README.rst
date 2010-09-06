=======================
django-vkontakte-iframe
=======================

Django app for developing vk.com (aka vkontakte.ru largest,
Russian social network) iframe applications.

Handles user authentication and registration.

Installation
============

::

    $ pip install django-vkontakte-iframe


Requirements
============

* django-annoying for AutoOneToOneField

Optional:

* vkontakte >= 0.9.4.1 for populating cities and countries info via admin action
* django-webtest >= 1.2.2 for tests

Usage
=====

1. Register and configure vkontakte iframe application here:
   http://vkontakte.ru/apps.php?act=add

2. Add your app's settings to settings.py::

        VK_APP_ID = '1234567'                   # Application ID
        VK_APP_KEY = 'M1gytuHwni'               # Application key
        VK_APP_SECRET = 'MiRFwrDYwcYFCTD18EcY'  # Secure key

3. Add 'vk_iframe' to INSTALLED_APPS

4. Add 'vk_iframe.backends.VkontakteUserBackend' to AUTHENTICATION_BACKENDS::

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'vk_iframe.backends.VkontakteUserBackend',
        )


5. Put 'vk_iframe.middleware.AuthenticationMiddleware' and
   'vk_iframe.middleware.LoginRequiredMiddleware' to the end of MIDDLEWARE_CLASSES::

        MIDDLEWARE_CLASSES = [
            # ...
            'vk_iframe.middleware.AuthenticationMiddleware',
            'vk_iframe.middleware.LoginRequiredMiddleware',
        ]

   Vkontakte visitors will be automatically registered and authorized as django
   users (username == vkontakte user id).

   LoginRequiredMiddleware is an optional. It returns 403 for all unauthorized
   requests with urls not listed in settings.PUBLIC_URLS. You should
   enable it for security reasons. Example of PUBLIC_URLS::

        PUBLIC_URLS = [
            '^admin/$',
            '^my-callback/',
        ]


6. Run ``python ./manage.py syncdb`` (or ``python ./manage.py migrate vk_iframe`` if
   South is used)

7. Optional: load initial geo data (cities and countries)::

      python manage loaddata vk-geo

8. If you want to store more user data then put the following line as
   the 'First API request' ('Первый запрос к API') option (in your app edit
   page at vkontakte.ru)::

        method=getProfiles&uids={viewer_id}&format=json&v=3.0&fields=uid,first_name,last_name,nickname,domain,sex,bdate,city,country,timezone,photo,photo_medium,photo_big,has_mobile,rate,contacts,education

9. That's all. All your app's visitors are now registered and authenticated
   django users. Additional profile data is available as user.vk_profile.

