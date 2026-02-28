# Feed Taxonomy Workflow

This project uses source-level taxonomy:

- `category` (domain): `AI, 安全, 系统, 前端, 后端, 数据, 产品, 商业, 设计, 科学`
- `source_type`: `个人博客, 公司技术博客, 媒体, 研究机构, 社区组织`

## 1) Export Manual Template

```bash
cd backend
python scripts/export_feed_taxonomy_template.py
```

Generated file:

- `backend/data/feed_taxonomy.csv`

## 2) Manually Fill Taxonomy

Edit `backend/data/feed_taxonomy.csv`:

- Keep `feed_url` unchanged.
- `current_category` is only a legacy reference column.
- Set `category` to one allowed domain value.
- Set `source_type` to one allowed source type value.

## 3) Import Into Database

```bash
cd backend
python scripts/import_feed_taxonomy.py
```

The importer validates values and updates matching feeds.
