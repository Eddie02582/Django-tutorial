# FBV Vs CBV


原文出處

Django視圖本質是一個函數：接受HttpRequest對像作為參數，返回一個HttpResponse對像作為返回.FBV直接就是這樣一個函數，而CBV類的方法as_view（），它的返回也是這樣一個函數。<br>
Django提供了一些通用視圖，基於通用類的視圖（GCBV），可以加快開發。實現所有內容。<br>

注意 FBV 與CBV path 中寫法不一樣

    
## FBV (Function Base View)

以下是簡單的FBV
**view.py**

```python
def ApLoss_View(request):   
    form = APLossForm()  
    if request.method == 'POST':
        form = APLossForm(request.POST) 
        if form.is_valid():             
            Freq = form.cleaned_data.get('FreqInMHz')         
            levelInDb = form.cleaned_data['levelInDb']
            result = (27.55 - (20 * math.log10(Freq)) + math.fabs(levelInDb)) / 20.0
            meters = math.pow(10, result)       
            feet = meters * 3.2808                  
            return render(request, 'APLoss.html', {'form': form,'feet':feet,'meters':meters})
```

**url.py**
```python
    path('APLoss/', views.ApLoss_View.as_view(), name='AP_Loss'),	
```


## GCBV (Generic Class-Based View)

<table>
    <tr>
        <th>名稱</th>
        <th>目的</th>        
    </tr>
    <tr>
        <td>ListView</td>
        <td>列出對象</td>
    </tr>
    <tr>
        <td>DetailView</td>
        <td>對象的詳細信息</td>
    </tr>    
    <tr>
        <td>FormView</td>
        <td>提交表單</td>
    </tr>
    <tr>
        <td>創建對象</td>
        <td>提交表單</td>
    </tr>
    <tr>
        <td>UpdateView</td>
        <td>更新對象</td>
    </tr>
    <tr>
        <td>DeleteView</td>
        <td>刪除對象</td>
    </tr>
</table>
詳細各個View 的方法 可以參考<href>https://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/CreateView/</href>



### FormView
可以比較一下和FBV 的差異<br>

**view.py**
```python
class ApLoss_View(FormView):
    form_class=APLossForm  
    template_name = 'APLoss.html'	
    def form_valid(self, form):        
        Freq = form.cleaned_data.get('FreqInMHz')         
        levelInDb = form.cleaned_data['levelInDb']
        result = (27.55 - (20 * math.log10(Freq)) + math.fabs(levelInDb)) / 20.0
        meters = math.pow(10, result)       
        feet = meters * 3.2808            	    
        return render(self.request, 'APLoss.html', {'form': form,'feet':feet,'meters':meters})
```


### ListView
ListView 搭配資料庫使用<br>
model :模型<br>
context_object_name :傳給template 資料名稱<br>
template_name: 使用的模板<br>
paginate_by :分頁<br>

**view.py**
```python
class HWTask_View(ListView):
    model = HW
    context_object_name = 'tasks'
    template_name =  'Task/HW/ListView.html'
    paginate_by = 10

    def get_queryset(self):
        queryset= HW.objects.all().order_by('-modify_date') 
        return queryset
```

若希望listView 也能有post可自行添<br>
> def post(self, request, *args, **kwargs):


### CreatView
注意希望使用自訂Form,可使用form_class=HWForm  <br>

**view.py**
```python
class HWTask_Creat(CreateView):
    model = HW
    #form_class=HWForm   
    template_name = 'Task/HW/Creat.html'
    success_url = reverse_lazy('hwtask_View')   
```

希望成功後進入url傳入參數,因此改寫def get_success_url<br>

**view.py**
```python
class HWTask_Creat(CreateView):
    model = HW
    form_class=HWForm   
    template_name = 'Task/HW/Creat.html'
    
    def get_success_url(self):
        #兩種方法都可 redirect or reverse
        #return redirect('pltask_detail', pltask_id=self.object.id)         
        return reverse('HW/Creat.html',args=(self.object.id,))  

        
```


### UpdateView
pk_url_kwarg 為傳入參數,與url.py 需一樣,因此tasks=HW.objects.get(id=pk_url_kwarg) <br>

**url.py**
```python
	path('HWTask/<int:hwtask_id>/edit/', views.HWTask_Edit.as_view(), name='hwtask_edit'),      
```

**view.py**
```python
class HWTask_Edit(UpdateView):
    model = HW
    form_class=HWForm  
    template_name = 'Task/HW/Edit.html'
    pk_url_kwarg = 'hwtask_id'
    context_object_name = 'tasks'  
```

比如你希望一個用戶只能查看或編輯自己發表的文章對象。當用戶查看別人的對象時，返回http 404錯誤。<br>
這時候你可以通過更具體的get_object（）方法來返回一個更具體的對象。如下：<br>

**view.py**
```python
class HWTask_Detail(DetailView): 
    model = HW
    template_name = 'HW/Detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'hwtask_id'
 
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
```

你希望一個用戶只能查看或編輯自己發表的文章對象，當用戶查看別人的對象時，返回其他網址<br>
可利用get()，super().get(request, *args, **kwargs) 執行原本為override 的代碼

**view.py**
```python
class HWTask_Edit(UpdateView):
    model = HW
    form_class=HWForm  
    template_name = 'HW/Edit.html'
    pk_url_kwarg = 'hwtask_id'
    context_object_name = 'tasks' 

    def get(self, request, *args, **kwargs): 
        obj=self.get_object()
        username=[ owner.username for owner in obj.owner.all()]
        if self.request.user.username  in username:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('/accounts/access_error/'
```

希望表單驗證時，有些資料需要在後台編輯修改(Form 可能沒完全包含整個Model fields)，可以透過form_valid()
注意本資料包含Many to Many 資料所以使用
form.save_m2m()  
tasks.save()

```python
class HWTask_Edit(UpdateView):
    model = HW
    form_class=HWForm  
    template_name = 'HW/Edit.html'
    pk_url_kwarg = 'hwtask_id'
    context_object_name = 'tasks' 


    def get(self, request, *args, **kwargs): 
        obj=self.get_object()
        username=[ owner.username for owner in obj.owner.all()]
        if self.request.user.username  in username:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('/accounts/access_error/')

    def form_valid(self, form):         
        tasks = form.save(commit=False) 
        if tasks.status=="Close":
            tasks.end_date=datetime.datetime.now()
        form.save_m2m()  
        tasks.save()     
        return redirect('hwtask_detail', hwtask_id=tasks.pk) 
```




### DetailView


```python
class HWTask_Detail(DetailView): 
    model = HW
    template_name = 'HW/Detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'hwtask_id'
```












