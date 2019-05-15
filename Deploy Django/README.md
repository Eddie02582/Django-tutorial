# Deploy Django


    
## Appache


** For Windows**<br/>

首先到官網下載 <href>https://httpd.apache.org/download.cgi</href><br/>

找到 Apache24\conf\httpd.conf 並依序修改<br/>

1.確認SRVROOT 路徑正確
> Define SRVROOT "D:/Apache24"
> ServerRoot "${SRVROOT}"

2.設定port Listen:8008
```
> # prevent Apache from glomming onto all bound IP addresses.
> #
> #Listen 12.34.56.78:80
> Listen 8008
```

3.設定python 路徑 和 wsgi路徑
```

#
# Dynamic Shared Object (DSO) Support
#
# To be able to use the functionality of a module which was built as a DSO you
# have to place corresponding `LoadModule' lines at this location so the
# directives contained in it are actually available _before_ they are used.
# Statically compiled modules (those listed by `httpd -l') do not need
# to be loaded here.
#
# Example:
# LoadModule foo_module modules/mod_foo.so
#

**LoadFile** "D:\Python\Python_Venv\Python36\djsc\Scripts\python36.dll"  
**LoadModule** wsgi_module "D:\Python\Python_Venv\Python36\djsc\Lib\site-packages\mod_wsgi\server\mod_wsgi.cp36-win_amd64.pyd"

LoadModule access_compat_module modules/mod_access_compat.so
LoadModule actions_module modules/mod_actions.so

```python

