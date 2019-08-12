Feature: 砍价支付

  @bargains_payment @bargains_payment1
  Scenario: 商户创建砍价支付
    Given 商户'mayun'登录系统
    When 'mayun'创建砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节砍价支付活动",
      "original_price": 1000,
      "discount_price": 500,
      "bargain_count": 50,
      "inventory": 20,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "settings": [{"name": "sex", "required": true, "sort_num": 1}]
    }
    """

  @bargains_payment @bargains_payment2
  Scenario: 砍价空状态
    Given 商户'mayun'登录系统
    When 'mayun'创建砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节砍价支付活动",
      "original_price": 1000,
      "discount_price": 500,
      "bargain_count": 50,
      "inventory": 20,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "settings": [{"name": "sex", "required": true}]
    }
    """
    Given 用户'zhangsan'登录系统

    # remnant_inventory 无法验证此字段
    　Then 用户'zhangsan'查看最近创建的支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节砍价支付活动",
      "original_price": 1000,
      "discount_price": 500,
      "bargain_count": 50,
      "inventory": 20,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "settings": [{"name": "sex", "required": true}]
    }
    """

  @bargains_payment @bargains_payment3
  Scenario: 参加活动,一个人只能参加一次
    Given 商户'mayun'登录系统
    When 'mayun'创建砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
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
    Given 用户'zhangyi'登录系统
    When 用户'zhangyi'报名最近添加的活动
    """
      {
        "full_name": "zhangyi",
        "telephone": "13333333333",
        "extra": [{"extend_name": "sex", "value": "female"}]
      }
    """

    Then 得到最近活动的弹幕
    """
    [
      {
        "head_url": "/static/zhangyi.jpg",
        "nickname": "zhangyi"

      }
    ]
    """
    Given 用户'zhanger'登录系统
    When 用户'zhanger'帮'zhangyi'砍价
    When 用户'zhanger'帮'zhangyi'砍价
    Then 得到报错信息'不能再次砍价'


  @bargains_payment @bargains_payment4
  Scenario: 参加活动,砍价有次数限制,并可以查看砍价的详情
    Given 商户'mayun'登录系统
    When 'mayun'创建砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
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
    Given 用户'zhangyi'登录系统
    When 用户'zhangyi'报名最近添加的活动
    """
      {
        "full_name": "zhangyi",
        "telephone": "13333333333",
        "extra": [{"extend_name": "sex", "value": "female"}]
      }
    """

    Given 用户'zhanger'登录系统
    When 用户'zhanger'帮'zhangyi'砍价

    Given 用户'zhangsan'登录系统
    When 用户'zhangsan'帮'zhangyi'砍价

    Given 用户'zhangsi'登录系统
    When 用户'zhangsi'帮'zhangyi'砍价

    Given 用户'zhangwu'登录系统
    When 用户'zhangwu'帮'zhangyi'砍价

    Given 用户'zhangliu'登录系统
    When 用户'zhangliu'帮'zhangyi'砍价
    Then 得到报错信息'没有砍价次数了'
    Then 查看'zhangyi'砍价支付的详情
    """
    [
    { "nickname": "zhangwu", "head_url": "/static/zhangwu.jpg"},
    { "nickname": "zhangsi", "head_url": "/static/zhangsi.jpg"},
    { "nickname": "zhangsan", "head_url": "/static/zhangsan.jpg"},
    { "nickname": "zhanger", "head_url": "/static/zhanger.jpg"}
    ]
    """

    When 用户'zhanger'报名最近添加的活动
    """
      {
        "full_name": "zhanger",
        "telephone": "13333333333",
        "extra": [{"extend_name": "sex", "value": "female"}]
      }
    """
    When 用户'zhangyi'帮'zhanger'砍价
    When 用户'zhangsan'帮'zhanger'砍价
    When 用户'zhangsi'帮'zhanger'砍价

    Then 查看'zhangyi'砍价支付的详情
    """
    [
    { "nickname": "zhangwu"},
    { "nickname": "zhangsi"},
    { "nickname": "zhangsan"},
    { "nickname": "zhanger"}
    ]
    """

    Then 查看'zhanger'砍价支付的详情
    """
    [

    { "nickname": "zhangsi"},
    { "nickname": "zhangsan"},
    { "nickname": "zhangyi"}
    ]
    """


  @bargains_payment @bargains_payment5
  Scenario: 参加活动,活动有次数限制, 无法验证,暂时没有实际意义
    Given 商户'mayun'登录系统
    When 'mayun'创建砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
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
    Given 用户'zhangyi'登录系统
    When 用户'zhangyi'报名最近添加的活动
    """
      {
        "full_name": "zhangyi",
        "telephone": "13333333333",
        "extra": [{"extend_name": "sex", "value": "female"}]
      }
    """


    Given 用户'zhanger'登录系统
    When 用户'zhanger'报名最近添加的活动
    """
      {
        "full_name": "zhanger",
        "telephone": "13333333333",
        "extra": [{"extend_name": "sex", "value": "female"}]
      }
    """


    Given 用户'zhangsan'登录系统
    When 用户'zhangsan'报名最近添加的活动
    """
      {
        "full_name": "zhangsan",
        "telephone": "13333333333",
        "extra": [{"extend_name": "sex", "value": "female"}]
      }
    """


    Given 用户'zhangsi'登录系统
    When 用户'zhangsi'报名最近添加的活动
    """
      {
        "full_name": "zhangsi",
        "telephone": "13333333333",
        "extra": [{"extend_name": "sex", "value": "female"}]
      }
    """
    #Then 得到报错信息'您来晚了,已抢完!'
#    Then 得到最近添加活动的所有参加人员

  @bargains_payment @bargains_payment6
  Scenario: 自己查看自己参加的活动
    Given 商户'mayun'登录系统
    When 'mayun'创建砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
      "title": "端午节砍价支付活动",
      "original_price": 1000,
      "discount_price": 500,
      "bargain_count": 50,
      "inventory": 20,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "练字",
      "settings": [{"name": "sex", "required": true}]
    }
    """
    Given 用户'zhangsan'登录系统
    Then 用户'zhangsan'查看最近创建的支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
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
      "settings": [{"name": "sex", "required": true}]
    }
    """
    When 用户'zhangsan'报名最近添加的活动
    """
      {
        "full_name": "zhangsan",
        "telephone": "13333333333",
        "extra": [{"extend_name": "sex", "value": "female"}]
      }
    """
    Then 用户'zhangsan'查看最近创建的支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
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
      "settings": [{"name": "sex", "required": true}],
      "bargain": {
        "user": {
        "head_url": "/static/zhangsan.jpg",
        "nickname": "zhangsan"
        },
        "price": 1000,
        "status": "start"
      }
    }
    """
    Given 用户'zhangyi'登录系统
    Then 用户'zhangyi'查看'zhangsan'分享的砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
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
      "settings": [{"name": "sex", "required": true}],
      "bargain": {
        "user": {
        "head_url": "/static/zhangsan.jpg",
        "nickname": "zhangsan"
        },
        "price": 1000,
        "status": "start"
      }
    }
    """

  @bargains_payment @bargains_payment7
  Scenario: 商家可以修改活动
    Given 商户'mayun'登录系统
    When 'mayun'创建砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
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
    Then 商家'mayun'查看最近的砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": ["/static/a.jpg"],
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
    When 商家'mayun'修改最近的砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": "/static/b.jpg",
      "title": "国庆节砍价支付活动",
      "original_price": 4000,
      "discount_price": 2000,
      "bargain_count": 4,
      "inventory": 3,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "barrage": "active",
      "category": "美术",
      "settings": [{"name": "sex1", "required": true}]
    }
    """
    Then 商家'mayun'查看最近的砍价支付活动
    """
    {
      "template_id": 1,
      "head_diagram": "/static/b.jpg",
      "title": "国庆节砍价支付活动",
      "original_price": 4000,
      "discount_price": 2000,
      "bargain_count": 4,
      "inventory": 3,
      "finish_time": "明天",
      "music": "稻花香",
      "effect": "雪花",
      "activity_types": "bargainWithPay",
      "barrage": "active",
      "category": "美术",
      "settings": [{"name": "sex1", "required": true}]
    }
    """
