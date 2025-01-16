from base.service import BaseService
from .models import Media

class MediaService(BaseService):

    def __init__(self, model=Media):
        self.model = model
