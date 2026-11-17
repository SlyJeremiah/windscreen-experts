from django.conf import settings


def site_settings(request):
    return {'ga_id': settings.GA_MEASUREMENT_ID}
