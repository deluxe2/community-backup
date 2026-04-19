from django.conf import settings


def release_version(_request):
    return {
        "RELEASE_VERSION": settings.RELEASE_VERSION,
    }
