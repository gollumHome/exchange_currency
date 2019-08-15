
# exchange-currency-api

#### 介绍
服务器端接口

#### 模块
- user: 用户
- pay: 支付
- order: 订单
- backend: 后台

#### 生成 Model
生成的 model 需要适配
```bash
pip install sqlacodegen
sqlacodegen mysql://root:nas@mhm1234@139.196.78.95:3306/school-saas > models.py
```

#### 迁移数据库

```bash
export FLASK_APP=manage.py

# model修改生成新的迁移文件
flask db migrate

# 执行迁移文件
flask db upgrade

```

#### 单元测试
```bash
# 准备
# pip install flask-testing pytest

# 测试整个 test 目录
python -m pytest
# 测试指定模块
python -m pytest -s test\test_merchant.py
# 测试指定函数/方法
python -m pytest -s test\test_merchant.py::TestMerchant::test_register
```

#### docs
```bash
python manage.py
```
打开 [http://localhost:8000/docs/api](http://localhost:8000/docs/api)
=======
# exchange_currency
