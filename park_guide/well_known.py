from django.conf import settings
from django.http import HttpResponse, JsonResponse


def _assetlinks_file_path():
    return settings.BASE_DIR / '.well-known' / 'assetlinks.json'


def assetlinks_json(request):
    assetlinks_path = _assetlinks_file_path()
    if assetlinks_path.exists():
        return HttpResponse(assetlinks_path.read_text(encoding='utf-8'), content_type='application/json')

    payload = [
        {
            "relation": [
                "delegate_permission/common.handle_all_urls",
                "delegate_permission/common.get_login_creds",
            ],
            "target": {
                "namespace": "android_app",
                "package_name": settings.PASSKEY_ANDROID_PACKAGE_NAME,
                "sha256_cert_fingerprints": [settings.PASSKEY_ANDROID_SHA256],
            },
        }
    ]
    return JsonResponse(payload, safe=False)
