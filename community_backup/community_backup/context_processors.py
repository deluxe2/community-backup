from django.conf import settings


def release_version(_request):
    return {
        "RELEASE_VERSION": settings.RELEASE_VERSION,
    }

def additional_footer_nav_items(_request):
    return {
        "ADDITIONAL_FOOTER_NAV_ITEMS": settings.ADDITIONAL_FOOTER_NAV_ITEMS,
    }
