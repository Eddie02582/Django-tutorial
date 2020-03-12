# Model Example


觀看範例請先閱讀
<
<u1>
    <li> <a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Field#field-introduction"> Field Introduction</a></li>
    <li> <a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Field#field-option"> Field Option</a></li>
    <li><a href = "https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Relationships#many-to-one">Many-to-One</a></li>
</ul>



建立一個每周會議紀錄的模型,包含一個Meeting的模型和一個Records的模型



``` python
from django.db import models

class Meeting(models.Model):  
    year = models.IntegerField()
    week = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
   
    
    '''
        一般使用Meeting.objects.all(),結果<QuerySet[<Meeting:Meeting object (1)>,<Meeting:Meeting object (1)>]>
        透過__str__,結果<QuerySet[<Meeting:2019-08>,<Meeting:2019-09>]>....
    
    '''
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return "{0}-W{1}".format(self.year,self.week)   
   
    def get_week_start(self):
        return datetime.datetime.strptime("{0}-W{1}-{2}".format(self.year,self.week,1), '%G-W%V-%u').date()

    def get_week_end(self):
        return datetime.datetime.strptime("{0}-W{1}-{2}".format(self.year,self.week,7), '%G-W%V-%u').date()

```
<ul>
    <li>定義__str__,修改查詢返回値的內容</li>
    <li>自訂函數:透過自訂函數, 便可以透過meeting.get_week_start</li>
</ul>


``` python

class 包含一個Meeting的模型和一個Records的模型(models.Model): 
    Status_CHOICES = (
        ('Close', 'Close'),       
		('Open', 'Open'),        
    ) 
   
    Item = models.CharField(max_length = 200,default='',null = False,blank = False)   
    #透過使用choices 變成下拉式選單
    status = models.CharField(max_length = 10, null = False,choices = Status_CHOICES,default='Open')
    meeting = models.ForeignKey(Meeting, related_name='has_items',on_delete=models.CASCADE)
```



## Model Example
好文分享<href>https://simpleisbetterthancomplex.com/series/2017/09/11/a-complete-beginners-guide-to-django-part-2.html<href>
