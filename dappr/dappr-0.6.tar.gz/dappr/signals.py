from django.dispatch import Signal


user_signed_up = Signal(providing_args=[""])
user_entered_password = Signal(providing_args=[""])
