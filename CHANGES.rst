CHANGES
=======

0.4 (2012-11-10)
----------------
* ``request.vk_api`` with ``vkontakte.API`` instance (thanks Anton Smirnov);
* Workaround for AttributeError in forms.py (thanks Evgeniy Kirov);
* Improved Safari cookie fix (thanks Domantas Jackūnas);
* IFrameFixMiddleware works now if user agent is not set (thanks Evgeniy Kirov).

0.3 (2011-11-28)
----------------

* Auth backend is fixed (thanks Evgeniy Kirov and http://habrahabr.ru/users/Zaharov/);
* improved README;
* IE fix: P3P policy headers are added (thanks Maxim Syabro for suggestion);
* Opera and Safari cookies fix (thanks Evgeniy Kirov);
* alternative OpenAPI authorization (thanks Evgeniy Kirov).

0.2 (2010-10-30)
----------------

* Vkontakte user language is integrated with django i18n. Thanks Vasyl Nakvasiuk.
* Error with InnoDB fixture loading is fixed.

0.1.1 (2010-10-09)
------------------

Bugfix: login was not allowed if user language was unknown.
Full vkontakte language list. Thanks Vasyl Nakvasiuk.

0.1 (2010-09-06)
----------------

The first release
