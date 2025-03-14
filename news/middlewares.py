import uuid


class UniqueUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.COOKIES.get("unique_user_id")

        if not user_id:
            user_id = str(uuid.uuid4())

        request.unique_user_id = user_id  # Attach to request for use in views

        response = self.get_response(request)

        # If the user didn't have an ID, set the cookie in the response
        if "unique_user_id" not in request.COOKIES:
            response.set_cookie(
                "unique_user_id", user_id, max_age=31536000, httponly=True, samesite='Lax'
            )  # 1 year expiration

        return response
