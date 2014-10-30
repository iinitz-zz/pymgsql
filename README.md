A python API for manage your MySQL database (select, insert, update, delete) like pymongo by iinitz


### Require
##### python-mysqldb
```
$ apt-get install python-mysqldb
```
##### SQLObject
```
$ easy_install sqlobject
```


### Install
```
$ git clone https://github.com/iinitz/pymgsql.git
$ cd pymgsql
$ python setup.py install
```


### Import
```python
from pymgsql import *
```


### Defined your SQL schema with Schema (like [SQLObject](http://sqlobject.org/))
```python
class Model1(Schema):
	class sqlmeta:
		table='model1'
	name=UnicodeCol(length=16,dbName='name',notNone=True)
	lastname=UnicodeCol(length=16,dbName='lastname',notNone=True)
	test=MultipleJoin('Model2',joinColumn='model1_id')
class Model2(Schema):
	class sqlmeta:
		table='model2'
	model1=ForeignKey('Model1',dbName='model1_id')
	type1=UnicodeCol(length=16,dbName='type1',notNone=True)
	type2=UnicodeCol(length=16,dbName='type2',notNone=True)
	type3=IntCol(length=16,dbName='type3',notNone=True)
```


### Create your table
```python
DB=(Model1,Model2)
for table in DB[::-1]: table.dropTable(ifExists=True)
for table in DB: table.createTable(ifNotExists=True)
```


### Create DB object
```python
db=MongoSQL('mysql://DB_USERNAME:DB_PASSWORD@HOSTNAME/DB_NAME?charset=utf8')
```


### Register your schema
```python
db.regis(DB)
```


### Select
##### Format
```python
db.tableName.find() # select all
db.tableName.find(param) # select filter
db.tableName.findOne(id) # select by id
```

##### Example
```python
a=db.model1.find({'name':'a'})
print a
b=db.model1.findOne(1)
print b
```

##### Option
```python
db.tableName.find(orderBy=['-id','name'])
db.tableName.find(limit=5,reversed=True)
```

##### Operator
NOT
```python
{'$not':{'columnName':'value'}}
```

OR
```python
{'$or':{'columnName1':'value1','columnName2':'value2'}}
```

AND
```python
{'$and':{'columnName1':'value1','columnName2':'value2'}}
```

IN
```python
{'columnName':{'$in':['value1','value2']}}
```

LIKE
```python
{'columnName':{'$like':'%value%'}}
```

<
```python
{'columnName':{'$lt':'value'}}
```

<=
```python
{'columnName':{'$lte':'value'}}
```

>
```python
{'columnName':{'$gt':'value'}}
```

>=
```python
{'columnName':{'$gte':'value'}}
```

!=
```python
{'columnName':{'$ne':'value'}}
```


### Insert 
##### Format
```python
db.tableName.insert(param)
```

##### Example
```python
c=db.model1.insert({'name':'a','lastname':'x'})
print c
```


### Update
##### Format
```python
db.tableName.update(id,param)
```

##### Example
```python
d=db.model1.update(1,{'name':'d'})
print d
```


### Delete
##### Format
```python
db.tableName.remove(id)
```

##### Example
```python
e=db.model1.remove(1)
print e # return True if delete success else return False
```
