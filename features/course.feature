Feature: 课程

  @course @course1
  Scenario: 添加课程
    Given 商户'mayun'登录系统
    When 商户'mayun'添加课程
    """
    {
      "title": "我是一个课程",
      "count": 5,
      "head_diagram": "/static/course.jpg",
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
    Then 查看刚刚添加的课程
    """
    {
      "title": "我是一个课程",
      "count": 5,
      "age_range": "5岁-7岁",
      "head_diagram": "/static/course.jpg",
      "course_type": "练字",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": false,
      "status": "upper",
      "settings": [{"name": "sex", "required": true}]
    }
    """

  @course @course2
  Scenario: 添加课程
    Given 商户'mayun'登录系统
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
      "is_experience": false,
      "settings": [{"name": "sex", "required": true}]
    }
    """
    Then 'mayun'修改刚刚的课程
    """
    {
      "title": "我还是一个课程",
      "head_diagram": "/static/xxx.jpg",
      "origin_price": 40050,
      "settings": [{"name": "sex1", "required": true}]
    }
    """
    Then 查看刚刚添加的课程
    """
    {
      "title": "我还是一个课程",
      "head_diagram": "/static/xxx.jpg",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 40050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": false,
      "status": "upper",
      "settings": [{"name": "sex1", "required": true}]
    }
    """
    When 'mayun'下架刚刚添加的课程
    Then 查看刚刚添加的课程
    """
    {
      "title": "我还是一个课程",
      "head_diagram": "/static/xxx.jpg",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 40050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": false,
      "status": "lower"
    }
    """

  @course @course3
  Scenario: 查询多个课程
    Given 商户'mayun'登录系统
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
       When 商户'mayun'添加课程
    """
    {
      "title": "我是三个课程",
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
      "title": "我是四个课程",
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
    Then 查询商户'mayun'的课程offset'1'limit'1'
    """
    [
      {
      "title": "我是三个课程",
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
    ]
    """

  @course @course4
  Scenario: 商户查询课程订单
    Given 商户'mayun'登录系统
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
    Given 用户'zhangyi'登录系统
    When 用户'zhangyi'报名最近添加的课程
    """
    {
      "telephone": "13333333333",
      "full_name": "张三",
      "extra": [{"extend_name": "sex", "value": "female"}]
    }
    """
# 缺少支付
#    Then 商户'mayun'查看课程订单
#    """
#    [
#      {
#
#        "full_name": "张三",
#        "telephone": "13333333333",
#        "extra": [{"extend_name": "sex", "value": "female"}]
#      }
#    ]
#    """

#  @course @course5
#  Scenario: 商户可以删除课程订单,暂时不做
#    Given 商户'mayun'登录系统
#    When 商户'mayun'添加课程
#    """
#    {
#      "title": "我是一个课程",
#      "count": 5,
#      "age_range": "5岁-7岁",
#      "course_type": "练字",
#      "origin_price": 20050,
#      "price": 10000,
#      "plan": "每天一课,上一周",
#      "describe": "我是描述",
#      "is_experience": false
#    }
#    """
#    Given 用户'zhangyi'登录系统
#    When 用户'zhangyi'购买最近添加的课程
#    """
#    {
#      "telephone": "13333333333",
#      "full_name": "张三",
#      "extra": [{"extend_name": "sex", "value": "female"}]
#    }
#    """
#    Then 商户'mayun'查看课程订单
#    """
#    [
#      {
#
#        "full_name": "张三",
#        "telephone": "13333333333",
#        "extra": [{"extend_name": "sex", "value": "female"}]
#      }
#    ]
#    """
#
#    When 商户'mayun'删除最近购买课程的订单
#    When 用户'zhangyi'购买最近添加的课程
#    """
#    {
#      "telephone": "13344444444",
#      "full_name": "张一",
#      "extra": [{"extend_name": "sex", "value": "female"}]
#    }
#    """
#    Then 商户'mayun'查看课程订单
#    """
#    [
#      {
#
#        "full_name": "张一",
#        "telephone": "13344444444",
#        "extra": [{"extend_name": "sex", "value": "female"}]
#      }
#    ]
#    """