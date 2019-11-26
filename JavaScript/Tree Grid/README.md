# Tree Grid














## Tree Grid with django modle 

### ｍodle

假設model 如下

```python
class Tasks(models.Model):
    name=models.CharField(max_length=50, null=False,default="")  
    duration= models.CharField(max_length=10,blank=True,default="")  
    start_date = models.DateTimeField('開始日期',null=True, blank=True)	
    end_date = models.DateTimeField('結束日期',null=True, blank=True)
    node_level=models.IntegerField(null=True,blank=True,default=0) 
    parent=models.IntegerField(null=True,default="", blank=True) 

```