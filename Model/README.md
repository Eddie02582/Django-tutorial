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


<ul>
    <li><a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Field">Field</a>  
        <ul>
            <li> <a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Field#field-introduction"> Field Introduction</a></li>
            <li> <a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Field#field-option"> Field Option</a></li>                              
        </ul>
    </li>  
    <li><a href="https://github.com/Eddie02582/Django-tutorial/blob/master/Model/Example/README.md">Example</a></li>      
    <li><a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Relationships">Relationships</a>
        <ul>
            <li><a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Relationships#many-to-one">Many-to-One</a></li>
            <li><a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Relationships#many-to-many">Many-to-Many</a></li>
            <li><a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Relationships#one-to-one">One-to-One</a></li>
        </ul>
    </li>   
    <li>  
        <a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Inheritance">Django-Model Inheritance</a>
        <ul>
            <li><a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Inheritance#1abstract-base-classes">Abstract base classes</a></li>
            <li><a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Inheritance#2multi-table-inheritance">Multi-table inheritance</a></li>
            <li><a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Inheritance#3proxy">Proxy</a></li>
        </ul>
    </li>  
    <li>  
        <a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Model/QuerySet">QuerySet</a>
        <ul>
            <li><a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/QuerySet#1create-object">Create Object</a></li>
            <li><a href=https://github.com/Eddie02582/Django-tutorial/tree/master/Model/QuerySet#2query>Query</a></li>
        </ul>
    </li>
    
</ul>


