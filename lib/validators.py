from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from datetime import datetime


def validate_rate(rate):
    if rate < 0 or rate > 5:
        raise ValidationError(_("Invalid rate"))


def validated_date(date):
    if date < datetime.now().date():
        raise ValidationError(_("Inavlid Date"))
