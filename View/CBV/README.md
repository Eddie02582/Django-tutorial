# CBV (Generic Class-Based View)

CBV類的方法as_view()，它的返回也是這樣一個函數。<br>
Django提供了一些通用視圖，基於通用類的視圖（GCBV），可以加快開發。實現所有內容。<br>

注意 FBV 與CBV path 中寫法不一樣



<table>
    <tr>
        <th>名稱</th>
        <th>目的</th>   
        <th>Link</th>        
    </tr>
    <tr>
        <td>ListView</td>
        <td>列出對象</td>       
        <td> <a href = "https://ccbv.co.uk/projects/Django/2.1/django.views.generic.list/ListView/">Link</a></td>
    </tr>
    <tr>
        <td>DetailView</td>
        <td>對象的詳細信息</td>
        <td> <a href = "https://ccbv.co.uk/projects/Django/2.1/django.views.generic.detail/DetailView/">Link</a></td>
    </tr>    
    <tr>
        <td>FormView</td>
        <td>提交表單</td>
        <td> <a href = "https://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/FormView/">Link</a></td>
    </tr>
    <tr>
        <td>CreateView</td>
        <td>提交表單</td>
        <td> <a href = "https://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/CreateView/">Link</a></td>
    </tr>
    <tr>
        <td>UpdateView</td>
        <td>更新對象</td>
        <td> <a href = "https://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/UpdateView/">Link</a></td>
    </tr>
    <tr>
        <td>DeleteView</td>
        <td>刪除對象</td>
        <td> <a href = "https://ccbv.co.uk/projects/Django/2.1/django.views.generic.edit/DeleteView/">Link</a></td>
    </tr>
</table>


介紹一些共用的Attributes,其它的分別在介紹</br>
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
        <td>success_url</td>
        <td>成功時導入的網址</td>
        <td>通常用在create,update</td>
    </tr> 
    <tr>
        <td>template_name</td>
        <td>使用的模板</td>
        <td></td>
    </tr>  
</table>

## CreatView/UpdateView
Attributes
<table>
    <tr>
        <th>名稱</th>
        <th>目的</th>
        <th>Note</th>        
    </tr>
     <tr>
        <td>fields</td>
        <td>選擇form的輸出欄位,通常會透過form.py設定</td>
        <td></td>
    </tr> 
    <tr>
        <td>form_class</td>
        <td>設定Form</td>
        <td>沒設定會照Model建form,此時就可以搭配fields</td>
    </tr>
    <tr>
        <td>pk_url_kwarg </td>
        <td>url 傳入的參數(　path('Task/<int:task_id>/edit/', views.Task_Edit.as_view(), name='task_edit'))</td>
        <td>使用在create,update,detail</td>
    </tr>  
    <tr>
        <td>initial</td>
        <td>設定給form initial 參數,也可以透過form.py</td>
        <td></td>
    </tr>  
</table>

```python
class Task_Creat(CreateView):
    model = Task
    form_class = TaskForm   
    template_name = 'Task/Creat.html'
    success_url = reverse_lazy('task_View')   
```

### override form_valid

有些資料需要在後台編輯修改透過override form_valid()

```python
class Task_Edit(UpdateView):
    model = Task
    form_class=TaskForm  
    template_name = 'Edit.html'
    pk_url_kwarg = 'task_id'
    context_object_name = 'task' 

    def form_valid(self, form):         
        tasks = form.save(commit = False) 
        if tasks.status　==　"Close":
            tasks.end_date = datetime.datetime.now()       
        tasks.save()     
        return super().form_valid(form)    
```

### override get_context_data
```python
    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)  
        context['user'] = request.user
        return context
```

### override  get_form_kwargs
將參數傳給form使用
```python
    def get_form_kwargs(self):
        kwargs = super(task_create, self).get_form_kwargs()
        kwargs['user'] = self.request.user # pass the 'user' in kwargs
        return kwargs   
```

### override get_success_url
可以寫在success_url,但是需要傳入參數可以透過override get_success_url

```python
class Task_Edit(UpdateView):
    model = Task
    form_class = TaskForm  
    template_name = 'Edit.html' 
    
    def get_success_url(self):
        return reverse('task_detail', args=(self.object.id,))
        
```

### override get_object
```python
class Task_Edit(UpdateView):
    model = Task
    form_class = TaskForm  
    template_name = 'Edit.html' 
 
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
```

### override get

```python
class HWTask_Edit(UpdateView):
    model = Task
    form_class = TaskForm  
    template_name = 'Edit.html' 
    pk_url_kwarg = 'hwtask_id'   
 
    def get(self, request, *args, **kwargs): 
        obj = self.get_object()       
        if self.request.user != self.request.user:
            return super().get(request, *args, **kwargs)
        else:            
            return redirect('/accounts/access_error/')

```

## ListView

Attributes
<table>
    <tr>
        <th>名稱</th>
        <th>目的</th>
        <th>Note</th>        
    </tr>
     <tr>
        <td>paginate_by</td>
        <td>設定一頁多少筆資料</td>
        <td></td>
    </tr> 
    <tr>
        <td>ordering</td>
        <td>設定排序</td>
        <td></td>
    </tr>
    <tr>
        <td>queryset</td>
        <td></td>
        <td></td>
    </tr>  

</table>


```python
class Task_ListView(ListView):
    model = Task 
    template_name = 'Task/List.html'
    context_object_name = 'tasks'  
    paginate_by = 10
```



### override get

```python
    def get_queryset(self):    
        return Task.objects.all().fliter(owner = self.request.user)  
```

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


 
## DetailView


```python
class HWTask_Detail(DetailView): 
    model = HW
    template_name = 'HW/Detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'hwtask_id'
```

## Mixin

介紹一個View共用的方法，避免重複寫code，定義ActionEditGetMixin，覆寫get 

   
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
