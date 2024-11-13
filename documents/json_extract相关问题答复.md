#### 1. ``json_extract()``是否支持嵌套？

支持。下面是一个例子：

```sql
-- 创建一个存储json数据的表
CREATE TABLE test_json (
    id INTEGER PRIMARY KEY,
    data JSON
);

-- 插入数据
INSERT INTO test_json (data) VALUES 
    ('
        {
            "name": "Alice",
            "age": 30,
            "skills":
                [
                    {
                        "skill_name": "Python",
                        "skill_level": "advanced"
                    },
                    {
                        "skill_name": "Python",
                        "skill_level": "advanced"
                    }
                ]
        }
    ');

-- json_extract()嵌套查询
SELECT json_extract(json_extract(data, '$.skills[0]'), '$.skill_name') FROM test_json;
-- 预期输出Python
```

#### 2. ``json_extract()``是否支持多个层级的路径表示法？

支持。同样是前面的例子

```sql
SELECT json_extract(data, '$.skills[0].skill_name') FROM test_json;
-- 效果和前面的例子一样
```