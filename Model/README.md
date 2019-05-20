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

<table>    
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
        <td>class DecimalField(max_digits=None, decimal_places=None, **options)</br> 
        固定精度的十進制小數。相當於Python的Decimal實例，有兩個指定的參數max_digits：最大的位數，必須大於或等於小數點位數 。 </br> 
        decimal_places：小數點位數，精度。</br> 
        例子：儲存最大不超過999，帶有2位小數位精度的數，定義如下：models.DecimalField(..., max_digits=5, decimal_places=2)。</br> 
        當localize=False時，它在HTML為NumberInput標籤，否則是text類型</br> 
        </td>
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
        <td></td>
    </tr>
    <tr>
        <td>FilePathField</td>
        <td></td>
    </tr>
        <tr>
        <td>FloatField</td>
        <td>相當於Python的float實例，當localize=False時，它在HTML為NumberInput標籤，否則是TextInput類型</td>
    </tr>
        <tr>
        <td>ImageField</td>
        <td></td>
    </tr>
        <tr>
        <td>IntegerField</td>
        <td>An integer. Values from -2147483648 to 2147483647 are safe in all databases supported by Django.The default form widget for this field is a NumberInput when localize is False or TextInput otherwise.</td>
    </tr>
        <tr>
        <td>GenericIPAddressField</td>
        <td>class GenericIPAddressField(protocol=’both’, unpack_ipv4=False, **options) </br> 
            IPV4者IPV6地址，字符串形式，例如192.0.2.30或者2a02:42fe::4在HTML中為TextInput標籤。</br> 
            參數protocol默認值為‘both’，可選‘IPv4’或者‘IPv6’</br> 
        </td>
    </tr>
    <tr>
        <td>NullBooleanField</td>
        <td>類似BooleanField，只不過額外允許NULL作為選項之一</td>
    </tr>
    <tr>
        <td>PositiveIntegerField</td>
        <td>正整數，包含0,最大2147483647。</td>
    </tr>
      <tr>
        <td>PositiveSmallIntegerField</td>
        <td>正整數，包含0,最大2147483647。</td>
    </tr>
      <tr>
        <td>SlugField</td>
        <td>slug是一個新聞行業的術語。一個slug就是一個某種東西的簡短標籤，包含字母、數字、下劃線或者連接線，通常用於URLs中。可以設置max_length參數，默認為50</td>
    </tr>
      <tr>
        <td>SmallIntegerField</td>
        <td>整數，範圍-32768到32767。</td>
    </tr>
      <tr>
        <td>TextField</td>
        <td>大量文本內容，在HTML中為Textarea標籤，如果設置max_length參數，那麼在前端頁面中會受到輸入字符數量限制，然而在模型和數據庫層面卻不受影響。只有CharField才能同時作用於兩者</td>
    </tr>
      <tr>
        <td>TimeField</td>
        <td>時間字段，Python中datetime.time的實例。接收同DateField一樣的參數，只作用於小時、分和秒</td>
    </tr>
      <tr>
        <td>URLField</td>
        <td>一個用於保存URL地址的字符串類型，默認最大長度200。</td>
    </tr>
    <tr>
        <td>UUIDField</td>
        <td>用於保存通用唯一識別碼（Universally Unique Identifier）的字段。使用Python的UUID類。在PostgreSQL數據庫中保存為uuid類型，其它數據庫中為char(32)。這個字段是自增主鍵的最佳替代品，後面有例子展示。</td>
    </tr>
</table>


### Field Option



<table>
    <tr>
        <th>Options</th>
        <th></th>        
    </tr>
    <tr>
        <td>null</td>
        <td>If True, Django will store empty values as NULL in the database. Default is False.</td>
    </tr>
    <tr>
        <td>blank</td>
        <td>If True, the field is allowed to be blank. Default is False.</br> 
            Note that this is different than null. null is purely database-related, whereas blank is validation-related.</br> 
            If a field has blank=True, form validation will allow entry of an empty value. If a field has blank=False,the field will be required.</br> 
        </td>
    </tr>    
    <tr>
        <td>choices</td>
        <td>An iterable (e.g., a list or tuple) of 2-tuples to use as choices for this field. If this is given, the default form widget will be a select box instead of the standard text field and will limit choices to the choices given.The first element in each tuple is the value that will be stored in the database. The second element is displayed by the field’s form widget.</td>
    </tr>
    <tr>
        <td>default</td>
        <td>The default value for the field. This can be a value or a callable object. If callable it will be called every time a new object is created.</td>
    </tr>
    <tr>
        <td>help_text</td>
        <td>Extra “help” text to be displayed with the form widget. It’s useful for documentation even if your field isn’t used on a form.</td>
    </tr>
    <tr>
        <td>primary_key</td>
        <td>If True, this field is the primary key for the model.If you don’t specify primary_key=True for any fields in your model, Django will automatically add an IntegerField to hold the primary key, so you don’t need to set primary_key=True on any of your fields unless you want to override the default primary-key behavior. For more, see Automatic primary key fields. The primary key field is read-only.</td>
    </tr>
    <tr>
        <td>verbose_name</td>
        <td>Each field type, except for ForeignKey, ManyToManyField and OneToOneField, takes an optional first positional argument – a verbose name. If the verbose name isn’t given, Django will automatically create it using the field’s attribute name, converting underscores to spaces.</td>
    </tr>
</table>