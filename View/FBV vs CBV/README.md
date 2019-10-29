# FBV Vs CBV




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
        <td>CreateView</td>
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
</br>
介紹一些常用的Attributes</br>

<table>
    <tr>
        <th>名稱</th>
        <th>目的</th>
        <th>Note</th>        
    </tr>
     <tr>
        <td>context_object_name</td>
        <td>傳給template 資料名稱</td>
        <td></td>
    </tr> 
    <tr>
        <td>model</td>
        <td>設定model</td>
        <td></td>
    </tr>
    <tr>
        <td>form_class</td>
        <td>設定Form</td>
        <td>不設定會照Model建form</td>
    </tr>    
    <tr>
        <td>pk_url_kwarg </td>
        <td>url 傳入的參數</td>
        <td>使用在create,update,detail</td>
    </tr>       
    <tr>
        <td>queryset</td>
        <td> </td>
        <td> </td>
    </tr>
    <tr>
        <td>success_url</td>
        <td>成功時導入的網址</td>
        <td>通常用在create,update</td>
    </tr> 
    <tr>
        <td>template_name</td>
        <td>使用的模板</td>
        <td></td>
    </tr>
    <tr>
        <td>paginate_by</td>
        <td>多少筆資料作為分頁</td>
        <td>list 專用</td>
    </tr>  
    <tr>
        <td>ordering</td>
        <td>排序</td>
        <td>list 專用</td>
    </tr>   
</table>


介紹一些常用的Method,不一定每個View 都有</br>
利用下面方式執行為override method
```
super().method_name(request, *args, **kwargs)
```
<table>
    <tr>
        <th>名稱</th>
        <th>目的</th>
        <th>Note</th>        
    </tr>
     <tr>
        <th>get_context_data</th>
        <td>取得context值</td>
        <td>若想增加回傳內容,可自行修改</td>
    </tr> 
    <tr>
        <td>get_queryset</td>
        <td>取得queryset</td>
        <td></td>
    </tr>
    <tr>
        <td>get</td>
        <td>get 動作</td>
        <td></td>
    </tr>    
    <tr>
        <td>post </td>
        <td>post 動作</td>
        <td></td>
    </tr>       
    <tr>
        <td>form_valid</td>
        <td>表單驗證</td>
        <td> </td>
    </tr>
    <tr>
        <td>get_success_url</td>
        <td>取得成功導入的網址</td>
        <td>通常用在create,update</td>
    </tr>    
</table>


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

### CreatView

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
        return reverse('hwtask_detail', args=(self.object.id,))
        
```

或者改寫form_valid

**view.py**
```python
class HWTask_Create(CreateView):
    model = HW
    form_class=HWForm	
    template_name = 'HW/Creat.html'  
    
    def form_valid(self, form): 
        tasks = form.save(commit=True)   
        return redirect('hwtask_detail', hwtask_id=tasks.pk) 
```

### UpdateView
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
class HWTask_Edit(UpdateView):
    model = HW
    form_class=HWForm  
    template_name = 'HW/Edit.html'
    pk_url_kwarg = 'hwtask_id'
    context_object_name = 'tasks' 
 
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
```

你希望導回自己建立的網頁而非raise Http404(),先利用get_object()取得物件,在判斷是否是為同一使用者,不是返回access_error網頁
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
            return redirect('/accounts/access_error/')
```



介紹一個View共用的方法，避免重複寫code，定義ActionEditGetMixin，覆寫get method

   
```python
class ActionEditGetMixin(object):
    def get(self, request, *args, **kwargs): 
        obj=self.get_object()
        username=[ owner.username for owner in obj.owner.all()]
        if self.request.user.username  in username:
            return super().get(request, *args, **kwargs)
        else:
            #raise PermissionDenied
            return redirect('/accounts/access_error/')

```
HWTask_Edit 同時繼承ActionEditGetMixin和UpdateView

```python  
class HWTask_Edit(ActionEditGetMixin,UpdateView):
    model = HW
    form_class=HWForm  
    template_name = 'HW/Edit.html'
    pk_url_kwarg = 'hwtask_id'
    context_object_name = 'tasks' 
```


希望表單驗證時，有些資料需要在後台編輯修改(Form 可能沒完全包含整個Model fields)，可以透過override form_valid()
注意本資料包含Many to Many 資料所以使用form.save_m2m() 和 tasks.save()

```python
class HWTask_Edit(UpdateView):
    model = HW
    form_class=HWForm  
    template_name = 'HW/Edit.html'
    pk_url_kwarg = 'hwtask_id'
    context_object_name = 'tasks' 

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












