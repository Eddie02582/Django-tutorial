# Migrate DataBase from SQLite to PostgreSQL

這邊以SQLite to PostgreSQL

有幾個步驟

## 正常做法

### Dump data
將資料dump 出來
```
python manage.py dumpdata > db.json
```

### 建立PostgreSQL DataBase
這邊使用pgAdmin建立<br>
#### 先建立使用者
步驟如下

<img src="1.png">
設定使用者名稱
<img src="2.png">
設定密碼
<img src="3.png">
設定權限
<img src="4.png">

#### 建立資料庫

<img src="5.png" >
設定資料庫名稱 和對應使用者
<img src="6.png" >

### 修改 setting.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Test',
        'USER': 'Eddie',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```



### 遷移資料庫
```
python manage migrate
```

### 修復資料
```
python manage shell
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()
```

### 將資料載入進資料庫
```
python manage.py loaddata db.json
```

## python manage migrate error
假設你使用<a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Extend%20Django%20USER%20Model#using-one-to-one-link-with-a-user-modelprofile">Using One-To-One Link With a User Model(Profile) </a>

可能會使得python manage.py migrate報錯,這時候你可能需要分開

```
python manage migrate auth
python manage migrate 
```

如果還是不行,請照下面作法

將url 相關app 註解 和setting.py installapp註解

在執行 python manage.py migrate auth即可

在把 setting install app 取消註解

執行 python manage.py migrate 










