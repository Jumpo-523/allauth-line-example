import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class CustomUsernameValidator(validators.RegexValidator):
    # regex = r'^[\w.@+-]+\Z'
    regex = r''
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = re.ASCII


custom_username_validators = [CustomUsernameValidator()]

