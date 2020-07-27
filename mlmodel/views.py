from django.shortcuts import render
from django.http import HttpResponse
from pandas import DataFrame
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

def data(request):
	data=pd.read_csv('https://raw.githubusercontent.com/Yuvateja01/csvdata/master/train.csv')
	center=pd.read_csv('https://raw.githubusercontent.com/Yuvateja01/csvdata/master/fulfilment_center_info.csv')
	meal=pd.read_csv('https://raw.githubusercontent.com/Yuvateja01/csvdata/master/meal_info.csv')
	test=pd.read_csv('https://raw.githubusercontent.com/Yuvateja01/csvdata/master/ibmhacktest.csv')
	data=pd.concat([data,test],axis=0)
	data=data.merge(center,on='center_id',how='left')
	data=data.merge(meal,on='meal_id',how='left')
	data['discount amount']=data['base_price']-data['checkout_price']
	data['discount percent'] = ((data['base_price']-data['checkout_price'])/data['base_price'])*100
	data['discount y/n'] = [1 if x>0 else 0 for x in (data['base_price']-data['checkout_price'])]
	data=data.sort_values(['center_id', 'meal_id', 'week']).reset_index()
	data['compare_week_price'] = data['checkout_price'] - data['checkout_price'].shift(1)
	data['compare_week_price'][data['week']==1]=0
	data=data.sort_values(by='index').reset_index().drop(['level_0','index'],axis=1)
	data['compare_week_price y/n'] = [1 if x>0 else 0 for x in data['compare_week_price']]
	city4={590:'CH1', 526:'CH2', 638:'CH3'}
	data['city_enc_4']=data['city_code'].map(city4)
	data['city_enc_4']=data['city_enc_4'].fillna('CH4')
	datax=data.copy()
	datax['center_id']=datax['center_id'].astype('object')
	datax['meal_id']=datax['meal_id'].astype('object')
	datax['region_code']=datax['region_code'].astype('object')
	obj=datax[['center_id','meal_id','region_code','center_type','category','cuisine','city_enc_4']]
	num=datax.drop(['center_id','meal_id','region_code','center_type','category','cuisine','city_enc_4'],axis=1)
	encode1=pd.get_dummies(obj,drop_first = True)
	datax=pd.concat([num,encode1],axis=1)
	sc=StandardScaler()
	cat=datax.drop(['checkout_price','base_price','discount amount','discount percent','compare_week_price'],axis=1)
	num=datax[['checkout_price','base_price','discount amount','discount percent','compare_week_price']]
	scal= pd.DataFrame(sc.fit_transform(num),columns=num.columns)
	datas=pd.concat([scal,cat],axis=1)
	datay=datas.copy()
	datay['Quarter']=(datas['week']/13).astype('int64')
	datay['Quarter'] = datay['Quarter'].map({0:'Q1',
                         1:'Q2',
                         2:'Q3',
                         3:'Q4',
                         4:'Q1',
                         5:'Q2',
                         6:'Q3',
                         7:'Q4',
                         8:'Q1',
                         9:'Q2',
                         10:'Q3',
                         11:'Q4'})
	datay['Quarter'].value_counts()
	datay['Year']=(datas['week']/52).astype('int64')
	datay['Year'] = datay['Year'].map({0:'Y1',
                         1:'Y2',
                         2:'Y3'})
	objy=datay[['Quarter', 'Year']]
	numy=datay.drop(['Quarter', 'Year'],axis=1)

	encode1y=pd.get_dummies(objy,drop_first = True)
	encode1y.head()
	datay=pd.concat([numy,encode1y],axis=1)
	datay['num_orders']=np.log1p(datay['num_orders'])
	train=datay[datay['week'].isin(range(1,136))]
	test=datay[datay['week'].isin(range(136,146))]
	X_train=train.drop(['id','num_orders','week','discount amount','city_code'],axis=1)
	y_train=train['num_orders']
	X_test=test.drop(['id','num_orders','week','discount amount','city_code'],axis=1)
	y_test=test['num_orders']
	reg = LinearRegression()
	reg.fit(X_train,y_train)
	y_pred=reg.predict(X_test)
	test1=test.copy()
	test1["num_orders"]=y_pred
	test1.to_csv('myvds.csv')
	return render(request,'mlmodel/mlmodel.html')


# Create your views here.



