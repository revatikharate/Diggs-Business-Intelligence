#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
from pandas import json_normalize
import json
# import requests module
import requests
from requests.auth import HTTPBasicAuth


# In[23]:


#initializing page variable
page=1
sales_data=[]
while(1):
    # api get request fot=r sales in the month of January
    response = requests.get('https://api.cin7.com/api/v1/SalesOrders?rows=250&where= createdDate<2023-02-01T00:00:00Z and createdDate>2022-12-31T23:59:59Z&fields=id,createdDate,projectName,total&page='+str(page),auth = HTTPBasicAuth('DiggsIncUS', '9901f725991a42c4b8ea12917e3c21d9'))
    #looping the api call till there isn't an empty object is returned
    if not response.json():
        break
    #print (response.json())
    page_data=response.json()
    #separarting each object from the the output array and then appending it sales_Data to have an array of salesrecord objects
    while len(page_data)>0:
        sales_data.append(page_data.pop(0))
    #end of a single page
    #print("-------------------------------------------------") 
    #increasing the page value to iterate through all pages and get the data
    page+=1 
#print(sales_data)                    


# In[27]:


#converting json data to a dataframe
df_sales = json_normalize(sales_data)
#print(df_sales)
#calculating no of sales records for each retailer type
df_retailersales_count=df.projectName.value_counts()
print(df_retailersales_count)
print("-------------------------------------------------") 
#calculating total amount of sales for each retailer type
df_retailersales_totalsum=df_sales.groupby('projectName')['total'].sum()
print(df_retailersales_totalsum)


# In[ ]:




