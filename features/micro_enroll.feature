Feature: #微报名
  @micro_enroll @micro_enroll1
  Scenario: 商户可以创建微报名活动,可以查看微报名活动
   Given 商户'mayun'登录系统
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
    Then 商户'mayun'查看最近创建的微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节微报名活动",
      "original_price": 5000,
      "inventory": 50,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "microEnroll",
      "settings": [{"name": "sex", "required": true}]
    }
    """


  @micro_enroll @micro_enroll2
  Scenario: 商户可以修改微报名活动
   Given 商户'mayun'登录系统
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
    When 商家'mayun'修改最近的微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "type": "microEnroll",
      "title": "端午节微报名活动",
      "original_price": 6000,
      "inventory": 20,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "口才",
      "settings": [{"name": "sex1", "required": true}]
    }
    """
    Then 商户'mayun'查看最近创建的微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节微报名活动",
      "original_price": 6000,
      "inventory": 20,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "口才",
      "activity_types": "microEnroll",
      "settings": [{"name": "sex1", "required": true}]
    }
    """

  @micro_enroll @micro_enroll3
  Scenario: 用户可以查看微报名活动,商家活动刚发布,无任何人报名
   Given 商户'mayun'登录系统
    When 'mayun'创建微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "type": "microEnroll",
      "title": "端午节微报名活动",
      "original_price": 5000,
      "inventory": 4,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "extra_fields": [{"name": "sex", "required": true}]
    }
    """
    Given 用户'zhangyi'登录系统
    Then 用户'zhangyi'查看最近的微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节微报名活动",
      "original_price": 5000,
      "inventory": 4,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "microEnroll",
      "settings": [{"name": "sex", "required": true}]
    }
    """


  @micro_enroll @micro_enroll4
  Scenario: 用户报名微报名活动,然后查看活动
   Given 商户'mayun'登录系统
    When 'mayun'创建微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "type": "microEnroll",
      "title": "端午节微报名活动",
      "original_price": 5000,
      "inventory": 4,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "extra_fields": [{"name": "sex", "required": true}]
    }
    """
    Given 用户'zhangyi'登录系统
    Then 用户'zhangyi'查看最近的微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节微报名活动",
      "original_price": 5000,
      "inventory": 4,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "microEnroll",
      "settings": [{"name": "sex", "required": true}]
    }
    """
   When 用户'zhangyi'报名最近添加的活动
   """
    {
      "full_name": "zhangyi",
      "telephone": "13333333333",
      "extra": [{"extend_name": "sex", "value": "female"}]
    }
   """
   Then 用户'zhangyi'查看最近的微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节微报名活动",
      "original_price": 5000,
      "inventory": 4,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "microEnroll",
      "settings": [{"name": "sex", "required": true}],
      "enroll": {"nickname": "zhangyi", "status": "unpaid"}
    }
    """
   Given 用户'zhanger'登录系统
   When 用户'zhanger'报名最近添加的活动
   """
    {
      "full_name": "zhanger",
      "telephone": "13333333334",
      "extra": [{"extend_name": "sex", "value": "female"}]
    }
   """
   Then 用户'zhangyi'查看最近的微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节微报名活动",
      "original_price": 5000,
      "inventory": 4,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "microEnroll",
      "settings": [{"name": "sex", "required": true}],
      "enroll": {"nickname": "zhangyi", "status": "unpaid"}
    }
    """
   Then 用户'zhanger'查看最近的微报名活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节微报名活动",
      "original_price": 5000,
      "inventory": 4,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "microEnroll",
      "settings": [{"name": "sex", "required": true}],
      "enroll": {"nickname": "zhanger", "status": "unpaid"}
    }
    """
