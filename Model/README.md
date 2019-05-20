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
## Field

### Field Introduction
介紹一些常用的
<table>
    <tr>
        <th>Fiele</th>
        <th></th>        
    </tr>
    <tr>
        <td>AutoField</td>
        <td>一個自動增加的整數類型字段。通常你不需要自己編寫它，Django會自動幫你添加字段：id = models.AutoField(primary_key=True)，這是一個自增字段，從1開始計數。如果你非要自己設置主鍵，那麼請務必將字段設置為primary_key=True。 Django在一個模型中只允許有一個自增字段，並且該字段必須為主鍵！</td>
    </tr>
    <tr>
        <td>BigAutoField</td>
        <td>A 64-bit integer, much like an AutoField except that it is guaranteed to fit numbers from 1 to 9223372036854775807.</td>
    </tr>    
    <tr>
        <td>BigIntegerField</td>
        <td>範圍為-9223372036854775808 到9223372036854775807。在Django的模板表單為一個textinput標籤。</td>
    </tr>
     <tr>
        <td>BinaryField</td>
        <td>A field to store raw binary data. It can be assigned bytes, bytearray, or memoryview. By default, BinaryField sets editable to False, in which case it can’t be included in a ModelForm.Older versions don’t allow setting editable to True.</td>
    </tr>
    <tr>
        <td>BooleanField</td>
        <td>The default form widget for this field is CheckboxInput, or NullBooleanSelect if null=True.The default value of BooleanField is None when Field.default isn’t defined.</td>
    </tr>
    <tr>
        <td>CharField</td>
        <td>字符串類型。必須接收一個max_length參數，表示字符串長度不能超過該值。默認的表單標籤是TextInput</td>
    </tr>
    <tr>
        <td>DateField</td>
        <td>class DateField(auto_now=False, auto_now_add=False, **options)</br> 
            auto_now:每當對像被保存時將字段設為當前日期，常用於保存最後修改時間。</br> 
            auto_now_add：每當對像被創建時，設為當前日期，常用於保存創建日期(注意是不可以修改)。</br> 
            設置上面兩個參數相當於給field添加了editable=False和blank=True</br> 
            如果想具有修改屬性，請用default參數。</br> 
            For DateField: default=date.today - from datetime.date.today()</br> 
            For DateTimeField: default=timezone.now - from django.utils.timezone.now()</br> 
            在HTML中為TextInput標籤。在admin後台中，Django會自動產生JS的日曆表和一個“Today”快捷方式，以及附加的日期合法性驗證。兩個重要參數：（參數互斥，不能共存）</br> 
        </td>            
    </tr>    
    <tr>
        <td>DecimalField</td>
        <td>對象的詳細信息</td>
    </tr>    
    <tr>
        <td>DurationField</td>
        <td>持續時間類型。存儲一定期間的時間長度。類似Python中的timedelta。在不同的數據庫實現中有不同的表示方法。常用於進行時間之間的加減運算。但是小心了， PostgreSQL等數據庫之間有兼容性問題！</td>
    </tr>
    <tr>
        <td>EmailField</td>
        <td>郵箱類型，默認max_length最大長度254位。使用這個字段的好處是，可以使用DJango內置的EmailValidator進行郵箱地址合法性驗證</td>
    </tr>
    <tr>
        <td>FileField</td>
        <td>更新對象</td>
    </tr>
    <tr>
        <td>FilePathField</td>
        <td>刪除對象</td>
    </tr>
        <tr>
        <td>FloatField</td>
        <td>相當於Python的float實例，當localize=False時，它在HTML為NumberInput標籤，否則是TextInput類型</td>
    </tr>
        <tr>
        <td>ImageField</td>
        <td>刪除對象</td>
    </tr>
        <tr>
        <td>IntegerField</td>
        <td>An integer. Values from -2147483648 to 2147483647 are safe in all databases supported by Django.The default form widget for this field is a NumberInput when localize is False or TextInput otherwise.</td>
    </tr>
        <tr>
        <td>GenericIPAddressField</td>
        <td>刪除對象</td>
    </tr>
        <tr>
        <td>NullBooleanField</td>
        <td>類似BooleanField，只不過額外允許NULL作為選項之一</td>
    </tr>
    <tr>
        <td>PositiveIntegerField</td>
        <td>正整數，包含0,最大2147483647。</td>
    </tr>
</table>