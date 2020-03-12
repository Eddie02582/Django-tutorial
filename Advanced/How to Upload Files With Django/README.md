# How to Upload Files With Django

<a href = "https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html">可以參考原文</a>

如果是使用model.form download file ,django 會自行處理,如果今天是使用model.form 或是在html自行撰寫的要如何處理


建立html
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="file" name="myfile">
    <input type="submit" value="Submit">
</form>
```







