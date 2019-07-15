# View


簡單的視圖函數

```python 

from django.http import HttpResponse

def home_page(request):
    return HttpResponse("Hello World!")  
```

將url

```python 
from . import views
...

urlpatterns = [
    # path函数将url映射到视图
    path('HonePage/', views.home_page, name='home_page'),
]
```




