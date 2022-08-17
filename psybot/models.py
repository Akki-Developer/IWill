from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, email, password, username):
        if password is None:
            raise TypeError('Superusers must have a password.')

        # user = self.create_user(name, email, password)
        user = self.model(email=email,username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class userdetails(AbstractBaseUser, PermissionsMixin): 
    username = models.CharField(db_index=True, max_length=50, default = '')
    username = models.CharField(db_index=True, max_length=50, default = '')
    email = models.CharField(max_length=225, unique=True)
    
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    
    objects = UserManager()

    def __str__(self):
        return self.email

#------------------------------------------------------------------------------------------------------------------------------------------------------------

class UserModel(models.Model):
    userId = models.IntegerField(null=True)
    name= models.CharField(max_length=225, default = '')
    gender = models.CharField(max_length=225, default = '')
    age = models.IntegerField(null=True)
    country = models.CharField(max_length=225, default = '')
    state = models.CharField(max_length=225, default = '')
    city = models.CharField(max_length=225, default = '')
    language = models.CharField(max_length=225, default = '')
    severity = models.CharField(max_length=225, default = '')
    cat_id =  models.IntegerField(null=True)
    # category = models.IntegerField(null=True)
    # sub_category = models.IntegerField(null=True)
    # region = models.CharField(max_length=100, default = '')
    created_at = models.DateTimeField(auto_now=True)


class Exercise(models.Model):
    exercise_id = models.IntegerField(null=True)
    exercise_name = models.CharField(max_length=50, default = '')
    created_at = models.DateField(auto_now_add=True)
    
class Bot_sessions(models.Model):
    bot_session_id = models.CharField(max_length=500, default = '')
    user_id = models.IntegerField(null=True)
    category_id = models.IntegerField(null=True)
    is_repeat_session = models.IntegerField(null=True)
    device_type = models.CharField(max_length=15, default = '')
    http_referer = models.CharField(max_length=30, default = '')
    utm_source = models.CharField(max_length=12, default = '')
    utm_campaign = models.CharField(max_length=20, default = '')
    utm_content = models.CharField(max_length=15, default = '')
    utm_content = models.CharField(max_length=15, default = '')
    created_at = models.DateTimeField(auto_now=True)

class Bot_conversation(models.Model):
    bot_session_id = models.CharField(max_length=500, default = '')
    user_id = models.IntegerField(null=True)
    category_id = models.IntegerField(null=True)
    input_text = models.CharField(max_length=500, default = '')
    response_text = models.JSONField(blank = True) 
    next_response = models.JSONField(blank = True)
    created_at = models.DateField(auto_now_add=True)

class Bot_emotion(models.Model):
    bot_session_id = models.CharField(max_length=500, default = '')
    emotion = models.CharField(max_length=500, default = '')
  
class User_exercise_status(models.Model):
    # bot_exercise_status_id = models.IntegerField(null=True)
    exercise_id = models.CharField(max_length=50, default = '')
    bot_session_id = models.CharField(max_length=500, default = '')
    week_count = models.IntegerField(default =0)
    completion_status = models.IntegerField(default =False)
    completed_at = models.DateTimeField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
