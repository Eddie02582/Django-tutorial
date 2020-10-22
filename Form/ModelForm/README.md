# ModelForm



假設有一個model,用來記錄任務的開始和結束時間<br>

**model.py**

 ```python 
class Task(models.Model):    
    name = models.CharField(max_length=100, null = False,default="")    
    owner = models.ForeignKey(User, related_name='+',null=True,on_delete=models.CASCADE,blank=True)
    start_date = models.DateTimeField()	
    end_date = models.DateTimeField()	
    note = models.CharField(max_length=50, null = True, blank=True)
 ```

**form.py**
 ```python 
class TaskForm(forms.ModelForm):   
    class Meta:
        model = Task     
        #fields='__all__'        
        fields=('name','owner','start_date','end_date','note')	
    
```

## Use ModelForm in FBV & CBV

### FBV
```python 
def task_create(request):    
    context = {}    
    if request.method == 'POST':        
        form = TaskForm(request.POST)
        if form.is_valid():  
            form.save()
    else:
        form = TaskForm()
    
    return render(request,"task_create.html",context)

``` 
也可以使用modelform_factory,而不用在form.py定義

```python 
    TaskForm = modelform_factory(Task, fields=('name','owner','start_date','end_date','note')	)   
``` 
也可修改widgets

```python 
    TaskForm = modelform_factory(Task, fields=('name','owner','start_date','end_date','note'),widgets={'note': forms.Textarea(attrs={'cols': 120,'rows':10})})
``` 

### CBV

```python 		
class task_create(CreateView):
    model = Task
    form_class = TaskForm	
    template_name = 'task_create.html'
```  

也可以不使用form_class

```python 		
class task_create(CreateView):
    model = Task
    form_class = TaskForm	
    template_name = 'task_create.html'
```  


## Modify widgets
希望能修改fileds輸出預設的欄位,有2種方式

### through meta override
 ```python 
class TaskForm(forms.ModelForm):    
    class Meta:
        model = Task
        fields = ('name','owner','start_date','end_date','note')	
        labels = {
            'name': _('task name'),
        }
        widgets = { 
            'owner': forms.ModelChoiceField(queryset = User.objects.all()),
            'start_date': forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d'))),
            'end_date': forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d'))),
            'note': forms.Textarea(attrs={'cols': 120,'rows':10}),
           
		}       
    
```    

### override fileds
 ```python 
class TaskForm(forms.ModelForm):   
    start_date= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d')))	
    end_date= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d')))

    class Meta:
        model = Task     
        #fields='__all__'        
        fields = ('name','owner','start_date','end_date','note')	
    
```


    
### through init
用在特別情況,需要額外傳入資料的時候

 ```python 
class TaskForm(forms.ModelForm):   

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)     
        super(TaskForm, self).__init__(*args, **kwargs)      
        self.fields['owner'] = forms.ModelChoiceField(queryset = User.objects.filter( first_name = user.first_name))
        
    class Meta:
        model = Task
        fields = ('name','owner','start_date','end_date','note')	
        labels = {
            'name': _('task name'),
        }
        widgets = { 
            'note': forms.Textarea(attrs={'cols': 120,'rows':10}),
            'start_date': forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d'))),
            'end_date': forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d'))),
           
		}      
    
```        

修改attrs
```python 
class TaskForm(forms.ModelForm):   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
```        



## Pass argument to form 
透過kwargs.pop,將參數取出

 ```python 
class TaskForm(forms.ModelForm):   

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)     
        super(TaskForm, self).__init__(*args, **kwargs)      
        self.fields['owner'] = forms.ModelChoiceField(queryset = User.objects.filter( first_name = user.first_name))
        

```       
    
    
### FBV 

```python 

def task_create(request):    
    context = {}
    
    if request.method == 'POST':        
        form = TaskForm(request.POST,user = user)
        if form.is_valid():  
            form.save()
    else:
        form = TaskForm(user = user)
    
    return render(request,"task_create.html",context)

```   

### CBV 

```python 

		
class task_create(CreateView):
    model = Task
    form_class = TaskForm	
    template_name = 'task_create.html'
    success_url = reverse_lazy('task_View')


    def get_form_kwargs(self):
        kwargs = super(task_create, self).get_form_kwargs()
        kwargs['user'] = self.request.user # pass the 'user' in kwargs
        return kwargs         

```   

## Validation form User define 
There are two main steps involved in validating a ModelForm:
<ul>
    <li>Validating the form</li>
    <li>Validating the model instance</li>
</ul>
這邊介紹Validating the form

## Overriding the clean() method

 ```python 
 
class TaskForm(forms.Form):   
    def clean(self):          
        cleaned_data  = super(TaskForm, self).clean()  
        start_date = cleaned_data.get('start_date') 
        end_date = cleaned_data.get('end_date') 
        
        if not end_date >= start_date:     
            raise forms.ValidationError("End date must be greater than start date")
        return cleaned_data     
    
    class Meta:
        model = Task
        fields = ('name','owner','start_date','end_date','note')	       
        widgets = { 
            'note': forms.Textarea(attrs={'cols': 120,'rows':10}),
            'start_date': forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d'))),
            'end_date': forms.DateInput(attrs={'type': 'date'},format=('%Y-%m-%d'))),
           
		}  
```
## clean_fields()

 ```python  
    def clean_start_date(self):   
        # data from the form is fetched using super function 
        cleaned_data  = super(ResourceForm, self).clean() 
        
        start_date = cleaned_data.get('start_date') 
        end_date = cleaned_data.get('end_date') 
        if not end_date >= start_date:    
            raise forms.ValidationError("End date must be greater than start date")
        return cleaned_data 
```

 ```python  
    def clean_start_date(self):           
        start_date = self.cleaned_data.get('start_date') 
        end_date = self.cleaned_data.get('end_date') 
  
        if not end_date >= start_date:    
            raise forms.ValidationError("End date must be greater than start date")
            
        return start_date 
```



## Pass initial value to form 
設定出始値也可以透過form.py設定default,但是需要依招不同情況的初始値,就可以使用




### FBV 

```python 

def task_create(request):    
    context = {}
    initial = {'note': 'NA'}
    if request.method == 'POST':        
        form = TaskForm(request.POST)
        if form.is_valid():  
            form.save()
    else:
        form = TaskForm(user = user,initial = initial)
    
    return render(request,"task_create.html",context)

```   

### CBV 

```python 		
class task_create(CreateView):
    model = Task
    form_class = TaskForm	
    template_name = 'task_create.html'
    success_url = reverse_lazy('task_View')
    initial = {'note': 'NA'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial = self.initial)
        return render(request, self.template_name, {'form': form})
        
    def get_form_kwargs(self):
        kwargs = super(task_create, self).get_form_kwargs()
        kwargs['user'] = self.request.user # pass the 'user' in kwargs
        return kwargs   
```  










    
    
    
    
    
    
    