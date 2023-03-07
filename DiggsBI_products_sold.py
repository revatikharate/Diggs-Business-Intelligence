#!/usr/bin/env python
# coding: utf-8

# In[190]:


import pandas as pd
from pandas import json_normalize
import json
import matplotlib.pyplot as plt
import requests
from requests.auth import HTTPBasicAuth


# In[191]:


#code to call the api and take respnse one page at a time
page=1
dict={}#storing the final data as a dictioanry where key is the code and value is its quantity sold
while(1):
    response = requests.get('https://api.cin7.com/api/v1/SalesOrders?rows=250&where=createdDate<2023-02-01T00:00:00Z and createdDate>2022-12-31T23:59:59Z&fields=lineItems&page='+str(page),auth = HTTPBasicAuth('DiggsIncUS', '9901f725991a42c4b8ea12917e3c21d9'))
    if not response.json():#to end the code once all pages containing data is covered
        break
    page_data=response.json()
    while len(page_data)>0:
        one_sales_record=(page_data.pop(0)).get('lineItems')#getting listitems for each sales record
        for i in range(0,len(one_sales_record)):#going through list of products in each sales record one by one
            quant=int(one_sales_record[i]['qty'])#accessing the quantity ordered and converting it to int type
            key=one_sales_record[i]['code']#accessing the code of the product
            if key in dict.keys():
                dict[key]+= quant #if code is presenting updating it's value
            else:
                dict[key]= quant #if not then creating a key,value by code,quantity
    page+=1
#print(dict)


# In[192]:


#saving the dictioanry to a dataframe
df=pd.DataFrame.from_dict(dict, orient='index').reset_index()
df=df.rename(columns={'index':'code', 0:'Qty'})
print(df)


# In[193]:


#accessing the skumapping excel
compare_df=pd.read_excel('/Users/nidhimenon/Downloads/DiggsSKUMapping.xlsx')
compare_df=compare_df.filter(['Diggs SKU', 'Product Variant'])
compare_df=compare_df.rename(columns={'Diggs SKU':'code'})
compare_df


# In[194]:


#matching the data from sales to the skumapping excel sheet to get product variants and their quantity sold
final_df=pd.merge(df, compare_df, on='code', how='left')
#final_df.to_excel("/Users/nidhimenon/Desktop/output3.xlsx")
agg_functions = {'code': 'first', 'Qty': 'sum'}
final_df=final_df.groupby(final_df['Product Variant']).aggregate(agg_functions)
final_df


# In[195]:


#saving it to excel sheet
final_df.to_excel("/Users/nidhimenon/Desktop/output.xlsx")


# In[196]:


#displaying top 5 most sold products
data=final_df.sort_values('Qty', ascending=False).head(5)
data


# In[197]:


data.plot.bar()	


# In[ ]:




