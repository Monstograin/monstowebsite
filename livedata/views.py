from django.shortcuts import render
from cloudant.client import Cloudant
client = Cloudant("8d68dbf2-0c78-4ff7-b30c-e0319888856f-bluemix", "3ba2666bcc1bc78211bb5dabe3310efb0599c54876d7199e0d2e181c8b8b03f0", url='https://8d68dbf2-0c78-4ff7-b30c-e0319888856f-bluemix:3ba2666bcc1bc78211bb5dabe3310efb0599c54876d7199e0d2e181c8b8b03f0@8d68dbf2-0c78-4ff7-b30c-e0319888856f-bluemix.cloudantnosqldb.appdomain.cloud',connect=True,auto_renew=True)
rspdata=client['rspdata']
my_document = rspdata["rspdata"]

def index(request):
	rspdata=client['rspdata']
	my_document = rspdata["rspdata"]
	temp=my_document["temperature"][0]
	humi=my_document["humidity"][0]
	co2=my_document["co2"][0]
	a=my_document["temperature"]
	b=my_document["humidity"]
	c=my_document["co2"]
	return render(request,'livedata/livedata.html',{"temp":temp,"humi":humi,"co2":co2,"graphtemp":a,"graphhumi":b,"graphco2":c})




# Create your views here.
