from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import euclidean_distances
import re
import numpy as np

model = SentenceTransformer('/Users/spatialite-project/Documents/spatialite/project/Whudatabase/documents/utils/all-MiniLM-L6-v2')

subtitle1_path = '/Users/spatialite-project/Documents/spatialite/project/Whudatabase/documents/utils/video_process/subtitle1.txt'

with open(subtitle1_path, 'r', encoding='utf-8') as f:
    subtitles1 = f.read().replace('\n', '')

sentences1 = re.split(r'(?<=[.!?])', subtitles1)
vectors1 = model.encode(sentences1)

query = 'Apple\'s made this promise'
query_vector = model.encode(query)

# 计算欧几里得距离
distances = euclidean_distances([query_vector], vectors1)[0]
# 找到最相似的字幕索引
min_index = np.argmin(distances)

# 输出最相似的字幕及其向量和距离
most_similar_sentence = sentences1[min_index]
most_similar_vector = vectors1[min_index]
most_similar_distance = distances[min_index]

print("最相似的字幕：", most_similar_sentence)
print("最小距离：", most_similar_distance)