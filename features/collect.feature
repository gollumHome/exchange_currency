Feature: 收藏活动,收藏课程
  # 用户可以收藏活动,可以收藏课程,可以查询收藏,取消收藏
  @collect @collect1
  Scenario: 收藏活动
    Given 商户'mayun'登录系统
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
      "activity_types": "bargainWithPay",
      "barrage": "active",
      "category": "练字",
      "settings": [{"name": "sex", "required": true}]
    }
    """
    Given 用户'zhangyi'登录系统
    When 用户'zhangyi'收藏最近添加的活动
    Then 用户'zhangyi'查询我的收藏
    """
    [
      {
        "title": "端午节砍价支付活动",
        "activity_type": "bargainWithPay"
      }
    ]
    """

  @collect @collect2
  Scenario: 收藏课程
    Given 商户'mayun'登录系统
    When 商户'mayun'添加课程
    """
    {
      "title": "我是一个课程",
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
    Given 用户'zhangyi'登录系统
    When 用户'zhangyi'收藏最近添加的课程
    Then 用户'zhangyi'查询我的收藏
    """
    [
      {
        "title": "我是一个课程",
        "is_experience": false
      }
    ]
    """
