# Export Table

介紹兩種方法
<ol>
    <li>encodeURIComponent</li>
    <li>FileSaver</li>
</ol>



## innerHTML

#### 1.  script
 ``` javascript
    function Table2Excel(table_id,name) {
      
      var table= document.getElementById(table_id).innerHTML
      var data={'table': table};      
	  
      table= "<table border=\"1\">" + table + "</table>"; 	 
      var uri = 'data:text/csv;charset=utf-8,' + encodeURIComponent(table);   
      var download_link = document.createElement('a');
      download_link.href = uri;  
      download_link.download = name+".xlsx"; 
      document.body.appendChild(download_link);
      download_link.click();
      document.body.removeChild(download_link);
    }   
```

## FileSaver

<a href = https://github.com/eligrey/FileSaver.js/>參考 eligrey </a>


#### 1. Include script

```html
<script src="FileSaver.js"></script>
```


#### 2. html Add javasctipt
 ``` html
<script>
function ExportTable2Excel(table_id,name) {
          
    var table= document.getElementById(table_id).innerHTML
    var data={'table': table}; 
    table= "<table border=\"1\">" + table + "</table>";    
    var filename = name+".xlsx"; 
    
    var blob = new Blob([table], {
            type: "text/csv;charset=utf-8"
    });          
    saveAs(blob,filename);
  
  }  
</script>
```

















