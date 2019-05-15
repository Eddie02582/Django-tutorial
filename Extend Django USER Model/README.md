# Extend Django USER Model

Django的內置身份驗證系統非常棒。 在大多數情況下，我們可以開箱即用，節省了大量的開發和測試工作。它適合大多數用例，非常安全。但有時我們需要做一些微調，以適應我們的Web應用程序。
通常我們希望存儲與我們的用戶相關的更多數據。如果您的Web應用程序具有社交吸引力，您可能希望存儲簡短的生物，用戶的位置以及其他類似的東西。在本教程中，我將介紹可用於簡單擴展默認Django用戶模型的策略，因此您無需從頭開始實現所有內容。<br>



Django中有幾種方式。
>
> > 1.Proxy Model：對Django用戶提供的所有內容感到滿意，並且不需要存儲額外的信息。
>
> > 2.User Profile：對Django處理身份驗證的方式感到滿意，並且需要向用戶添加一些非身份驗證相關的屬性。
>
> > 3.Custom User Model from AbstractBaseUser:Django處理身份驗證的方式不適合您的需求。
>
> > 4.Custom User Model from AbstractUser:Django處理auth的方式非常適合您的需求，但仍然希望添加額外的屬性而無需創建單獨的模型。
    
## Using a Proxy Model
**什麼是代理模型？**<br>
它是一種模型繼承，無需在數據庫中創建新表。 它用於更改現有模型的行為（例如，默認排序，添加新方法等），而不會影響現有數據庫模式。<br>

**我什麼時候應該使用代理模型？**<br>
當您不需要在數據庫中存儲額外信息時，您應該使用代理模型來擴展現有的用戶模型，而只需添加額外的方法或更改模型的查詢管理器。<br><br>

這是擴展現有用戶模型的侵入性較小的方法。 這種策略不會有任何缺點。 但它在很多方面都非常有限。<br>


```python
from django.contrib.auth.models import User
from .managers import PersonManager
class Person(User):
    objects = PersonManager()
    class Meta:
        proxy = True
        ordering = ('first_name', )
    def do_something(self):
        ...
```
這是在上面的示例中，我們定義了一個名為Person的代理模型。 我們通過在Meta類中添加以下屬性來告訴Django這是一個代理模型：proxy = True。<br>
在這種情況下，重新定義了默認排序，為模型分配了自定義管理器，還定義了一個新方法do_something。<br>
值得注意的是，User.objects.all（）和Person.objects.all（）將查詢相同的數據庫表。 唯一的區別在於我們為代理模型定義的行為。<br>


