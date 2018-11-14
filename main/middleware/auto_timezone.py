from django.utils import timezone


class UserTimezoneAutoSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            timezone.activate(timezone.FixedOffset(request.user.timezone_offset))

        response = self.get_response(request)

        return response
