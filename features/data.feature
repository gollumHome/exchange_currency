Feature: #专门用来生成数据用
  @data
  Scenario:
    Given 商户'mayun'登录系统
    Given 商户'liuqiangdong'登录系统
    Given 用户'zhangyi'登录系统
    Given 用户'zhanger'登录系统
    Given 用户'zhangsan'登录系统
    Given 用户'zhangsi'登录系统
    Given 用户'zhangwu'登录系统
    Given 用户'zhangliu'登录系统

    # 填充砍价支付活动数据
    When 'mayun'创建砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": "/static/a.jpg",
      "title": "端午节砍价支付活动",
      "original_price": 1000,
      "discount_price": 500,
      "bargain_count": 4,
      "inventory": 3,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "settings": [{"name": "sex", "required": true}]
    }
    """
    When 'mayun'创建微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "type": "microEnroll",
      "title": "端午节微报名活动",
      "original_price": 5000,
      "inventory": 50,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "extra_fields": [{"name": "sex", "required": true}]
    }
    """
    When 'liuqiangdong'创建砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": "/static/a.jpg",
      "title": "端午节砍价支付活动liuqiangdong",
      "original_price": 1000,
      "discount_price": 500,
      "bargain_count": 4,
      "inventory": 3,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "settings": [{"name": "sex", "required": true}]
    }
    """
    When 用户'zhangyi'参加最近添加的砍价支付活动
    When 用户'zhanger'参加最近添加的砍价支付活动
    When 'mayun'创建砍价活动
    """
    {
      "template_id": 1,
      "head_diagram": "/static/a.jpg",
      "title": "端午节砍价活动",
      "original_price": 1000,
      "discount_price": 500,
      "bargain_count": 4,
      "inventory": 3,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "settings": [{"name": "sex", "required": true}]
    }
    """
    When 'liuqiangdong'创建砍价活动
    """
    {
      "template_id": 1,
      "head_diagram": "/static/a.jpg",
      "title": "端午节砍价活动liuqiangdong",
      "original_price": 1000,
      "discount_price": 500,
      "bargain_count": 4,
      "inventory": 3,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "settings": [{"name": "sex", "required": true}]
    }
    """
    When 用户'zhangyi'收藏最近添加的活动
    Then 用户'zhangyi'查询我的收藏
    """
    [
      {
        "title": "端午节砍价活动liuqiangdong",
        "activity_type": "bargain"
      }
    ]
    """
    When 商户'mayun'添加课程
    """
    {
      "title": "我是mayun的一个课程",
      "head_diagram": "/static/a.jpg",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": false,
      "settings": [{"name": "sex", "required": true}]
    }
    """
    When 商户'liuqiangdong'添加课程
    """
    {
      "title": "我是liuqiangdong的一个课程",
      "head_diagram": "/static/a.jpg",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": true,
      "settings": [{"name": "sex", "required": true}]
    }
    """
    When 用户'zhangyi'收藏最近添加的课程
    Then 用户'zhangyi'查询我的收藏
    """
    [
      {
        "title": "我是liuqiangdong的一个课程",
        "is_experience": true
      }, {
        "title": "端午节砍价活动liuqiangdong",
        "activity_type": "bargain"
      }
    ]
    """
    When 用户'zhangyi'报名最近添加的课程
    """
    {
      "telephone": "13333333333",
      "full_name": "张三",
      "extra": [{"extend_name": "sex", "value": "female"}]
    }
    """
    When 商户'liuqiangdong'添加课程
    """
    {
      "title": "我是liuqiangdong的两个课程",
      "head_diagram": "/static/a.jpg",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": true,
      "settings": [{"name": "sex", "required": true}]
    }
    """
    Then 查询商户'liuqiangdong'的课程offset'0'limit'20'
    """
    [
      {
      "title": "我是liuqiangdong的两个课程",
      "head_diagram": "/static/a.jpg",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": true
      }, {
      "title": "我是liuqiangdong的一个课程",
      "head_diagram": "/static/a.jpg",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": true
      }
    ]
    """
    When 商户'mayun'设置预约页面
      """
      {
        "image": "/status/1.jpg",
        "describe": "mayun尽快预约"
      }
      """
    Then 商户'mayun'访问自己的预约页面
    """
      {
        "image": "/status/1.jpg",
        "describe": "mayun尽快预约"
      }
    """
    When 商户'liuqiangdong'设置预约页面
      """
      {
        "image": "/status/1.jpg",
        "describe": "liuqiangdong尽快预约"
      }
      """
    Then 商户'liuqiangdong'访问自己的预约页面
    """
      {
        "image": "/status/1.jpg",
        "describe": "liuqiangdong尽快预约"
      }
    """

    When 'zhangsan'预约商户'mayun'的课程
    """

    {
      "phone": "13333333333",
      "name": "张三",
      "remark": "备注",
      "age_range": "2岁-5岁",
      "courses": ["我是mayun的一个课程"]
    }

    """
    Then 'mayun'查看预约
    """
      [
        {
        "phone": "13333333333",
        "name": "张三",
        "remark": "备注",
        "age_range": "2岁-5岁",
        "courses": [ "我是mayun的一个课程"]
        }
      ]
    """
    When 用户'zhangsan'设置信息
    """
    {
      "province": "浙江",
      "city": "温州",
      "age_range": "5岁-7岁",
      "course_type" :"美术"
    }
    """
    Then 'zhangsan'得到自己的信息
    """
    {
      "province": "浙江",
      "city": "温州",
      "age_range": "5岁-7岁",
      "course_type" :"美术",
      "telephone": "15000000003"
    }
    """