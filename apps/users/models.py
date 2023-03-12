from django.db import models
import datetime
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

# Create your models here.

class UserAccountManager(BaseUserManager):

    def create_user(self , email, username, full_name, password = None, type='', contact_number=''):
        
        if not email or len(email) <= 0 :
            raise ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        if not username :
            raise ValueError("Username is required")
        if not full_name :
            raise ValueError("Full name is required")
        if not contact_number :
            raise ValueError("Contact number is required")
		
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            full_name = full_name,
            type = type, #to include the type of user at creation
            contact_number = contact_number
        )
        user.set_password(password) #the password will be hashed in the database before saving
        user.save(using = self._db)
        return user
	
    def create_superuser(self, email, username, full_name, password):
        user = self.create_user(
        email = self.normalize_email(email) ,
        password = password,
        username = username,
        full_name = full_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
	
class UserAccount(AbstractBaseUser):

    class Types(models.TextChoices):
        LANDLORD = "LANDLORD" , "landlord"
        TENANT = "TENANT" , "tenant"
		
    
    type = models.CharField(max_length = 8 , choices = Types.choices, default="TENANT") 

    email = models.EmailField(max_length = 200 , unique = True)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    username = models.CharField(max_length=200, unique=True)
    contact_number = models.IntegerField(default=0, unique=True)
    address = models.CharField(max_length=200, null=False, blank=False)
    is_firsttimelogin = models.BooleanField(default=True)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    profile_image = models.FileField()
    created_at = models.DateTimeField(default=datetime.datetime.now())
    updated_at = models.DateTimeField(default=datetime.datetime.now())

    USERNAME_FIELD = "username"

    # defining the manager for the UserAccount model
    objects = UserAccountManager()
	
    def __str__(self):
        return str(self.email)

    def has_perm(self , perm, obj = None):
        return self.is_admin

    def has_module_perms(self , app_label):
        return True


 

