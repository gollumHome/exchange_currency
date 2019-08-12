Feature: #管理员得到课程,可以下架
  # Enter feature description here

  @admin_course  @admin_course1
  Scenario: # 管理可以查询课程
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
      "is_experience": false
    }
    """
    When 商户'mayun'添加课程
    """
    {
      "title": "我是二个课程",
      "head_diagram": "/static/course.jpg",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "美术",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": true
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
      "is_experience": true
    }
    """
    Given 商户'liuqiangdong'登录系统
    When 商户'liuqiangdong'添加课程
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

    Given 管理员'admin'登录系统
    When 管理员设置查询课程条件
    """
    {
      "title": "我是三个课程"
    }
    """
    Then 管理员'admin'得到查询结果
    """
    [
    {
     "merchant_name": "liuqiangdong",
      "title": "我是三个课程",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": false,
      "status": "upper"
    },
    {
     "merchant_name": "mayun",
      "title": "我是三个课程",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": true,
      "status": "upper"
    }
    ]
    """
    When 管理员设置查询课程条件
    """
    {
      "phone": "15000000001"
    }
    """
    Then 管理员'admin'得到查询结果
    """
    [
        {
      "title": "我是三个课程",
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

    When 管理员设置查询课程条件
    """
    {
      "merchant_name": "liu"
    }
    """
    Then 管理员'admin'得到查询结果
    """
    [
        {
      "title": "我是三个课程",
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

    When 管理员设置查询课程条件
    """
    {
      "merchant_name": "may",
      "is_experience": "false"
    }
    """
    Then 管理员'admin'得到查询结果
    """
    [
       {
      "title": "我是一个课程",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": false,
      "merchant_name": "mayun"
    }
    ]
    """


  @admin_course  @admin_course2
  Scenario: # 管理可以下架课程
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
      "title": "我是二个课程",
      "head_diagram": "/static/course.jpg",
      "count": 5,
      "age_range": "5岁-7岁",
      "course_type": "美术",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": true
    }
    """
    When 商户'mayun'添加课程
    """
    {
      "title": "我是三个课程",
      "count": 5,
      "head_diagram": "/static/course.jpg",
      "age_range": "5岁-7岁",
      "course_type": "练字",
      "origin_price": 20050,
      "price": 10000,
      "plan": "每天一课,上一周",
      "describe": "我是描述",
      "is_experience": true
    }
    """
    Given 商户'liuqiangdong'登录系统
    When 商户'liuqiangdong'添加课程
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
    Given 管理员'admin'登录系统
    When 管理员'admin'下架最新添加的课程
    When 管理员设置查询课程条件
    """
    {
      "status": "lower"
    }
    """
    Then 管理员'admin'得到查询结果
    """
    [
    {
      "title": "我是三个课程",
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
