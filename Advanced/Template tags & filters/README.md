#  Template tags & filters

<a href = "https://zwindr.blogspot.com/2016/05/django-template-tags-filters.html">詳細可以參考 </a>


這邊主要分兩部分一是在admin 顯示，和在網頁上顯示,假設有一個model,Project 如下


## 設定
<u1>
    <li>
        建立templatetags資料夾</a>
    </li>  
    <li>
        在欲使用html 裡面加入 {% load eamsfilter %}
    </li>    
    <li>
        在eamsfilter.py
        ``` python 
            from django import template            
            register = template.Library()
        ```        
    </li>       
</ul>

Note :eamsfilter 可自己取名,但是注意 {% load name %} ,name.py 名字要一樣

## 定義 template filters

eamsfilter.py

``` python 
from django import template
register = template.Library()
@register.filter(name='lower')
def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()
``` 

html 
``` 
{% load eamsfilter %} 

{{ somevariable|lower}}
``` 

如果資料為model </br>

model.py
``` python 

class Tasks(models.Model):
    name=models.CharField(max_length=50, null=False,default="")  
    
    def lower():
       return value.lower()
``` 

html 
``` 
   {{task.lower}}
``` 
