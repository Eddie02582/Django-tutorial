# Extend Django USER Model


原文出處
<href>https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html<href>

Django的內置身份驗證系統非常棒。 在大多數情況下，我們可以開箱即用，節省了大量的開發和測試工作。它適合大多數用例，非常安全。但有時我們需要做一些微調，以適應我們的Web應用程序。
通常我們希望存儲與我們的用戶相關的更多數據。如果您的Web應用程序具有社交吸引力，您可能希望存儲簡短的生物，用戶的位置以及其他類似的東西。在本教程中，我將介紹可用於簡單擴展默認Django用戶模型的策略，因此您無需從頭開始實現所有內容。<br>



Django中有幾種方式。
>
> > 1.Proxy Model：對Django用戶提供的所有內容感到滿意，並且不需要存儲額外的信息。
>
> > 2.User Profile：對Django處理身份驗證的方式感到滿意，並且需要向用戶添加一些非身份驗證相關的屬性。
>
> > 3.Custom User Model from AbstractBaseUser:Django處理身份驗證的方式不適合您的需求。
>
> > 4.Custom User Model from AbstractUser:Django處理auth的方式非常適合您的需求，但仍然希望添加額外的屬性而無需創建單獨的模型。
    
## Using a Proxy Model
**什麼是代理模型？**<br>
它是一種模型繼承，無需在數據庫中創建新表。 它用於更改現有模型的行為（例如，默認排序，添加新方法等），而不會影響現有數據庫模式。<br>

**我什麼時候應該使用代理模型？**<br>
當您不需要在數據庫中存儲額外信息時，您應該使用代理模型來擴展現有的用戶模型，而只需添加額外的方法或更改模型的查詢管理器。<br><br>

這是擴展現有用戶模型的侵入性較小的方法。 這種策略不會有任何缺點。 但它在很多方面都非常有限。<br>


```python
from django.contrib.auth.models import User
from .managers import PersonManager
class Person(User):
    objects = PersonManager()
    class Meta:
        proxy = True
        ordering = ('first_name', )
    def do_something(self):
        ...
```
這是在上面的示例中，我們定義了一個名為Person的代理模型。 我們通過在Meta類中添加以下屬性來告訴Django這是一個代理模型：proxy = True。<br>
在這種情況下，重新定義了默認排序，為模型分配了自定義管理器，還定義了一個新方法do_something。<br>
值得注意的是，User.objects.all（）和Person.objects.all（）將查詢相同的數據庫表。 唯一的區別在於我們為代理模型定義的行為。<br>


## Using One-To-One Link With a User Model(Profile)

**What is a One-To-One Link?**<br>
它是一個常規的Django模型，它將擁有自己的數據庫表，並通過OneToOneField與現有的用戶模型保持一對一的關係。<br>

**When should I use a One-To-One Link?**<br>
當您需要存儲與身份驗證過程無關的現有用戶模型的額外信息時，應使用一對一鏈接。 我們通常將其稱為用戶檔案。<br>

這很有可能是你想要的。 就個人而言，這是我大部分時間使用的方法。 我們將創建一個新的Django模型來存儲與用戶模型相關的額外信息<br>

建立Profile模型<br>

```python
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)  
```

定義信號，以便在創建/更新用戶實例時自動創建/更新我們的Profile模型。
```python
class Profile(models.Model):
.......
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save() 
```
**form.py**

```python
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('url', 'location', 'company')
```

**view.py**

```python
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form    })
```

## Using a Custom Model Extending AbstractBaseUser
需要使用電子郵件地址作為身份驗證令牌，在這種情況下，用戶名對我來說完全沒用。<br>
此外，不需要is_staff標誌，因為我沒有使用Django Admin。<br>
注意我們應該在項目的開始階段設計好完，因為它操作將極大地影響數據庫模式。執行時要格外小心。<br>

自己定義user model 
**model.py**

```python 
from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    def get_full_name(self):       
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    def get_short_name(self):       
        return self.first_name
    def email_user(self, subject, message, from_email=None, **kwargs):
        ''' Sends an email to this User.'''
        send_mail(subject, message, from_email, [self.email], **kwargs) 
```

希望盡可能接近現有的用戶模型。由於我們繼承自AbstractBaseUser，我們必須遵循一些規則：<br>

USERNAME_FIELD：描述用戶模型上用作唯一標識符的字段名稱的字符串。該字段必須是唯一的（即，在其定義中設置unique = True）<br>
REQUIRED_FIELDS：通過createsuperuser管理命令創建用戶時將提示的字段名稱列表<br>
is_active**：一個布爾屬性，指示用戶是否被視為“活動”<br>
get_full_name（）：用戶的較長的正式標識符。常見的解釋是用戶的全名，但它可以是標識用戶的任何字符串。<br>
get_short_name（）：用戶的簡短非正式標識符。常見的解釋是用戶的名字。<br>

還要定義自己的UserManager。那是因為現有的管理器定義了create_user和create_superuser方法。<br>


```python 
from django.contrib.auth.base_user import BaseUserManager
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.') 
```

現在是最後的舉動。 我們必須更新settings.py 修改AUTH_USER_MODEL屬性，<br>
> AUTH_USER_MODEL = 'core.User'
這樣我們就告訴Django使用我們的自定義模型而不是默認模型。 在上面的示例中，我在名為core的應用程序中創建了自定義模型。<br>


**How should I reference this model?**<br>

有兩種方法。 考慮一個名為Course的模型：<br>


```python 
from django.db import models
from testapp.core.models import User
class Course(models.Model):
    slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=100)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
```

This is perfectly okay. But if you are creating a reusable app, that you want to make available for the public,<br> 
it is strongly advised that you use the following strategy:<br>


```python 
from django.db import models
from django.conf import settings

class Course(models.Model):
    slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=100)
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

<br> 
**Using a Custom Model Extending AbstractUser


```python 
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
```

我們必須更新settings.py 修改AUTH_USER_MODEL屬性，<br> 
> AUTH_USER_MODEL = 'core.User'

與前一種方法類似的方式，這應該在項目的開始時進行，並且要特別小心。 它將更改整個數據庫架構。 <br> 
此外，更喜歡為用戶模型創建外鍵，從django.conf導入設置導入設置並引用settings.AUTH_USER_MODEL而不是直接引用自定義用戶模型。<br> 