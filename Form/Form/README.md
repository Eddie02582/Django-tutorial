# Form



## Form.py

**form.py**

```python 
from django import forms			 
class APLossForm(forms.Form):
    FreqInMHz  = forms.FloatField(label='Freq (MHz)', required=True)
    levelInDb  = forms.FloatField(label='Rssi Level In dB', required=True)
```





**view.py**

<ul>
    <li>form = APLossForm()</li>
    <li>form = APLossForm(request.POST)取得form POST 的資料</li>   
    <li>form.is_valid() 用來驗證表單資料是否正確</li>
    <li>form.cleaned_data[field] 取得資料(field 對應form.py欄位)</li>
</ul>


```python 
def ApLoss_View(request):	
    form = APLossForm()  
    if request.method == 'POST':
        form = APLossForm(request.POST)	
        if form.is_valid():             
            Freq = form.cleaned_data.get('FreqInMHz')         
            levelInDb = form.cleaned_data['levelInDb']
            result = (27.55 - (20 * math.log10(Freq)) + math.fabs(levelInDb)) / 20.0
            meters = math.pow(10, result)       
            feet = meters * 3.2808            	    
            return render(request, 'APLoss.html', {'form': form,'feet':feet,'meters':meters})		        
    else:        
        return render(request, 'APLoss.html', {'form': form})	

```











    
    
    
    
    
    
    