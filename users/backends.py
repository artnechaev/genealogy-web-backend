from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class UsernameAuthBackend(ModelBackend):
    """Backend для аутентификации по username и password"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = user_model.objects.get(username=username)
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            user_model().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
