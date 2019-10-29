# Ajax

有時候我們希望網頁在不重新讀取的情況下更新資料


## example 1

利用ajax 連動 下拉選單



view.py 建立一個 ajax_get_city_choices函數
```python
def ajax_get_city_choices(request):
    if request.method == 'GET':
        country = request.GET.get('country', None) 
        city = []
        data = {}
        if country == "Taiwan":
            city =["Taipei","Tainan","Kaohsiung"]
        elif country == "China":
            city =["Suzhou","Shanghai"]
        elif country == "Japan":
            city =["Osaka","Tokyo"]
        data["city"] = city     
        return JsonResponse(data,safe = False)

def ajax_example(request):   
    return render(request,'Ajax.html')	
```

再url.py 新增ajax網址
```python
    #path('ajax/test_item_save_all/', views.ajax_test_item_save_all, name='ajax_test_item_save_all'),
    re_path(r'^ajax/test_item_save_all/$', views.ajax_test_item_save_all, name='ajax_test_item_save_all'), 
```



在 Ajax.html 使用 jquery 呼叫ajax,再覆寫 select
```html

{% load static %}
<!doctype html>
<html>
<head>
  <meta charset="utf-8">  
  <script src="{% static 'js/jquery-3.3.1.min.js' %}"></script> 
  <script src="{% static 'js/bootstrap.min.js' %}"></script>  
  <link rel="stylesheet" type="text/css" href="{% static 'css/bootstrap.min.css' %}"> 
</head>

<h1>Ajax Example </h1>

<form method="POST" class="post-form." enctype="multipart/form-data">
	{% csrf_token %}    
    <select id ="select-country">
            <option value=""></option>
            <option value="Taiwan">Taiwan</option>
            <option value="Japan">Japan</option>
            <option value="China">China</option>    
        </select>
    <br>
    <select id ="select-city">
        <option value=""></option>          
    </select>     
</form>


<script>
    function load_city_choice () {  
		var country = $(this).val();
        // var country = $("#select-country").val();
		var data = {'country':country} ;
        
		$.get("/ajax/get_city_choices",data, function(data){ 
            var content = ''; 
                $.each(data["city"], function(i, item) {                                                                       
                     content += '<option value=' + item + '>' + item + '</option>'
                    });
                $('#select-city').html(content);  
			})    
   
	} 
	
	$("#select-country").change(load_city_choice);

</script>



```

## example 2

利用ajax 顯示table

table html template
```html
<table class="table table-striped table-horver" id="table-info">
    <thead>
      <tr>
        <th>Firstname</th>
        <th>Lastname</th>
        <th>Email</th>
      </tr>
    </thead>
    <tbody>
      {% for user in users %}   
      <tr>
        {{for user in users}}
        <td>{{user.firstname}}</td>
        <td>{{user.lastname}}</td>
        <td>{{user.email}}</td>
      </tr>
      {% endfor %} 

    </tbody>
</table>
```

html 模板
```html
	<div id="Users-content"> 
	</div>
    
    <script>
        function load_users_content () {           
       
            var data = {} ;	
            
            $.get("/ajax/get_user_data",data, function(data){
                $('#Users-content').html(data.html_form);                    
            })    
           
        }    
    </script>
```

```

from django.template.loader import render_to_string
def ajax_get_user_data(request):
    if request.method == 'GET':
        context = {} 
        context ["users"] = User.objects.all()     


        html_form = render_to_string('Users.html',
            context,            
            )     
         

        return JsonResponse({'html_form': html_form}) 
        
```

























