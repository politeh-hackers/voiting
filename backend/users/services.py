from base.service import BaseService


class AdminsService:
    
    def __init__(self, model):
        self.model = model

    def authenticate(self, login, password):
        try:
            admin = self.model.objects.get(login=login)
            return admin.check_password(password)
        except self.model.DoesNotExist:
            return False

    def get_all(self):
        return list(self.model.objects.values('login'))