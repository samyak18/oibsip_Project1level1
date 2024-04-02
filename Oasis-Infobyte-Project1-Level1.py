#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_excel(r"C:\Users\kumar\Downloads\exploratory-data-analysis-on-retail-data\exploratory-data-analysis-on-retail-data\Online Retail.xlsx")
df.head()


# In[3]:


df.shape


# In[4]:


df.tail()


# In[5]:


df.info()


# In[6]:


df[df['InvoiceNo'].str.contains('C', na=False)]


# In[7]:


print("Number of missing values per column:")
print(df.isnull().sum())

print("---------------------------------------------------------------------------------------------")

print("Number of unique values per row:")
print(df.nunique())


# In[8]:


df['CustomerID'].fillna("Unknown", inplace=True)
df = df[df['Description'].notna()]
columns_to_drop = ["InvoiceNo", "StockCode"]
df.drop(columns=columns_to_drop, inplace=True)
df.head(10)


# In[9]:


df = df.drop_duplicates()
df.info()


# In[10]:


df = df.assign(Gross=df['Quantity'] * df['UnitPrice'])
df


# In[11]:


df.describe()


# In[12]:


median = df.median(numeric_only=True)
median


# In[13]:


df['MonthYear'] = df['InvoiceDate'].dt.to_period('M').copy()
df


# In[14]:


import matplotlib.pyplot as plt
import numpy as np
monthly_data = df.groupby('MonthYear')['Gross'].sum().reset_index()
monthly_data['MonthYear'] = monthly_data['MonthYear'].astype(str)
fig, ax = plt.subplots(figsize=(10, 5))
fig.autofmt_xdate()
plt.plot(monthly_data['MonthYear'], monthly_data['Gross'], marker='o', linestyle='-', color='Purple', label='Gross')
plt.title('Gross by Month', fontsize=16)
plt.xlabel('MonthYear', fontsize=12)
plt.ylabel('Gross', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='upper left', fontsize=12)
ax.set_facecolor('grey')
plt.show()  


# In[15]:


df['Month'] = df['InvoiceDate'].dt.month.values
df['DayOfWeek'] = df['InvoiceDate'].dt.day_name().values
monthly_sales = df.groupby('Month')['Gross'].sum()
daily_sales = df.groupby('DayOfWeek')['Gross'].sum()
busiest_month = monthly_sales.idxmax()
busiest_day = daily_sales.idxmax()
print("Busiest Month (in terms of sales):", busiest_month)
print("Busiest Day of the Week (in terms of sales):", busiest_day)


# In[16]:


import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
colors = ['blue', 'green', 'red', 'yellow', 'orange', 'black', 'magenta']
plt.bar(daily_sales.index, daily_sales.values, color=colors)
plt.xlabel('Day of the Week', fontsize=12)
plt.ylabel('Gross Amount', fontsize=12)
plt.title('Sales Trend of Weekdays', fontsize=16)
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.xticks(range(len(days_of_week)), days_of_week, rotation=45, fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# In[17]:


customer_total_purchase = df.groupby('CustomerID')['Gross'].sum()
most_valuable_customers = customer_total_purchase.sort_values(ascending=False)
most_valuable_customers_df = pd.DataFrame(most_valuable_customers, columns=['Gross']).reset_index()
total_customers = df['CustomerID'].nunique()
print('\033[1m' + f"Among {total_customers} customers, the top 10 customers are:" +'\033[0m', list(most_valuable_customers_df['CustomerID'][:10]))


# In[18]:


items_total_sell = df.groupby('Description')['Gross'].sum()
most_valuable_items = items_total_sell.sort_values(ascending=False)
most_valuable_items_df = pd.DataFrame(most_valuable_items, columns=['Gross']).reset_index()
total_items = df['Description'].nunique()
print('\033[1m' + f"Among {total_items} items, the 10 most valuable items are:" +'\033[0m', list(most_valuable_items_df['Description'][:10]))


# In[19]:


countrywise_sell = df.groupby('Country')['Gross'].sum()
top_selling_country = countrywise_sell.sort_values(ascending=False)
top_selling_country_df = pd.DataFrame(top_selling_country, columns=['Gross']).reset_index()
total_countries = df['Country'].nunique()
print('\033[1m' + f"Among {total_countries} countries, the top 10 selling countries are:" +'\033[0m', list(top_selling_country_df['Country'][:10]))


# In[20]:


import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, y='Gross', color='lightblue', showfliers=False)  
plt.title('Distribution of Gross Amount', fontsize=16)
plt.xlabel('Gross', fontsize=12)
plt.show()


# In[21]:


from scipy import stats
z_scores = stats.zscore(df['Gross'])
threshold = 3
outlier_mask = abs(z_scores) > threshold
outliers = df[outlier_mask]
outliers.shape


# In[22]:


without_outliers_online_retail = df[~outlier_mask]
summary_without_outliers = without_outliers_online_retail.describe()
summary_without_outliers


# In[23]:


df.describe()


# In[24]:


import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 6))
colors = sns.color_palette("Blues")  
sns.boxplot(data=without_outliers_online_retail, y='Gross', palette=colors, width=0.5, linewidth=2)
plt.title('Distribution of Gross Amount (Without Outliers)', fontsize=16)
plt.xlabel('Gross', fontsize=12)
plt.ylabel('Gross Amount', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# In[ ]:




