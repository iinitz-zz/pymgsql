from pymgsql import *

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

db=MongoSQL('mysql://DB_USERNAME:DB_PASSWORD@HOSTNAME/DB_NAME?charset=utf8')
DB=(Model1,Model2)
for table in DB[::-1]: table.dropTable(ifExists=True)
for table in DB: table.createTable(ifNotExists=True)
Model1(name='a',lastname='i')
Model1(name='b',lastname='j')
Model1(name='c',lastname='k')
Model2(model1=1,type1='x',type2='x',type3=1)
Model2(model1=2,type1='y',type2='y',type3=2)
Model2(model1=3,type1='z',type2='y',type3=3)
Model2(model1=2,type1='x',type2='x',type3=4)
Model2(model1=3,type1='z',type2='x',type3=5)
db.regis(DB)
#a=db.model2.find({'model1.name':'b','model1.lastname':'j','type2':'y'},orderBy=['-id'])
#a=db.model2.find({'type2':'x','type3':{'$gte':3},'$or':{'model1.name':{'$in':['a','c']},'model1.lastname':'j'}})
#a=db.model2.find({'$or':{'type3':{'$like':'xy%'},'type1':'y'}})
a=db.model1.find({'name':{'$in':['a','b']}}) # find
b=db.model1.findOne(1) # findOne
c=db.model1.insert({'name':'d','lastname':'l'}) # insert
d=db.model1.update(1,{'name':'e','lastname':'m'}) # update
e=db.model2.remove(1) # remove
print a
print b
print c
print d
print e
