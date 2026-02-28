# MVP 上线前检查清单

## 概述
日期: 2026-02-28
状态: 待实现
实现优先级: 高

## 一、环境配置问题

### 1.1 后端 CORS 硬编码
**问题**: `backend/app/main.py` 中 CORS 配置硬编码了 `localhost`
```python
allow_origins=["http://localhost:5173", "http://localhost:3000"]
```

**修复方案**: 改为环境变量
```python
# .env
FRONTEND_URL=https://your-frontend.com

# main.py
allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")]
```

**影响**: 生产环境前后端无法通信

### 1.2 前端 API Base URL 硬编码
**问题**: `frontend/src/lib/api.ts` 中硬编码
```python
const API_BASE_URL = "http://localhost:8000"
```
**修复方案**: 使用环境变量
```javascript
// .env (Vite 会自动加载 .env.local)
VITE_API_URL=https://your-backend.com

// api.ts
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"
```
**影响**: 生产环境前端无法调用后端 API

## 二、功能实现

### 2.1 时间显示修复
**问题**: 29% 的文章 `published_at` 为 null， 显示 "未知时间"
**修复方案**: 前端 fallback 到 `created_at`
```javascript
// ArticleCard.tsx
const formatDate = (dateStr: string | null, fallbackDate?: string) => {
  if (!dateStr && !fallbackDate) return '未知时间'
  // ... 使用 fallbackDate 作为后备
}

```
**影响**: 用户体验差，**工作量**: 小 (仅前端修改)

### 2.2 反馈链接
**需求**: 添加 GitHub Issues 链接
**实现**: 在 Layout 夌 App览按钮或```javascript
// Layout.tsx header
<a href="https://github.com/your-repo/issues/new" target="_blank">
  反馈建议</a>
```
**工作量**: 小 (仅前端修改)
### 2.3 RSS 源推荐功能
**需求**: 用户可推荐 RSS 源
**实现**:
1. 数据库: 新建 `suggested_feeds` 表
2. 后端: POST /api/suggestions API
3. 前端: Sidebar 底部 "推荐 RSS 源" 按钮 + 表单弹窗
4. 管理: Python 脚本查看推荐列表
**工作量**: 中 (新增 Model、 API、 前端组件、 脚本)

## 三、部署准备

### 3.1 Railway 配置
**已存在**: `railway.json`, `railway.toml`, `nixpack` 文件
**需确认**:
- [ ] 騡块版本是否- [ ] 启动命令
- [ ] 健康检查路径
### 3.2 安全检查
- [x] `.env` 在 `.gitignore` ✅
- [x] 敏感信息不应提交
- [ ] 依赖漏洞扫描
### 3.3 数据库
- [ ] 备份策略 (Railway 卷备份需额外配置)
- [ ] 迁移到 PostgreSQL (可选)

## 四、实现顺序

1. 修复 CORS 和 API URL 配置
2. 实现时间显示修复
3. 添加反馈链接
4. 实现 RSS 推荐功能
5. 全面测试
6. 部署上线
