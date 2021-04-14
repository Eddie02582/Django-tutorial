# Django dumpdata and loaddata


## dumpdata
It is a django management command, which can be use to backup(export) you model instances or whole database


### database dump
Following command will dump whole database in to a db.json file
```
    manage.py dumpdata > db.json
```

### for specific app
Following command will dump the content in django admin app into admin.json file
```
    manage.py dumpdata admin > admin.json
```

### for specific table
Following command will dump only the content in django auth.user table
```
    manage.py dumpdata auth.user > user.json
```

### dumpdata (--exclude)
You can use --exclude option to specify apps/tables which don't need being dumped
```
    manage.py dumpdata --exclude auth.permission > db.json
```

###dumpdata (--indent)
By default, dumpdata will output all data on a single line. It isn’t easy for humans to readYou can use the --indent option to pretty-print the output with a number of indentation spaces
```
    manage.py dumpdata auth.user --indent 2 > user.json
```

## loaddata
This command can be use to load the fixtures(database dumps) into database
```
    manage.py loaddata user.json
```

## Restore fresh database
<ul>
    <li>When you backup whole database by using dumpdata command, it will backup all the database tables</li>
    <li>If you use this database dump to load the fresh database(in another django project), it can be causes IntegrityError (If you loaddata in same database it works fine)</li>
    <li>To fix this problem, make sure to backup the database by excluding contenttypes and auth.permissions tables</li>

</ul>

```
    manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
```

```
    manage.py loaddata db.json
```







