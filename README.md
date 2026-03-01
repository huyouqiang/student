# 学生管理系统

基于 FastAPI 的学校信息管理 Web 应用，提供学生、教师、学校、成绩等模块的增删改查，支持管理员登录与会话鉴权，前后端采用 Bootstrap 5 + Jinja2 模板。

## 功能特性

- **多模块管理**：学生列表、教师列表、学校列表、学生成绩
- **权限控制**：管理员可增删改查，访客仅可查看
- **学生与成绩关联**：学生列表点击姓名查看成绩，成绩录入时选择学生并自动关联 `student_id`
- **RESTful API**：统一 `/api` 前缀，支持 Swagger 文档

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 模板引擎 | Jinja2 |
| 前端 UI | Bootstrap 5、Bootstrap Icons |
| 数据校验 | Pydantic |
| 会话 | Starlette SessionMiddleware |
| 存储 | MySQL |

## 项目结构

```
student/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口、页面路由
│   ├── auth.py              # 会话、管理员鉴权
│   ├── models/              # 内存存储
│   │   ├── student.py
│   │   ├── teacher.py
│   │   ├── school.py
│   │   └── grade.py
│   ├── schemas/             # Pydantic 模型
│   │   ├── student.py
│   │   ├── teacher.py
│   │   ├── school.py
│   │   └── grade.py
│   └── routers/             # API 路由
│       ├── auth.py          # 登录/登出
│       ├── students.py
│       ├── teachers.py
│       ├── schools.py
│       └── grades.py
├── templates/
│   ├── base.html            # 布局、导航
│   ├── auth/
│   │   └── login.html
│   ├── students/
│   │   └── index.html       # 学生列表、点击姓名查看成绩
│   ├── teachers/
│   │   └── index.html
│   ├── schools/
│   │   └── index.html
│   └── grades/
│       └── index.html       # 成绩列表、选择学生弹框
├── requirements.txt
└── README.md
```

## 安装与运行

### 1. 创建虚拟环境

```bash
cd /opt/homebrew/var/www/student
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问地址

| 页面 | 地址 |
|------|------|
| 学生列表 | http://localhost:8000/ |
| 教师列表 | http://localhost:8000/teachers |
| 学校列表 | http://localhost:8000/schools |
| 学生成绩 | http://localhost:8000/grades |
| 管理员登录 | http://localhost:8000/login |
| Swagger API 文档 | http://localhost:8000/docs |
| API 说明 | http://localhost:8000/api-info |

## 权限说明

| 用户类型 | 查看 | 新增 | 编辑 | 删除 |
|----------|------|------|------|------|
| 访客 | ✅ | ❌ | ❌ | ❌ |
| 管理员 | ✅ | ✅ | ✅ | ✅ |

- 默认管理员：`admin` / `admin123`
- 生产环境请设置环境变量 `SESSION_SECRET`

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/students | 学生列表 |
| GET | /api/students/{id} | 单个学生 |
| POST | /api/students | 新增学生（管理员） |
| PUT | /api/students/{id} | 更新学生（管理员） |
| DELETE | /api/students/{id} | 删除学生（管理员） |
| GET | /api/teachers | 教师列表 |
| GET | /api/teachers/{id} | 单个教师 |
| POST | /api/teachers | 新增教师（管理员） |
| PUT | /api/teachers/{id} | 更新教师（管理员） |
| DELETE | /api/teachers/{id} | 删除教师（管理员） |
| GET | /api/schools | 学校列表 |
| GET | /api/schools/{id} | 单个学校 |
| POST | /api/schools | 新增学校（管理员） |
| PUT | /api/schools/{id} | 更新学校（管理员） |
| DELETE | /api/schools/{id} | 删除学校（管理员） |
| GET | /api/grades | 成绩列表，支持 `?student_id=1` 筛选 |
| GET | /api/grades/{id} | 单条成绩 |
| POST | /api/grades | 新增成绩（管理员） |
| PUT | /api/grades/{id} | 更新成绩（管理员） |
| DELETE | /api/grades/{id} | 删除成绩（管理员） |

## 数据模型

### 学生 (Student)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | str | 姓名 |
| age | int | 年龄 |
| grade | str | 年级/班级 |

### 教师 (Teacher)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | str | 姓名 |
| subject | str | 任教科目 |
| title | str | 职称 |
| phone | str | 联系电话 |

### 学校 (School)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | str | 学校名称 |
| address | str | 地址 |
| school_type | str | 类型（小学/初中/高中） |
| student_count | int | 学生人数 |

### 成绩 (Grade)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| student_id | int? | 关联学生 ID |
| student_name | str | 学生姓名 |
| subject | str | 科目 |
| score | float | 分数（0–100） |
| exam_date | str | 考试日期 |
| semester | str | 学期 |

## 学生与成绩关联

1. **学生列表**：点击学生姓名，弹出该学生的成绩列表
2. **成绩录入**：新增/编辑成绩时，点击「选择学生」打开学生列表，选择后自动填充 `student_id` 与 `student_name`

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| SESSION_SECRET | 会话签名密钥 | dev-secret-change-in-production |
| MYSQL_HOST | MySQL 主机 | localhost |
| MYSQL_USER | MySQL 用户 | root |
| MYSQL_PASSWORD | MySQL 密码 | 空 |
| MYSQL_DATABASE | 数据库名 | student |

## 依赖

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
httpx>=0.26.0
jinja2>=3.1.0
python-multipart>=0.0.6
itsdangerous>=2.1.0
mysql-connector-python>=8.0.0
```

---

启动前请确保 MySQL 已运行，应用启动时会自动创建 `student` 数据库及所需表（若不存在）。
