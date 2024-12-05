from base.service import BaseValidationService, BaseService


class AdminsService(BaseValidationService, BaseService):

    def validation(self, data):
        self.validate_login("login", data)
        self.validate_password_strength("password",data)
        return super().create(data)

    def authenticate(self, login, password):
        return self.model.objects.filter(login=login, password=password).exists()