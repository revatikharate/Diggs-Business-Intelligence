#!/usr/bin/env python
# coding: utf-8

# In[122]:


import pandas as pd
from pandas import json_normalize
import json
import matplotlib.pyplot as plt
import requests
from requests.auth import HTTPBasicAuth


# In[123]:


page=1
dict={}
while(1):
    response = requests.get('https://api.cin7.com/api/v1/SalesOrders?rows=250&where=createdDate<2023-02-01T00:00:00Z and createdDate>2022-12-31T23:59:59Z&fields=lineItems&page='+str(page),auth = HTTPBasicAuth('DiggsIncUS', '9901f725991a42c4b8ea12917e3c21d9'))
    if not response.json():
        break
    page_data=response.json()
    while len(page_data)>0:
        one_sales_record=(page_data.pop(0)).get('lineItems')
        for i in range(0,len(one_sales_record)):
            quant=int(one_sales_record[i]['qty'])
            key=one_sales_record[i]['code']
            if key in dict.keys():
                dict[key]+= quant
            else:
                dict[key]= quant
    page+=1
#print(dict)


# In[146]:


df=pd.DataFrame.from_dict(dict, orient='index').reset_index()
df=df.rename(columns={'index':'code', 0:'Qty'})
print(df)


# In[147]:


compare_df=pd.read_excel('/Users/nidhimenon/Downloads/DiggsSKUMapping.xlsx')
compare_df=compare_df.filter(['Diggs SKU', 'Variant'])
compare_df=compare_df.rename(columns={'Diggs SKU':'code'})
#compare_df


# In[148]:


final_df=pd.merge(df, compare_df, on='code', how='left')


# In[149]:


final_df.to_excel("/Users/nidhimenon/Desktop/output.xlsx")


# In[150]:


data=final_df.sort_values('Qty', ascending=False).head(5)
data


# In[151]:


data.plot(x='Variant', y='Qty', kind='bar')	


# In[ ]:




