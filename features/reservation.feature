Feature: 预约

  @reservation @reservation1
  Scenario: 访问预约页面,生成预约表
    Given 商户'mayun'登录系统
    When 商户'mayun'设置预约页面
      """
      {
        "image": "/status/1.jpg",
        "describe": "尽快预约"
      }
      """

    Then 商户'mayun'访问自己的预约页面
    """
      {
        "image": "/status/1.jpg",
        "describe": "尽快预约"
      }
    """
  @reservation @reservation2
  Scenario: 用户可以预约课程
    Given 商户'mayun'登录系统
    When 商户'mayun'设置预约页面
      """
      {
        "image": "/status/1.jpg",
        "describe": "尽快预约"
      }
      """

    Then 商户'mayun'访问自己的预约页面
    """
      {
        "image": "/status/1.jpg",
        "describe": "尽快预约"
      }
    """
    When 商户'mayun'添加课程
    """
    {
      "title": "我是一个课程",
      "head_diagram": "/static/course.jpg",
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
   When 商户'mayun'添加课程
    """
    {
      "title": "我是两个课程",
      "head_diagram": "/static/course.jpg",
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
    Given 用户'zhangsan'登录系统
    Then 'zhangsan'查看商户'mayun'预约页面
    """
    {
      "image": "/status/1.jpg",
      "describe": "尽快预约"
    }
    """
    When 'zhangsan'预约商户'mayun'的课程
    """

    {
      "phone": "13333333333",
      "name": "张三",
      "remark": "备注",
      "age_range": "2岁-5岁",
      "courses": ["我是两个课程", "我是一个课程"]
    }

    """
    When 管理员设置查询课程条件
    """
    {
      "filter_str": "13"
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
        "courses": [ "我是一个课程", "我是两个课程"]
        }
      ]
    """
    When 管理员设置查询课程条件
    """
    {
      "filter_str": "13"
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
        "courses": [ "我是一个课程", "我是两个课程"]
        }
      ]
    """
    When 管理员设置查询课程条件
    """
    {
      "filter_str": "99"
    }
    """
    Then 'mayun'查看预约
    """
    []
    """
