# Keyword 项目

本项目使用 **Python** 语言开发，数据库采用 **MySQL**。

## 功能简介

- **添加 keyword**
  - 支持单个添加与批量添加

- **修改 keyword**
  - 先查询目标 keyword，再进行修改
  - 支持通过模糊搜索 keyword 名称，修改其他属性

- **查询 keyword**
  - 按网站名称查询
  - 按喜爱程度查询
  - 按备注模糊查询
  - 支持模糊查询

## 数据结构

### keyword 表（主表）

| 字段 | 类型 | 说明 | 是否必须
|------|------|------|------
| ID | INT | 主键 | 是
| keyword_name | VARCHAR(50) | 关键词主体 | 是
| remark | VARCHAR(400) | 备注信息 | 否
| site_id | VARCHAR(50) | 外键关联 | 是
| rating | TINYINT | 1-5 级别 | 否
| image_path | VARCHAR(255) | 图片路径 | 否
| create_at | TIMESTAMP | 默认当天 | 否
| update_at | TIMESTAMP | 默认修改日期 | 否

### 网站表

| 字段 | 类型 | 说明 | 是否必须
|------|------|------|------
| ID | INT | 主键 | 是
| site_name | VARCHAR(50) | 网站名称 | 是
| url | VARCHAR(100) | 网站 URL | 是
| quick_search | ENUM | 是/否/无 | 否

### 图片文件夹

- 文件命名规则：使用 keyword 表的 ID 作为文件名
