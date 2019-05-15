# FBV Vs CBV


原文出處

Django視圖本質是一個函數：接受HttpRequest對像作為參數，返回一個HttpResponse對像作為返回.FBV直接就是這樣一個函數，而CBV類的方法as_view（），它的返回也是這樣一個函數。<br>
Django提供了一些通用視圖，基於通用類的視圖（GCBV），可以加快開發。實現所有內容。<br>

    
## FBV (Function Base View)

以下是簡單的FBV

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

**FormView**<br>
可以比較一下和FBV 的差異<br>

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


**ListView**<br>
ListView 搭配資料庫使用
model :模型
context_object_name :傳給template 資料名稱
template_name: 使用的模板
paginate_by :分頁

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