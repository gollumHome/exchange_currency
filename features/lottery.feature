Feature: # 抽奖
  @lottery @lottery1
  Scenario: 商户可以创建抽奖活动,可以查看抽奖活动
   Given 商户'mayun'登录系统
    When 'mayun'创建抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "type": "lottery",
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "draws_count": 5,
      "unlocks_count": 3,
      "extra_fields": [{"name": "sex", "required": true}],
      "prizes": [{"award": "一等奖", "name": "奖励的课程", "image": "1.jpg", "count": 2, "probability": 5000}]
    }
    """
    Then 商户'mayun'查看最近创建的抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "lottery",
      "settings": [{"name": "sex", "required": true}],
      "draws_count": 5,
      "unlocks_count": 3,
      "prizes": [{"award": "一等奖", "name": "奖励的课程", "image": "1.jpg", "count": 2, "probability": 5000}]
    }
    """

  @lottery @lottery2
  Scenario: 商户可以更新抽奖活动
   Given 商户'mayun'登录系统
    When 'mayun'创建抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "type": "lottery",
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "draws_count": 5,
      "unlocks_count": 3,
      "extra_fields": [{"name": "sex", "required": true}],
      "prizes": [{"award": "一等奖", "name": "奖励的课程", "image": "1.jpg", "count": 2, "probability": 5000}]
    }
    """
    When 商家'mayun'更新抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/b.jpg"],
      "type": "lottery",
      "title": "端午节抽奖活动1",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "美术",
      "draws_count": 6,
      "unlocks_count": 8,
      "settings": [{"name": "sex1", "required": true}],
      "prizes": [{"award": "一等奖1", "name": "奖励的课程1", "image": "11.jpg", "count": 21, "probability": 6000}]
    }
    """
    Then 商户'mayun'查看最近创建的抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/b.jpg"],
      "title": "端午节抽奖活动1",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "美术",
      "activity_types": "lottery",
      "settings": [{"name": "sex1", "required": true}],
      "prizes": [{"award": "一等奖1", "name": "奖励的课程1", "image": "11.jpg", "count": 21, "probability": 6000}]
    }
    """

  @lottery @lottery3
  Scenario: 用户查看抽奖活动
    Given 商户'mayun'登录系统
    When 'mayun'创建抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "type": "lottery",
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "draws_count": 5,
      "unlocks_count": 3,
      "extra_fields": [{"name": "sex", "required": true}],
      "prizes": [{"award": "一等奖", "name": "奖励的课程", "image": "1.jpg", "count": 2, "probability": 5000}]
    }
    """
    Given 用户'zhangyi'登录系统
    Then 用户'zhangyi'查看最近创建的抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "lottery",
      "enroll": {}
    }
    """

  @lottery @lottery4
  Scenario: 用户可以抽奖, 没有抽奖次数的时候
    Given 商户'mayun'登录系统
    When 'mayun'创建抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "type": "lottery",
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "draws_count": 5,
      "unlocks_count": 3,
      "extra_fields": [{"name": "sex", "required": true}],
      "prizes": [{"award": "一等奖", "name": "奖励的课程", "image": "1.jpg", "count": 2, "probability": 5000}]
    }
    """
    Given 用户'zhangyi'登录系统
    When 用户'zhangyi'报名最近添加的活动
    """
      {
        "full_name": "zhangyi",
        "telephone": "13333333333",
        "extra": [{"extend_name": "sex", "value": "female"}]
      }
    """

    When 用户'zhangyi'在最近的抽奖活动中抽奖
    Then 返回success
    When 用户'zhangyi'在最近的抽奖活动中抽奖
    Then 得到报错信息'次数不足'
    Then 用户'zhangyi'查看最近创建的抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "lottery",
      "enroll": {"nickname": "zhangyi", "status": "unpaid"}
    }
    """
    Given 用户'zhanger'登录系统
    Then 用户'zhanger'查看'zhangyi'share的抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "lottery",
      "enroll": {"nickname": "zhangyi", "status": "unpaid"}
    }
    """

  @lottery @lottery4
  Scenario: 用户报名后查看抽奖活动
    Given 商户'mayun'登录系统
    When 'mayun'创建抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "type": "lottery",
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "draws_count": 5,
      "unlocks_count": 3,
      "extra_fields": [{"name": "sex", "required": true}],
      "prizes": [{"award": "一等奖", "name": "奖励的课程", "image": "1.jpg", "count": 2, "probability": 5000}]
    }
    """
    Given 用户'zhangyi'登录系统
    Given 用户'zhanger'登录系统
    Given 用户'zhangsan'登录系统
    Given 用户'zhangsi'登录系统
    Given 用户'zhangwu'登录系统
    Given 用户'zhangliu'登录系统
    Given 用户'zhangqi'登录系统
    Given 用户'zhangba'登录系统
    Given 用户'zhangjiu'登录系统
    Given 用户'zhang10'登录系统
    Given 用户'zhang11'登录系统
    Given 用户'zhang12'登录系统
    Given 用户'zhang13'登录系统
    Given 用户'zhang14'登录系统
    Given 用户'zhang15'登录系统
    Given 用户'zhang16'登录系统
    Then 用户'zhangyi'查看最近创建的抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "lottery"
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
    Then 用户'zhangyi'查看最近创建的抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "lottery",
      "enroll": {"nickname": "zhangyi", "status": "unpaid"},
      "remaining_times": 1,
      "lock_times": 0,
      "help_times": 0,
      "can_user_help_times": 0
    }
    """
    When 用户'zhangyi'在最近的抽奖活动中抽奖
    Then 用户'zhangyi'查看最近创建的抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "lottery",
      "enroll": {"nickname": "zhangyi", "status": "unpaid"},
      "remaining_times": 0,
      "lock_times": 0,
      "help_times": 0,
      "can_user_help_times": 0
    }
    """
    When 用户'zhanger'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhanger'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 得到报错信息'已经帮过了'

    When 用户'zhangsan'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    Then 用户'zhangyi'查看最近创建的抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "lottery",
      "enroll": {"nickname": "zhangyi", "status": "unpaid"},
      "remaining_times": 0,
      "lock_times": 0,
      "help_times": 2,
      "can_user_help_times": 2
    }
    """
    When 用户'zhangsi'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    Then 用户'zhangyi'查看最近创建的抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "activity_types": "lottery",
      "enroll": {"nickname": "zhangyi", "status": "unpaid"},
      "remaining_times": 1,
      "lock_times": 1,
      "help_times": 3,
      "can_user_help_times": 0
    }
    """
    When 用户'zhangwu'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhangliu'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhangqi'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhangba'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhangjiu'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhang10'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhang11'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhang12'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhang13'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhang14'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 得到报错信息'没有抽奖次数了'

    When 用户'zhangyi'在最近的抽奖活动中抽奖
    Then 返回success
    When 用户'zhangyi'在最近的抽奖活动中抽奖
    Then 返回success
    When 用户'zhangyi'在最近的抽奖活动中抽奖
    Then 返回success
    When 用户'zhangyi'在最近的抽奖活动中抽奖
    Then 返回success
    When 用户'zhangyi'在最近的抽奖活动中抽奖
    Then 得到报错信息'次数不足'

  @lottery @lottery5
  Scenario: 奖品有次数限制
    Given 商户'mayun'登录系统
    When 'mayun'创建抽奖活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "type": "lottery",
      "title": "端午节抽奖活动",
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "draws_count": 5,
      "unlocks_count": 1,
      "extra_fields": [{"name": "sex", "required": true}],
      "prizes": [{"award": "一等奖", "name": "奖励的课程", "image": "1.jpg", "count": 2, "probability": 10000}]
    }
    """
    Given 用户'zhangyi'登录系统
    Given 用户'zhanger'登录系统
    Given 用户'zhangsan'登录系统
    Given 用户'zhangsi'登录系统

    When 用户'zhangyi'报名最近添加的活动
    """
      {
        "full_name": "zhangyi",
        "telephone": "13333333333",
        "extra": [{"extend_name": "sex", "value": "female"}]
      }
    """
    When 用户'zhangyi'在最近的抽奖活动中抽奖
    When 用户'zhanger'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhangyi'在最近的抽奖活动中抽奖
    When 用户'zhangsan'给'zhangyi'最近参加的抽奖活动增加抽奖机会
    Then 返回success
    When 用户'zhangyi'在最近的抽奖活动中抽奖
    Then 得到报错信息'没中奖'

