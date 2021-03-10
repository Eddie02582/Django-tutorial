# Form



## Create Simple Form

主要分三部分
<ul>
    <li>form:寫入表單對應的欄位</li>
    <li>views:處理提交form表單</li>
    <li>template:顯示網頁上的表格</li>
</ul>

### Form.py
建立表單需要的欄位

```python 
from django import forms			 
class APLossForm(forms.Form):
    FreqInMHz  = forms.FloatField(label='Freq (MHz)', required=True)
    levelInDb  = forms.FloatField(label='Rssi Level In dB', required=True)
```


### View.py 
<ul>
    <li>form = APLossForm()實體化,並將form 傳入template</li>
    <li>form = APLossForm(request.POST)取得form POST 的資料</li>   
    <li>form.is_valid() 用來驗證表單資料是否正確</li>
    <li>form.cleaned_data[field] 取得資料(field 對應form.py欄位)</li>
</ul>

```python 
def ApLoss_View(request):	     
    if request.method == 'POST':
        form = APLossForm(request.POST)	
        if form.is_valid():             
            Freq = form.cleaned_data.get('FreqInMHz') 
            levelInDb = request.POST.get('levelInDb',)         
            result = (27.55 - (20 * math.log10(Freq)) + math.fabs(levelInDb)) / 20.0
            meters = math.pow(10, result)       
            feet = meters * 3.2808            	    
            return render(request, 'APLoss.html', {'form': form,'feet':feet,'meters':meters})		        
    else:  
        form = APLossForm() 
        return render(request, 'APLoss.html', {'form': form})

```

### template

有以下方法可以顯示table 格式
<ul>
    <li>{{ form.as_table }} will render them as table cells wrapped in <tr> tags</li>
    <li>{{ form.as_p }} will render them wrapped in <p> tags</li>
    <li>{{ form.as_ul }} will render them wrapped in <li> tags</li>
</ul>

```html
    <form method="post">
        {% csrf_token %}
        {{form.as_table}}
        <input type="submit" value="Submit">
    </form>	
```

如果需要自訂格式也可以
```html
	<form enctype="form-data" action="" method="post">
		{% csrf_token %}
		<div class="form-group ">{{form.FreqInMHz.label}} : {{form.FreqInMHz}}</div>		
		<div class="form-group ">{{form.levelInDb.label}} : {{form.levelInDb}}</div>  	
		<input type="submit" value="Submit">		
	</form>	
```


## Create Form with File
    
### Form.py

```python 
from django import forms			 
class FileForm(forms.Form):
   upload = forms.FileField(label='Upload File', required = True)    
```

### View.py 

透過request.FILES['upload']取得

```python 
def upload_file(request):	     
    if request.method == 'POST':
        form = FileForm(request.POST)	
        if form.is_valid():             
            file_path = handle_uploaded_file(request.FILES['upload'],path)      	    
            return render(request, 'APLoss.html',{'form':form})		        
    else:  
        form = APLossForm() 
    return render(request, 'APLoss.html', {'form': form})

def handle_uploaded_file(f,path):    
    path += f.name 
    with open(path,"wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)   
    return path
```

### Template
```html
<form method="post" enctype="multipart/form-data">
	{% csrf_token %}		
    {{form.form.as_p}}
	<input type="submit" value="Submit">
</form>	
```

    
    
    
    
    
    