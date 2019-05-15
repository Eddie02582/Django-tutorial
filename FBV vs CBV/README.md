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

進階的寫法,希望成功後進入url**傳入參數**,因此改寫form_valid<br>

**view.py**
```python
class HWTask_Creat(CreateView):
    model = HW
    form_class=HWForm   
    template_name = 'Task/HW/Creat.html'
    def form_valid(self, form):         
        tasks = form.save(commit=False)         
        tasks.save()    
        return redirect('hwtask_detail', hwtask_id=tasks.pk) )   
```

若欄位含有ManytoMany Field 使用form.save_m2m()  使用或者直接使用form.save(commit=True) 


**view.py**
```python
class HWTask_Creat(CreateView):
    model = HW
    form_class=HWForm   
    template_name = 'Task/HW/Creat.html'  
    def form_valid(self, form):         
        tasks = form.save(commit=False)   
        form.save_m2m()  
        tasks.save()    
        return redirect('hwtask_detail', hwtask_id=tasks.pk)
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
    
    def form_valid(self, form):        
        tasks = form.save(commit=False)
        tasks.modify_date = timezone.now()        
        form.save_m2m()  
        tasks.save()
        return redirect('hwtask_detail', hwtask_id=tasks.pk) 
```


