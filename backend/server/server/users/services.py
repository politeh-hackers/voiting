from base.service import BaseService


class AdminsService(BaseService):

    # def validation(self, data):
    #     self.validate_login("login", data)
    #     self.validate_password_strength("password",data)
    #     return super().create(data)

    def authenticate(self, login, password):
        return self.model.objects.filter(login=login, password=password).exists()