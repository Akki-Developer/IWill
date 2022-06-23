from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations = True

    # def create_user(self, name, email, password=None):
    #     if not email:
    #         raise ValueError('Users Must Have an email address')
    #     user = self.model(name=name, email=email)
    #     user.set_password(password)
    #     user.save()
    #     return user

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
    # pass
    username = models.CharField(db_index=True, max_length=50, default = '')
    username = models.CharField(db_index=True, max_length=50, default = '')
    email = models.CharField(max_length=225, unique=True)
    # is_email_verified= models.CharField(max_length=225, default = '')
    # userId= models.CharField(max_length=225, default = '')
    # mobile_number = models.CharField(max_length=30, default = '')
    # country_code = models.CharField(max_length=30, default = '')
    # twilio_s_id = models.CharField(max_length=200, default = '')
    # is_mobile_verified = models.BooleanField(default=False)
    # customerId= models.CharField(max_length=225, default = '')
    # firstname= models.CharField(max_length=225, default = '')
    # lastname= models.CharField(max_length=225, default = '')
    # account_type= models.CharField(max_length=225, default = '')
    # daily_limit= models.CharField(max_length=225, default = '')
    # city= models.CharField(max_length=225, blank=True, default=None, null=True)
    # country= models.CharField(max_length=225, blank=True, default=None, null=True)
    # timezone= models.CharField(max_length=225, default = '')
    # status= models.CharField(max_length=225, default = '')
    # s3_path= models.CharField(max_length=225, blank=True, default=None, null=True)
    # api_access_token= models.CharField(max_length=1000, default = '')
    # jwt_token= models.CharField(max_length=1000, default = '')
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    
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

    # def save(self, *args, **kwargs):
    #     self.userId = self.userId
    #     super(UserModel, self).save(*args, **kwargs)


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
    input_text = models.TextField(default = '')
    response_text = models.JSONField(blank = True) 
    created_at = models.DateField(auto_now_add=True)
    next_response = models.JSONField(blank = True)

  
# class Country_region(models.Model):
#     country_id = models.IntegerField(null=True)
#     user_id = models.IntegerField(null=True)
#     country_name = models.CharField(max_length=100, default = '')
#     state_id = models.IntegerField(null=True)
#     state_name = models.IntegerField(null=True)
#     city_id = models.IntegerField(null=True)
#     city_name = models.CharField(max_length=100, default = '')
#     region_id = models.IntegerField(null=True)
#     region_name = models.CharField(max_length=100, default = '')

# class Bot_exerciseviews(models.Model):
#     # bot_exerciseviews_id = models.IntegerField(null=True)
#     exercise_id = models.CharField(max_length=50, default = '')
#     bot_session_id = models.IntegerField(null=True)
#     created_at = models.IntegerField(null=True)

class User_exercise_status(models.Model):
    # bot_exercise_status_id = models.IntegerField(null=True)
    exercise_id = models.CharField(max_length=50, default = '')
    bot_session_id = models.CharField(max_length=500, default = '')
    completion_status = models.IntegerField(default =False)
    completed_at = models.DateTimeField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

# class Recommended_exercise(models.Model):
#     recommended_exercise_id = models.IntegerField(null=True)
#     exercise_id = models.IntegerField(null=True)
#     bot_session_id = models.IntegerField(null=True)
#     category_id = models.IntegerField(null=True)
#     created_at = models.IntegerField(null=True)
#     severity_id = models.IntegerField(null=True)
#     sub_category_id = models.IntegerField(null=True)
#     age_id = models.IntegerField(null=True)
#     gender_id = models.IntegerField(null=True)
#     country_id = models.IntegerField(null=True)
#     state_id = models.IntegerField(null=True)
#     language_id = models.IntegerField(null=True)

# class User_exercise_inputs(models.Model):
#     user_exercise_inputs_id = models.IntegerField(null=True)
#     bot_exerciseviews_id = models.IntegerField(null=True)
#     input_1 = models.CharField(max_length= '', default = '')

# class Category(models.Model):
#     category_id = models.IntegerField(null=True)
#     user_id = models.IntegerField(null=True)
#     category_name = models.CharField(max_length=100, default = '')
#     created_at = models.IntegerField(null=True)

# class Sub_category(models.Model):
#     sub_category_id = models.IntegerField(null=True)
#     user_id = models.IntegerField(null=True)
#     sub_category_name = models.CharField(max_length=100, default = '')
#     created_at = models.IntegerField(null=True)
#     category_id = models.IntegerField(null=True)

# class Language(models.Model):
#     language_id = models.IntegerField(null=True)
#     user_id = models.IntegerField(null=True)    

# class Issue_severity(models.Model):
#     severity_id = models.IntegerField(null=True)   
#     user_id  = models.IntegerField(null=True)   

# class Age_gender_id(models.Model):    
#     age_id = models.IntegerField(null=True)  
#     user_id = models.IntegerField(null=True)  
#     age_range = models.IntegerField(null=True)  
#     gender_id = models.IntegerField(null=True)  
#     gender_name = models.CharField(max_length=30, default = '')

       