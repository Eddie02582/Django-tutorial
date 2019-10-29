#Show Pdf file in web

我們想在網頁上直接開啟pdf 或是png 檔






## View 

view.py

``` python 
def download_attach(request,filename):	
    from django.conf import settings  
    path = settings.MEDIA_ROOT+"\\"+filename
    content_types = {
                        'pdf':'application/pdf',
                        'jpg':'image/jpeg',
                        'jfif':'image/jpeg',
                        'png':'image/png',                  
                        # 'bmp':'application/x-bmp',
                        'wbmp':'image/vnd.wap.wbmp',
                        'tiff':'image/tiff',
                        'xls':'application/vnd.ms-excel',                    
                        'xlsx':'application/vnd.ms-excel',
                        'text':'text/xml',
                        '.ppt':'application/vnd.ms-powerpoint',
                    }
    try:
        path = path.lower()
        extension = path.split('.')[-1]
        if extension in content_types:
            return FileResponse(open(path, 'rb'), content_type=content_types[extension])       
        else:
            file = open(path, 'rb')
            filename = path.split('/')[-1]             
            response = HttpResponse(file)
            response['Content-Type'] = 'application/octet-stream' 
            response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
            return response            
    except FileNotFoundError:
            raise Http404()
``` 

並在url.py 新增 
``` python 
  path('download_attach/<str:filename>/', views.download_attach, name='download_attach'),
``` 


