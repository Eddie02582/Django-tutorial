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

```python
from django.template.loader import render_to_string
def ajax_get_user_data(request):
    if request.method == 'GET':
        context = {} 
        context ["users"] = User.objects.all()     


        html_form = render_to_string('Users.html',context,)     
         

        return JsonResponse({'html_form': html_form}) 
        
```

## example 3
    利用ajax 更新資料

html 模板 


```html

<!doctype html>
<html>
<head>
  <meta charset="utf-8">  
  <script src="jquery-3.3.1.min.js"></script> 
  <script src="bootstrap.min.js"></script>   
  <link rel="stylesheet" type="text/css" href="bootstrap.min.css"> 
</head>

<button class="btn btn-outline-primary" onclick="saveAllData()">Save All</button>
<table class="table table-horver table-striped" style="width:100%">    
    <tr>
        <th>Firstname</th>
        <th>Lastname</th>          
        <th>Gender</th>
        <th></th>
        <th></th>
    </tr>    
    <tr id="data-1">
        <td contenteditable="true" id="firstname-1">Howard</td>
        <td contenteditable="true" id="lastname-1">Lai</td>       
        <td contenteditable="true" id="gender-1">
            <select id="id_gender-1" class="form-control">  
                <option>male</option>   
                <option>female</option>                      
            </select>
        </td>  
        <td>
            <a onclick="saveData('1')" class="btn btn-primary">Save</a>
        </td>
        <td>
            <a onclick="deleteData('1')" class="btn btn-danger">Delete</a>
        </td>
      </tr>   
    <tr id="data-2">
        <td contenteditable="true" id="firstname-2">Lao</td>
        <td contenteditable="true" id="lastname-2">Da</td>       
        <td contenteditable="true" id="gender-2">
            <select id="id_gender-2" class="form-control">  
                <option>male</option>   
                <option>female</option>                      
            </select>
        </td>  
        <td>
            <a onclick="saveData('2')" class="btn btn-primary">Save</a>
        </td>
        <td>
            <a onclick="deleteData('2')" class="btn btn-danger">Delete</a>
        </td>
    </tr>         
</table>



<script>

     function saveData(id) {
        var editableFirstName = document.getElementById('firstname-'+id)
        var editableLastName = document.getElementById('lastname-'+id)       
        var editableGender = document.getElementById('id_gender-'+id)
        $.ajax({
            url: "/ajax/test_item_change/",   
            data: {
                    "firstname": editableFirstName.innerHTML, 
                    "lastname": editableLastName.innerHTML,
                    "gender": editableGender.options[editableGender.selectedIndex].value,                   
                    'id':id,
            },            
            type: "GET",
            dataType: "json",
          
          
        });  
    }
    
    function saveAllData() {
        dataid = $("[id^=data]");      
        var data_firstname = [];
        var data_lastname = [];
        var data_gender = [];
        var data_id = [];
 
        $("[id^=data]").each(function(){
            var id = $(this).attr('id').replace("data-","");
            var editableFirstName = document.getElementById('firstname-'+id)
            var editableLastName = document.getElementById('lastname-'+id)       
            var editableGender = document.getElementById('id_gender-'+id)
        
            var FirstName = editableFirstName.innerHTML        
            var LastName = editableLastName.innerHTML      
            var Gender = editableGender.options[editableGender.selectedIndex].value
            
            data_id.push(id);   
            data_firstname.push(FirstName);  
            data_lastname.push(LastName);  
            data_gender.push(Gender);    
        });
     
        $.ajax({
            url: "ajax/test_item_save_all/",             
            data: {          
                    'data_id':data_id,
                    'data_firstname':data_firstname,
                    'data_lastname':data_lastname,
                    'data_gender':data_gender,
            },            
            type: "GET",
            dataType: "json", 
            contentType: "application/x-www-form-urlencoded/json",
        });          
          
     };        
</script>
```


重點注意
<ul>
    <li>python讀取js傳入陣列的方法</li>
    <li>bulk_update 可以快速更新</li> 
</ul> 


js存入陣列在python 取資料的方法
```python
def ajax_test_item_save_all(request):
    if request.method == 'GET':
    
        data_firstname = request.GET.getlist('data_firstname[]')
        data_id = request.GET.getlist('data_id[]')
        data_gender = request.GET.getlist('data_gender[]')
        data_lastname = request.GET.getlist('data_lastname[]')  
   
        objs = [ User.objects.get(id = id) for id in data_id]
        for i in range(len(objs)):          
            objs[i].firstname = data_firstname[i]           
            objs[i].gender = data_gender[i]  
            objs[i].lastname = data_lastname[i]       
        User.objects.bulk_update(objs, ['firstname','gender','lastname'])       
        return JsonResponse("",safe = False)    
```


























```






















