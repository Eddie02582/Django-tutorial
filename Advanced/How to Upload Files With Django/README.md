# How to Upload Files With Django


表單上傳的檔案物件儲存request.FILES中，表單格式需為multipart/form-data
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="file" name="myfile" required>
    <input type="submit" value="Submit">
</form>
```

request.FILES中的key來自於表單中的<input type=”file” name=”” />的name值：
```
request.FILES['file']
```


## Simple File Upload

### FileSystemStorage
路徑會指向media
```python
def simple_upload(request):
    if request.method == 'POST':        
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)       
    return render(request, 'simple_upload.html')

```
### open
此方法用於存在本地

```python
def handle_upload_file(f,path):
    file_path = path + f.name
    with open(path,'wb+') as destination:
        for chunk in f.cunks():
            destination.write(chunk)

    return file_path
def simple_upload(request):
    if request.method == 'POST':        
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)       
    return render(request, 'simple_upload.html')

```
## Model Form






