# Excel Table

<a href = https://github.com/chestercharles/excel-bootstrap-table-filter>參考 chestercharles github </a>



<img src = "1.png"> 






## 如何使用

<a href ="https://github.com/Eddie02582/Django-tutorial/blob/master/JavaScript/Excel%20Table/excel-bootstrap-table-filter-style.html">example code</a>
#### 1. Include css/script

```html
<script src="excel-bootstrap-table-filter-bundle.js"></script>
<link rel="stylesheet" href="excel-bootstrap-table-filter-style.css">
```

#### 2. Add javasctipt
指定要excelTableFilter的table

```html
 <script>
    $('#table-info').excelTableFilter();
  </script> 
```
#### 3.Advance

透過class 指定謀先欄位是否要sort/filter

```
    <thead>
      <tr>
        <th class = "no-filter no-sort">Firstname</th>
        <th class = "no-filter">Lastname</th>
        <th>Team</th>       
      </tr>
    </thead>
```















