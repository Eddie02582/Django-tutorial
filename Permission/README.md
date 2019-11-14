# Permission

有時候我們會希望特定'網頁需要登入或是規範特定類別的人能使用
分別介紹兩種decorator

1.permission_required(perm, login_url=None, raise_exception=False) 
>> perm:設定權限 </br> 
>>>    add: user.has_perm('foo.add_hw')</br>
>>>    change: user.has_perm('foo.change_hw')</br>
>>>    delete: user.has_perm('foo.delete_hw')</br>
>>>    view: user.has_perm('foo.view_hw') </br>     
  
>>  login_url :沒權限導入的網址</br>
>>  raise_exception: 是否raise PermissionDenied (403)</br>




2.login_required(redirect_field_name='next', login_url=None)</br>
>如果用戶未登錄，則重定向到settings.LOGIN_URL</br>
>如果用戶已登錄，請正常執行視圖。 視圖代碼可以自由地假設用戶已登錄。</br>
>默認情況下，成功驗證時用戶應重定向到的路徑存儲在名為“next”的查詢字符串參數中。 如果您希望為此參數使用其他名稱，則login_required（）將使用可選的redirect_field_name參數：</br>
>基本上直接使用login_required()

    
以下有兩種方法分別在view.py 或是url.py 使用 
 
 
## View.py 

**FBV**

```python
@login_required
def HWTask_Detail(request,hwtask_id): 
    task = get_object_or_404(HW, pk=hwtask_id) 
    return render(request, 'HW/Detail.html', {'task': task})

@permission_required('catalog.view_hw',login_url='/accounts/access_error/')
def HWTask_Detail(request,hwtask_id): 
    task = get_object_or_404(HW, pk=hwtask_id) 
    return render(request, 'HW/Detail.html', {'task': task})

```

**GCBV (Generic Class-Based View)**

裝飾login_required 在dispatch method

```python	
@method_decorator(login_required(),name='dispatch') 		
class HWTask_Create(CreateView):
    model = HW
    form_class=HWForm	
    template_name = 'HW/Creat.html'  
```       

也可以裝飾在method上面

```python	
class HWTask_Create(CreateView):
    model = HW
    form_class=HWForm	
    template_name = 'HW/Creat.html'  
    
    @method_decorator(login_required()) 
    def get(self, request, *args, **kwargs): 
        return super().get(request, *args, **kwargs)
```      

使用多個裝飾，檢查條件由上往下，在未登入的情況下會導入登入介面，已登入的情況在判斷permission


```python	
@method_decorator(login_required(),name='dispatch') 	
@method_decorator(permission_required('catalog.add_hw',login_url='/accounts/access_error/'),name='dispatch')	
class HWTask_Create(CreateView):
    model = HW
    form_class=HWForm	
    template_name = 'HW/Creat.html'      
``` 


## url.py 
也可以在url.py 直接使用裝飾器


**FBV**
```python
path('HWTask/<int:hwtask_id>/', login_required(views.HWTask_Detail), name='hwtask_detail'),
path('HWTask/<int:hwtask_id>/', permission_required('catalog.add_hw',login_url='/accounts/access_error/')(views.HWTask_Detail)), name='hwtask_detail'),
``` 





**GCBV (Generic Class-Based View)**
```python
path('HWTask_Create/', permission_required('catalog.add_hw')(views.HWTask_Create.as_view())),
path('HWTask_Create/', login_required(views.HWTask_Create.as_view()), name='hwtask_create'),  	
path('HWTask_Create/', permission_required('catalog.add_hw',login_url='/accounts/access_error/')(views.HWTask_Create.as_view()), name='hwtask_create'),
``` 


















