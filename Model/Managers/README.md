# Managers

以下介紹如何自訂修改Manager方法</br>



## Adding extra manager methods

### through manager

額外增加的方法沒有限定必須返回 QuerySet,PollManager 繼承models.Manager並額外新增with_counts的方法，它會返回包含所有 OpinionPoll 對象的列表,每個objects都有一個額外屬性 num_response，這是一次聚合查詢的結果

```python
from django.db import models

class PollManager(models.Manager):
    def with_counts(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.question, p.poll_date, COUNT(*)
                FROM polls_opinionpoll p, polls_response r
                WHERE p.id = r.poll_id
                GROUP BY p.id, p.question, p.poll_date
                ORDER BY p.poll_date DESC""")
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], question=row[1], poll_date=row[2])
                p.num_responses = row[3]
                result_list.append(p)
        return result_list

class OpinionPoll(models.Model):
    question = models.CharField(max_length=200)
    poll_date = models.DateField()
    objects = PollManager()

class Response(models.Model):
    poll = models.ForeignKey(OpinionPoll, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=50)
    response = models.TextField()
    
```
通過本例，你可以利用 OpinionPoll.objects.with_counts() 返回一個包含 OpinionPoll 對象的列表，每個對像都有 num_responses 屬性。

### through queryset

```python
from django.db import models
from django.db.models.aggregates import Count, Max, Min

class PollQuerySet(models.QuerySet):
    def with_counts(self):        
        return self.prefetch_related("has_respones").annotate(count = Count('has_respones'),)

class OpinionPoll(models.Model):
    question = models.CharField(max_length=200)
    poll_date = models.DateField()  
    objects = PollQuerySet.as_manager()

class Response(models.Model):
    poll = models.ForeignKey(OpinionPoll,related_name='has_respones', on_delete=models.CASCADE)
    person_name = models.CharField(max_length=50)
    response = models.TextField()    
```



## Modifying a manager’s initial QuerySet

### through manager
是新增一個manager並修改QuerySet

Manager 的基础 QuerySet 会返回系统中所有的对象。例如，使用以下模型:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
```  
    

可以通過重寫 Manager.get_queryset() 方法來覆蓋 Manager 的基礎 QuerySet。 get_queryset() 返回的 QuerySet 應該包含你需要的屬性。<br>

例如，以下模型有 兩個 Manager —— 一個返回所有對象，另一個僅返回 Roald Dahl 寫的書<br>


```python
class DahlBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(author='Roald Dahl')

# Then hook it into the Book model explicitly.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

    objects = models.Manager() # The default manager.
    dahl_objects = DahlBookManager() # The Dahl-specific manager.
```  
  
使用這個實例模型時， Book.objects.all() 會返回數據庫中所有的書，而 Book.dahl_objects.all() 僅返回 Roald Dahl 寫的書<br>

### through queryset

```python
class DahlBookQuerySet(models.QuerySet):
    def get_queryset(self):
        return super().get_queryset().filter(author='Roald Dahl')
        
        

# Then hook it into the Book model explicitly.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)

    objects = models.Manager() # The default manager.
    dahl_objects = DahlBookQuerySet.as_manager() # The Dahl-specific manager.
```  











