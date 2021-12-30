from django.core import validators


class CodeValidators(validators.RegexValidator):
    regex = '^.{10}$'
    message = (
        'Enter a valid code.'
    )
    flags = 0

class PhoneValidator(validators.RegexValidator):

    regex = '^\+?1?\d{9,11}$'
    message = (
        'Enter a valid phone number.'
    )
    flags = 0
