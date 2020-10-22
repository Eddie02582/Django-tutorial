# FBV 

    
## FBV (Function Base View)

以下是簡單的FBV
**view.py**

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
            
    return return render(request, 'APLoss.html')
```


**url.py**
```python
    path('APLoss/', views.ApLoss_View, name='AP_Loss'),	
```
