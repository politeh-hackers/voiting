from django.core.exceptions import ValidationError

from base.service import BaseService
from pages.models import Appeal


class AppealService(BaseService[Appeal]):
    model = Appeal


