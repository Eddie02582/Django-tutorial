# Admin User Modify

這邊教如何修改User Model Admin
這邊使用<a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Extend%20Django%20USER%20Model#using-one-to-one-link-with-a-user-modelprofile">Using One-To-One Link With a User Model(Profile) </a>



model.py如下


```python 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Team_CHOICES = (        
		('HW', 'HW'), 
		('Layout', 'Layout'), 	
        ('Driver', 'Driver'),    			
	)    
    
    
    Team = models.CharField(max_length=30,default='Others',choices=Team_CHOICES)
    Ext = models.CharField(max_length=30,null=True,blank=True,default="")	
    Short_number= models.CharField(max_length=30,null=True,blank=True,default="")	
    Cellphone_number= models.CharField(max_length=30,null=True,blank=True,default="")
    WeChat_ID= models.CharField(max_length=30,null=True,blank=True,default="")	
    Supervisor =  models.ForeignKey(User, on_delete=models.SET_NULL,related_name="+",null=True,blank=True)   
    incumbent = models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name +" " +self.user.last_name 

    def get_user_id(self):
        return self.user.username
	
    get_user_id.short_description   = 'ID'
```

## Incline
admin.py
注意這邊為OneToOneField,處理方式與ForeignKey不同


```python 
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
```

    
## 修改UserAdmin 
透過繼承方式修改,並unregister,再register新的
 
```python
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username','Team','__str__','email','Ext','Supervisor','last_login')
    ordering = ('username',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def Team(self,obj):
        return obj.profile.Team

    def Supervisor(self,obj):
        return obj.profile.Supervisor
 
    def Ext(self,obj):
        return obj.profile.Ext        
```

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

