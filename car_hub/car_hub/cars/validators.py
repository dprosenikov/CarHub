from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year_range(value):
    current_year = datetime.now().year
    if not (1886 <= value <= current_year):
        raise ValidationError(f'Year must be in range 1886 - {current_year}')
