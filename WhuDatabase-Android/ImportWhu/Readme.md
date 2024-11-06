@[TOC](WhuDatabase)

# 这是什么

移植到 Android 的 WhuDatabase 数据库
100% 离线、可移植且独立于 SQLite。

# 什么时候需要它？
当您需要在 Android 设备上部署、收集、处理和快速查询少量到大量几何数据（点、折线、多边形、多多边形等）时。
当您希望 100% 独立于任何服务器/云后端时。

# 入门
工作原理与SQLite基本相同，使用SQL语句进行建表，插入数据，以及查询。
## 示例
### 创建表和插入数据
```java
// 创建表格
CREATE TABLE places (
    id INTEGER PRIMARY KEY,
    name TEXT,
    geom GEOMETRY
);

// 插入点数据
INSERT INTO places (name, geom) VALUES ('Place A', GeomFromText('POINT(1 1)', 4326));
INSERT INTO places (name, geom) VALUES ('Place B', GeomFromText('POINT(2 2)', 4326));

// 插入线数据
INSERT INTO places (name, geom) VALUES ('Line A', GeomFromText('LINESTRING(0 0, 2 2)', 4326));
INSERT INTO places (name, geom) VALUES ('Line B', GeomFromText('LINESTRING(0 2, 2 0)', 4326));

// 插入多边形数据
INSERT INTO places (name, geom) VALUES ('Polygon A', GeomFromText('POLYGON((0 0, 0 3, 3 3, 3 0, 0 0))', 4326));
```
### 基本查询

查询所有数据并显示几何对象的文本表示
```java
SELECT id, name, AsText(geom) FROM places;
```
### 空间查询

查询包含特定点的几何对象
```java
SELECT name FROM places WHERE Contains(geom, GeomFromText('POINT(1 1)', 4326));
```
查询相交的几何对象

```java
// 两条线相交
SELECT Intersects(
    (SELECT geom FROM places WHERE name = 'Line A'),
    (SELECT geom FROM places WHERE name = 'Line B')
) AS do_intersect;

// 与一条线相交的所有图形名字
SELECT name FROM places WHERE Intersects(geom, GeomFromText('LINESTRING(0 0, 2 2)', 4326));
```

查询距离

```java
// 两点之间的距离
SELECT Distance(
    (SELECT geom FROM places WHERE name = 'Place A'),
    (SELECT geom FROM places WHERE name = 'Place B')
) AS distance;

// 距离特定点一定范围内的几何对象
SELECT name FROM places WHERE Distance(geom, GeomFromText('POINT(1 1)', 4326)) < 2.0;
```
### 几何操作
计算几何对象的缓冲区

```java
SELECT id, name, AsText(Buffer(geom, 1.0)) AS buffered_geom FROM places;
```
计算几何对象的凸包

```java
SELECT id, name, AsText(ConvexHull(geom)) AS convex_hull_geom FROM places;
```
计算两个几何对象的交集

```java
SELECT AsText(Intersection(
    (SELECT geom FROM places WHERE name = 'Line A'),
    (SELECT geom FROM places WHERE name = 'Line B')
)) AS geom_intersection;
```

# 其他常见问题
## 什么是 WhuDatabase？
简单来说：WhuDatabase= SQLite + 高级地理空间支持。
WhuDatabase是 SQLite 的地理空间扩展。它是一组用 C 编写的库，用于扩展 SQLite 的几何数据类型和许多基于几何数据的 SQL 函数。
## 它使用 JDBC 吗？
否，它使用cursors - 建议使用轻量级方法来访问 Android 平台中使用的 SQL，而不是更重的 JDBC。
## 它支持64位架构吗？
是的，它为 arm64-v8a 和 x86_64 构建。
## 当前打包了哪些库？
 - SQLite 3.15.1
 - Whu 2.0.1
 - GEOS 3.4.2
 - Proj4 4.8.0
 - lzma 5.2.1
 - iconv 1.13
 - xml2 2.9.2
 - freexl 1.0.2

# 要求
最低SDK16
