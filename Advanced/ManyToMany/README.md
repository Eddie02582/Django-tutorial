# Many to Many

這邊主要分兩部分一是在admin 顯示，和在網頁上顯示,假設有一個model,Project 如下


``` python 
class Project(models.Model):
    name = models.CharField(max_length=100,null=False,blank=True)
    owner = models.ManyToManyField(User,related_name='+',blank=True)



```
## admin 顯示
override formfield_for_manytomany,修改widget方式


``` python 
from django.contrib.admin.widgets import FilteredSelectMultiple
class ProjectAdmin(admin.ModelAdmin):   
    fields = ['name','owner']   
    def formfield_for_manytomany(self, db_field, request, **kwargs):
         vertical = False  # change to True if you prefer boxes to be stacked vertically
         kwargs['widget'] = FilteredSelectMultiple(
             db_field.verbose_name,
             vertical,
         )
         return super().formfield_for_manytomany(db_field, request, **kwargs)

```



## 網頁顯示


### 修改forms.py
加入class Meida 


``` python 
class ProjectForm(forms.ModelForm):   
    class Meta:       
        model = Project         
        fields=['project','owner']

    class Media:
        css = {'all':('css/widgets.css', 'css/overrides.css'),}
```

加入html 加入

```  html
{{ form.media }} 
<script src="/admin/jsi18n/"></script>
```

