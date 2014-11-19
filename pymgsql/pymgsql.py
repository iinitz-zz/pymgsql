# -*- coding: utf-8 -*-
from datetime import date,time,datetime
from sqlobject import *
from sqlobject.sqlbuilder import *
from sqlobject.classregistry import findClass

class MongoStyle(Style):
	def instanceAttrToIDAttr(self,attr):
		return attr+'_id'
	def instanceIDAttrToAttr(self,attr):
		return attr[:-3]
class Schema(SQLObject):
	class sqlmeta:
		style=MongoStyle()

class Resource:
	model=None
	name=None
	joins=None
	excCols=None
	def __init__(self,model,name=None,excCols=None):
		self.model=model
		self.tableName=self.model.sqlmeta.table
		self.name=name or self.tableName
		self.joins={}
		for k,v in self.model.sqlmeta.columns.items():
			if type(v)==col.SOForeignKey:
				model=findClass(v.foreignKey,self.model.sqlmeta.registry)
				self.joins[model.sqlmeta.table]={'column':k,'model':model}
				self.joins[model.sqlmeta.table]['joinOn']=self.createExpr('{0}.{1}'.format(model.sqlmeta.table,'id'))==self.createExpr(k)
		if excCols:
			self.excCols=excCols
	def toDict(self,obj,l=[]):
		if isinstance(obj,(list,sresults.SelectResults)):
			return [self.toDict(x) for x in list(obj)]
		else:
			tmp={}
			l=l+[obj.sqlmeta.table]
			for k,v in vars(type(obj)).items():
				if isinstance(v,property):
					value=getattr(obj,k)
					bases=type(value).__bases__
					if isinstance(value,list) and len(value)>0 and not value[0].sqlmeta.table in l:
						tmp[k]=[self.toDict(x,l) for x in value]
					elif Schema in bases and value.sqlmeta.table in l:
						continue
					elif datetime in bases:
						tmp[k]=str(value)
					else:
						tmp[k]=value
			tmp['id']=obj.id
			return tmp
	def createExpr(self,column):
		if '.' in column:
			table,column=column.split('.')
			return getattr(self.joins[table]['model'].q,column)
		else:
			return getattr(self.model.q,column)
	def createClause(self,param,op=None):
		tmp,join=[],{}
		for key,value in param.items():
			if key=='$not':
				tmp.append(self.createClause(value,'NOT'))
			elif key=='$or':
				tmp.append(self.createClause(value,'OR'))
			elif key=='$and':
				tmp.append(self.createClause(value,'AND'))
			else:
				if isinstance(value,dict):
					tmp2=[]
					for k,v in value.items():
						if k=='$in':
							tmp.append(IN(self.createExpr(key),v))
						elif k=='$like':
							tmp2.append(LIKE(self.createExpr(key),v))
						elif k=='$lt':
							tmp2.append(self.createExpr(key)<v)
						elif k=='$lte':
							tmp2.append(self.createExpr(key)<=v)
						elif k=='$gt':
							tmp2.append(self.createExpr(key)>v)
						elif k=='$gte':
							tmp2.append(self.createExpr(key)>=v)
						elif k=='$ne':
							tmp2.append(self.createExpr(key)!=v)
					tmp.extend(tmp2)
				else:
					tmp.append(self.createExpr(key)==value)
				if '.' in key:
					join[key.split('.')[0]]=self.joins[key.split('.')[0]]['joinOn']
		if op=='NOT':
			tmp=NOT(*tuple(tmp))
		elif op=='OR':
			tmp=OR(*tuple(tmp))
		else:
			tmp=AND(*tuple(tmp))
		return AND(tmp,*tuple(join.values()))
	def findObj(self,param=None,orderBy=None,limit=None,distinct=False,reversed=False):
		return self.model.select(self.createClause(param),orderBy=orderBy,limit=limit,distinct=distinct,reversed=reversed)
	def findOneObj(self,id):
		return self.model.get(id)
	def insertObj(self,data):
		return self.model(**data)
	def updateObj(self,id,data):
		self.findOneObj(id).set(**data)
		return self.findOneObj(id)
	def removeObj(self,id):
		self.model.get(id).destroySelf()
	def find(self,param=None,orderBy=None,limit=None,distinct=False,reversed=False):
		try:
			return self.toDict(self.findObj(param=param,orderBy=orderBy,limit=limit,distinct=distinct,reversed=reversed))
		except:
			return None
	def findOne(self,id):
		try:
			return self.toDict(self.findOneObj(id))
		except:
			return None
	def insert(self,data):
		try:
			return self.toDict(self.insertObj(data))
		except:
			return None
	def update(self,id,data):
		try:
			return self.toDict(self.updateObj(id,data))
		except:
			return None
	def remove(self,id):
		try:
			self.removeObj(id)
			return True
		except:
			return False
class MongoSQL:
	def __init__(self,uri,*args,**kwargs):
		self.connection=connectionForURI(uri)
		sqlhub.processConnection=self.connection
		self.models={}
	def regis(self,resource):
		if isinstance(resource,(list,tuple)):
			for rsc in resource:
				self.regis(rsc)
		else:
			if type(resource)==declarative.DeclarativeMeta:
				resource=Resource(resource)
			setattr(self,resource.name,resource)
			self.models[resource.name]=resource
