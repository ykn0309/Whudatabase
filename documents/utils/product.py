from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.decomposition import PCA

# 商品名称列表
products = [
    "iPhone 15 Pro",
    "Samsung Galaxy S23",
    "MacBook Air",
    "Sony WH-1000XM5 Headphones",
    "Kindle Paperwhite",
    "Fitbit Charge 5 Fitness Tracker",
    "Dyson Vacuum Cleaner",
    "Instant Pot Multi-Function Electric Pressure Cooker",
    "Brita Water Filter Jug",
    "IKEA Mug",
    "Philips Smart Light Bulb",
    "Tempur-Pedic Memory Foam Pillow",
    "Nike Air Force 1 Sneakers",
    "Levis Classic Jeans",
    "Uniqlo Down Jacket",
    "Patagonia Windbreaker",
    "Adidas Originals Hoodie",
    "Vans Canvas Shoes",
    "Estee Lauder Advanced Night Repair Serum",
    "SK-II Facial Treatment Essence",
    "LOreal Paris Foundation",
    "Colgate Electric Toothbrush",
    "Neutrogena Sunscreen",
    "Olay Water Infused Whitening Cream",
    "Starbucks Coffee Beans",
    "Gillette Razor",
    "Dove Soap",
    "Head & Shoulders Shampoo",
    "Kleenex Tissues",
    "Tide Laundry Detergent",
    "Coca-Cola",
    "Lays Potato Chips",
    "Ferrero Rocher Chocolate",
    "Haagen-Dazs Ice Cream",
    "Lipton Black Tea",
    "Blue Diamond Almonds"
]

# 加载 Sentence-BERT 模型
model = SentenceTransformer('/Users/spatialite-project/Documents/spatialite/project/Whudatabase/documents/utils/all-MiniLM-L6-v2')

# 生成商品的向量表示
product_embeddings = model.encode(products)

pca = PCA(n_components=10)
product_embeddings = pca.fit_transform(product_embeddings)

with open('insert_products.sql', 'w') as f:
    for i in range (len(products)):
        product = products[i]
        vector = product_embeddings[i].tolist()
        sql = f"INSERT INTO products (product_name, product_vector) VALUES ('{product}', vec_f32('{vector}'));\n"
        f.write(sql)

# 打印所有商品向量的形状
print("商品向量的形状：", product_embeddings.shape)

# 计算并展示任意两个商品的相似度
similarity_matrix = cosine_similarity(product_embeddings)
print("相似度矩阵（部分）：")
print(similarity_matrix[:5, :5])  # 显示前5个商品的相似度

# 示例：找到与 "xxx" 最相似的商品
target_product = "Coca-Cola"
target_index = products.index(target_product)
similarities = similarity_matrix[target_index]

# 排序并输出最相似的商品（排除自身）
most_similar_indices = np.argsort(-similarities)[1:6]  # 排序后取前5个相似商品
print(f"\n与 '{target_product}' 最相似的商品：")
for idx in most_similar_indices:
    print(f"{products[idx]}，相似度：{similarities[idx]:.2f}")