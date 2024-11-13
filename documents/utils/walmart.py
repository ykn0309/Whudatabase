import pandas as pd

df = pd.read_csv("WMT_Grocery_202209.csv", low_memory=False)

column_to_drop = ['SHIPPING_LOCATION', 'DEPARTMENT', 'SUBCATEGORY', 'BREADCRUMBS', 'SKU', 'PRODUCT_URL', 'PRICE_RETAIL', 'PRODUCT_SIZE', 'PROMOTION', 'RunDate', 'tid']

df = df.drop(columns=column_to_drop)

df.columns = ['index', 'category', 'product_name', 'brand', 'price']

df = df.drop_duplicates(subset=['product_name'])

df = df.iloc[:30000]

df.to_csv("product_dataset.csv", index=False)