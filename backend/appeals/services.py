from base.service import BaseService
from .models import Appeal

class AppealService(BaseService):

    def __init__(self, model=Appeal):
        self.model = model
