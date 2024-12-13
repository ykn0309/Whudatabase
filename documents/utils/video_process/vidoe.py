from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import os
import srt

model = SentenceTransformer('/Users/spatialite-project/Documents/spatialite/project/Whudatabase/documents/utils/all-MiniLM-L6-v2')

# 自动检测字幕文件所在目录
subtitle_dir = '/Users/spatialite-project/Documents/spatialite/project/Whudatabase/documents/utils/video_process/subtitles/'
subtitle_paths = [
    os.path.join(subtitle_dir, file) for file in os.listdir(subtitle_dir) if file.endswith('.srt')
]

all_entries = []  # 存储所有字幕信息

for path in subtitle_paths:
    with open(path, 'r', encoding='utf-8') as f:
        subtitles = list(srt.parse(f.read()))  # 解析 SRT 文件
        for subtitle in subtitles:
            start_time = subtitle.start.total_seconds()  # 开始时间（秒）
            end_time = subtitle.end.total_seconds()  # 结束时间（秒）
            content = subtitle.content.strip()  # 字幕内容
            subtitle_id = subtitle.index  # 字幕 ID
            vector = model.encode(content)  # 计算字幕向量

            all_entries.append({
                'video_name': os.path.basename(path),
                'subtitle_id': subtitle_id,
                'start_time': start_time,
                'end_time': end_time,
                'content': content,
                'vector': vector
            })

# 生成 SQL 插入语句
sql_statements = []
for entry in all_entries:
    vector_str = ','.join(map(str, entry['vector']))  # 将向量转化为字符串
    sql = f"""
    INSERT INTO subtitles (video_name, subtitle_id, start_time, end_time, content, vector)
    VALUES (
        '{entry['video_name'].replace(".srt", "")}',
        {entry['subtitle_id']},
        {entry['start_time']},
        {entry['end_time']},
        '{entry['content'].replace("'", "''")}',
        vec_f32('[{vector_str}]')
    );
    """
    sql_statements.append(sql)

# 保存 SQL 语句到文件
output_sql_path = os.path.join(subtitle_dir, 'insert_subtitles.sql')
with open(output_sql_path, 'w', encoding='utf-8') as sql_file:
    sql_file.write('\n'.join(sql_statements))

print(f"SQL 插入语句已保存到 {output_sql_path}")