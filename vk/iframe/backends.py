#coding: utf-8
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from vk.iframe.models import City, Country

class VkontakteUserBackend(ModelBackend):
    """ Использовать вместе с vk.middleware.AuthenticationMiddleware """

    def authenticate(self, vk_form):

        if not vk_form:
            return

        if not vk_form.is_valid():
            return

        defaults = {}
        username = str(vk_form.cleaned_data['viewer_id'])
        vk_profile = vk_form.profile_api_result()
        if vk_profile:
            defaults = dict(
                first_name = vk_profile['first_name'],
                last_name = vk_profile['last_name'],
            )

        user, created = User.objects.get_or_create(username=username, defaults=defaults)
        if created:
            user = self.configure_user(vk_profile, user)
        return user

    def configure_user(self, vk_profile, user):
        user_profile = user.vk_profile
        for key in vk_profile:
            if key not in ['city', 'country']:
                setattr(user_profile, key, vk_profile[key])

        country_id = vk_profile.get('country', None)
        if country_id:
            country, created = Country.objects.get_or_create(id=country_id)
            user_profile.country = country

        city_id = vk_profile.get('city', None)
        if city_id:
            city, created = City.objects.get_or_create(id=city_id, defaults={'country_id': country_id})
            user_profile.city = city

        user_profile.save()
        return user
