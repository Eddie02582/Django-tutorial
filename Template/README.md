



## reqroup
不管是list(dict) 資料或是queryset 資料,想要group by 特定欄位,因為django query不支援groupby,一般來說我們view 實作

```
cities = [
    {'name': 'Mumbai', 'population': '19,000,000', 'country': 'India'},
    {'name': 'Calcutta', 'population': '15,000,000', 'country': 'India'},
    {'name': 'New York', 'population': '20,000,000', 'country': 'USA'},
    {'name': 'Chicago', 'population': '7,000,000', 'country': 'USA'},
    {'name': 'Tokyo', 'population': '33,000,000', 'country': 'Japan'},
]
```

實作

```python 
    country_list = {}       
       
    for city  in cities:
        if city['country'] not in country_list:
            country_list[city['country']] = []
        country_list[city['country']].append(city)


```

```python
{
    'India': [
                {'name': 'Mumbai', 'population': '19,000,000', 'country': 'India'}, 
                {'name': 'Calcutta', 'population': '15,000,000', 'country': 'India'}
             ], 
    'USA': [
            {'name': 'New York', 'population': '20,000,000', 'country': 'USA'}, 
            {'name': 'Chicago', 'population': '7,000,000', 'country': 'USA'}
           ], 
    'Japan': [
                {'name': 'Tokyo', 'population': '33,000,000', 'country': 'Japan'}
             ]
}

```

html
```
<ul>
{% for key,v in country_list.items %}
    <li>{{ key }}
    <ul>
        {% for city in v %}
           <li>{{ city.name }}: {{ city.population }}</li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
</ul>
```

使用regroup
```
{% regroup cities by country as country_list %}

<ul>
{% for country in country_list %}
    <li>{{ country.grouper }}
    <ul>
        {% for city in country.list %}
          <li>{{ city.name }}: {{ city.population }}</li>
        {% endfor %}
    </ul>
    </li>
{% endfor %}
</ul>
```
  
但是資料如果位排序會有問題,需將先以country排序

```
{% regroup cities|dictsort:"country" by country as country_list %}  
```







