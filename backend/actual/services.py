from base.service import BaseService
from .models import Actual

class ActualService(BaseService):

    def __init__(self, model=Actual):
        self.model = model
