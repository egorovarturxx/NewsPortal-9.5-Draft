from django.contrib.auth.models import User

class User(User):
    user =  User.objects.create_user('Artur', 'egorovarturxx@gmail.com', 'password')
    user.last_name = 'Egorov'
    user.save()