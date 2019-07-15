# View


## Simple View 

```python 

from django.http import HttpResponse

def home_page(request):
    return HttpResponse("Hello World!")  
```

將HomePage導入views.home_page

```python 
from . import views
...

urlpatterns = [
    # path函数将url映射到视图
    path('HonePage/', views.home_page, name='home_page'),
]
```
## Example 


假設我們想建立一個計算BMI 的網頁</br>

form.py </br>

```python 

from django import forms
			 
class BMIForm(forms.Form):
    Height  = forms.FloatField(label='Height (m)', required=True)
    Weight = forms.FloatField(label='Weight (kg)', required=True)

```

url.py

```
urlpatterns = [
    .....
            path('BMI/', views.BMI, name='BMI'),	
]
```

```python 
from .forms import BMIForm
def BMI(request):	
    form = BMIForm()  
    if request.method == 'POST':
        form = BMIForm(request.POST)	
        if form.is_valid():             
            Height = form.cleaned_data.get('Height')         
            Weight = form.cleaned_data['Weight']
            bmi = Weight/ (Height*Height)       	    
            return render(request, 'BMI.html', {'form': form,'bmi':bmi})		        
    else:        
        return render(request, 'BMI.html', {'form': form})		
```

BMI.html
```

<form enctype="multipart/form-data" action="" method="post">
    {% csrf_token %}
    {{form.as_p}}	
    <input type="submit" value="Run">	
	{% if  bmi %}
        BMI is : {{bmi}}
	{% endif %} 	
</form>
```


<img src="view_example.png">

## Use  FormView


注意url.py 要使用.as_view()

```
urlpatterns = [
    .....
            path('BMI/', views.BMI.as_view(), name='BMI'),	
]
```

form.py
詳細可以參考<a href ="https://github.com/Eddie02582/Django-tutorial/tree/master/View/FBV%20vs%20CBV">FBV vs CBV</a>

```python
class BMI(View):

    form_class= BMIForm  
    template_name = 'BMI.html'
    
    def form_valid(self, form):                   
        Height = form.cleaned_data.get('Height')         
        Weight = form.cleaned_data['Weight']
        bmi = Weight/ (Height*Height)       	    
        return render(request, 'BMI.html', {'form': form,'bmi':bmi})	

```





