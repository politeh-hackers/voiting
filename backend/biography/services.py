from base.service import BaseService
from .models import Biography

class BiographyService(BaseService):

    def __init__(self, model=Biography):
        self.model = model
