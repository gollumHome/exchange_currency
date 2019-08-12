Feature: #用户中心

  @user_center @user_center1
  Scenario: # 用户中心查询活动
    Given 商户'mayun'登录系统
    When 'mayun'创建砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": "/static/a.jpg",
      "title": "端午节砍价支付活动",
      "original_price": 1000,
      "discount_price": 500,
      "bargain_count": 50,
      "inventory": 20,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "activity_types": "bargainWithPay",
      "barrage": "active",
      "category": "练字",
      "settings": [{"name": "sex", "required": true, "sort_num": 1}]
    }
    """
    Given 用户'zhangyi'登录系统
    When 用户'zhangyi'参加最近添加的砍价支付活动

    And 用户'zhangyi'报名最近添加的活动
    """
    {
      "full_name": "zhangyi",
      "telephone": "13333333333",
      "extra": [{"extend_name": "sex", "value": "female"}]
    }
    """
# 需要购买的接口
#    Then 用户'zhangyi'查询自己报名的活动
#    """
#    [
#      {
#        "activity_types": "bargainWithPay",
#        "title": "端午节砍价支付活动"
#      }
#    ]
#    """
#
#    Given 用户'zhanger'登录系统
#    When 用户'zhanger'参加最近添加的砍价支付活动
#
#    And 用户'zhangyi'报名最近添加的活动
#    """
#    {
#      "full_name": "zhanger",
#      "telephone": "13333333334",
#      "extra": [{"extend_name": "sex", "value": "female"}]
#    }
#    """
#
#    Then 用户'zhangyi'查询自己报名的活动
#    """
#    [
#      {
#        "activity_types": "bargainWithPay",
#        "title": "端午节砍价支付活动"
#      }
#    ]
#    """

  @user_center @user_center2
  Scenario: # 用户中心查询课程
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
      "is_experience": false
    }
    """
    Given 用户'zhangyi'登录系统
    When 用户'zhangyi'报名最近添加的课程
    """
    {
      "telephone": "13333333333",
      "full_name": "张三",
      "extra": [{"extend_name": "sex", "value": "female"}]
    }
    """
#  需要购买的接口
#    Then 用户'zhangyi'查询自己报名的课程
#    """
#    [
#      {
#        "is_experience": false,
#        "title": "我是一个课程"
#      }
#    ]
#    """