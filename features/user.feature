Feature: 用户页面

  @user @user1
  Scenario: 用户可以修改信息
    Given 用户'zhangsan'登录系统
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

  @user @user2
  Scenario: 用户可以修改信息,可以修改手机号码,验证手机号码格式
    Given 用户'zhangsan'登录系统
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
    When 用户'zhangsan'发送'15000000033'验证码
    When 用户'zhangsan'设置手机号码
    """
    {
      "telephone": "10000000033",
      "code": "随机生成"
    }
    """
    Then 得到报错信息'请输入正确的手机号'

    When 用户'zhangsan'设置手机号码
    """
    {
      "telephone": "",
      "code": "随机生成"
    }
    """
    Then 得到报错信息'手机号不能为空'

    When 用户'zhangsan'设置手机号码
    """
    {
      "telephone": "15000000033",
      "code": "随机生成"
    }
    """
    Then 返回success

    Then 'zhangsan'得到自己的信息
    """
    {
      "province": "浙江",
      "city": "温州",
      "age_range": "5岁-7岁",
      "course_type" :"美术",
      "telephone": "15000000033"
    }
    """