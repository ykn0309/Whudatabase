from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd

df = pd.read_csv('/Users/spatialite-project/Documents/spatialite/project/Whudatabase/documents/utils/product_dataset.csv', low_memory=False)

products = df['product_name'].tolist()
categories = df['category'].tolist()

# 加载 Sentence-BERT 模型
model = SentenceTransformer('/Users/spatialite-project/Documents/spatialite/project/Whudatabase/documents/utils/all-MiniLM-L6-v2')

# 生成商品的向量表示
product_embeddings = model.encode(products)

pca = PCA(n_components=10)
product_embeddings = pca.fit_transform(product_embeddings)

with open('walmart.sql', 'w') as f:
    for i in range (len(products)):
        product = products[i]
        category = categories[i]
        vector = product_embeddings[i].tolist()
        sql = f"INSERT INTO products (product_name, category, product_vector) VALUES ('{product}', '{category}', vec_f32('{vector}'));\n"
        f.write(sql)