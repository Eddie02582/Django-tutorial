# ORM  
Python 模型是採用ORM(object-relational mapping,物件關聯映射) ，它的作用是在關係數據庫和業務實體對象之間作一個映射，這樣，我們在具體的操作業務對象的時候，就不需要再去和複雜的SQL語句打交道，只需簡單的操作對象的屬性和方法。</br>

以下簡單定義模型(model.py)


```python 

from django.db import models
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)    
```

以上代碼相當於SQL

```sql
CREATE TABLE myapp_person (
    "id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);
```

新增修改模型cmd執行以下指令</br>

```
python manage.py makemigrations [app]

python manage.py migrate
```

建立migrations folder
```
python manage.py makemigrations --empty app
```


以下Model相關介紹

<a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Field">Field</a>
<u1>
    <li>Field Introduction</li>
    <li>Field Option</li>
</ul>



<a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Inheritance">Django-Model Inheritance</a>
<u1>
    <li>Abstract base classes</li>
    <li>Multi-table inheritance</li>
    <li>Proxy</li>
</ul>