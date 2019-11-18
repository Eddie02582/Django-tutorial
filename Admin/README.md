# Admin


```python 

from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']
    admin.site.register(Question, QuestionAdmin)

```

透過 admin.site.register 修改admin 方式


<img src="admin_1.png" alt="Smiley face">