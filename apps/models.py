# -*- coding: utf-8 -*-

import re
import time

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import class_mapper, synonym

from . import db

IMAGE_PATTERN = re.compile(r".*\.(png|jpg|jpeg|bmp|gif)", re.I)

# 年龄段
AGE_RANGE = db.Enum("2岁-5岁","5岁-7岁",	"7岁-12岁", "12岁以上")

# 课程类型
COURSE_TYPE = db.Enum('美术', '练字', '书法', '英语', '魔方', '课外辅导', '作文', '钢琴', '舞蹈',
                      '口才', '幼儿园', '乐高', '机器人', '编程', '跆拳道', '早教',
                      '幼小衔接', '架子鼓', '托管', '围棋', '武术', '体育', '音乐', '其他')

# 商户行业
MERCHANT_INDUSTRY = ("教育培训", "餐饮美食", "消费购物", "休闲娱乐", "美容美发", "婚庆影楼", " 运动健身",
                     "汽车美容", "家装建材", "广告公司", "其他")

# 商户规模
MERCHANT_SIZE = ('1-10人', '10-50人', '50人-100人', '100人以上')

# 活动类型
ACTIVITY_TYPES = db.Enum(
    'bargainWithPay',  # 砍价支付
    'bargain',  # 砍价
    'groups',
    'groupsWithRetail',
    'fissionCoupon',
    'assist',
    'envelopeWithRetail',
    'microEnroll',  # 微报名
    'lottery',  # 抽奖
    'assistWithPay',  # 助力支付版
    'collectCard'  # 集卡
)

# 产品类型
PRODUCT_TYPE = db.Enum('activity', 'course', 'merchant')


def current_timestamp(*args, **kwargs):
    return int(time.time())


class BaseModel(db.Model):
    __abstract__ = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def type_to_name(self):
        if hasattr(self, "activity_types"):
            return self.name_of_type(self.activity_types)
        return ""

    @staticmethod
    def name_of_type(t):
        return {
            "bargainWithPay": "砍价支付版",
            "bargain": "砍价",
            "groups": "拼团",
            "groupsWithRetail": "拼团分销版",
            "fissionCoupon": "裂变现金券",
            "assist": "助力类",
            "envelopeWithRetail": "分销红包",
            "micro_enroll": "微报名",
        }.get(t, "未知")


class AccessToken(BaseModel):
    __tablename__ = 'Access_token'

    id = db.Column(db.BIGINT(), primary_key=True)
    access_token = db.Column(db.String(530), nullable=False)
    expire_in = db.Column(db.INTEGER(), nullable=False)
    update_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp)


# 手机验证码
class TelVerifyCode(BaseModel):
    __tablename__ = 'Tel_VerifyCode'
    id = db.Column(db.Integer, primary_key=True)
    telephone = db.Column(db.String(64), unique=True, index=True)  # 手机号
    verifyCode = db.Column(db.String(64), unique=False, index=True)  # 验证码
    create_time = db.Column(db.Integer, unique=False, index=True, default=current_timestamp)
    dead_line = db.Column(db.Integer, unique=False, index=True)  # 失效时间
    usable = db.Column(db.Integer, unique=False, index=False)  # 1.无效 2.有效，因为有 dead_line，目前不需要使用这个字段
    verify_type = db.Column(db.Enum('mch_register', 'add_phone', 'reset_pass', 'withdraw'), unique=False, index=True)  # 手机号

    def __repr__(self):
        return '<TelVerifyCode %d %s %d %d %d %d>' % (self.id,  self.telephone, self.verifyCode, self.create_time,
                                                      self.dead_line, self.usable)


class User(BaseModel):
    """用户"""
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(130), unique=False, index=True)
    nickname = db.Column(db.String(60), unique=False, index=False)
    head_url = db.Column(db.String(255), unique=False, index=False, comment='头像')
    telephone = db.Column(db.String(12), nullable=False, comment='手机')
    session_key = db.Column(db.String(120), unique=False, index=False)
    access_token = db.Column(db.String(1500), unique=False, index=False)
    favorite_course = db.Column(COURSE_TYPE)  # 喜欢的课程类型
    age_range = db.Column(AGE_RANGE) # 年龄段
    province = db.Column(db.String(50))  # 省
    city = db.Column(db.String(50))  # 城市
    child_name = db.Column(db.String(30), comment='小孩姓名')
    create_time = db.Column(db.Integer, unique=False, index=True, default=current_timestamp)
    expire_time = db.Column(db.Integer, unique=False, index=True, default=current_timestamp)
    login_time = db.Column(db.Integer, unique=False, index=True, default=current_timestamp)
    status = db.Column(db.Enum('normal', 'black'), unique=False, index=True)

    # def __repr__(self):
    #     return '<User %d %s %s %s %s %s %d %d>' % (self.id, self.openid, self.nickname, self.head_url, self.session_key,
    #                                                self.access_token, self.create_time, self.expire_time)
    def get_user_info(self):
        """
                获取当前用户基本信息
                :return:
                """
        return self.nickname, self.head_url, self.telephone

    def get_pay_info(self):
        """
        获取当前用户消费次数和消费金额
        :return:
        """
        counts = 0
        query = ChannelPay.query.filter_by(user_id=self.id, status='success')
        for pay in query:
            counts += int(pay.total_fee)
        return query.count(), counts


class Account(BaseModel):
    __tablename__ = 'Account'

    id = db.Column(db.BIGINT(), primary_key=True)
    user_id = db.Column(db.BIGINT(), nullable=False)
    balance = db.Column(db.INTEGER())
    unsettled = db.Column(db.INTEGER())
    available = db.Column(db.INTEGER())
    status = db.Column(db.Enum('common', 'black'), nullable=False)


class Activity(BaseModel):
    """活动"""
    __tablename__ = 'Activity'

    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True)
    merchant_id = db.Column(db.BIGINT())
    merchant_name = db.Column(db.String(150, 'utf8mb4_bin'), nullable=False)
    template_id = db.Column(db.INTEGER(), primary_key=True, nullable=False)
    user_id = db.Column(db.BIGINT())
    title = db.Column(db.String(150, 'utf8mb4_bin'), nullable=False, comment='活动标题')
    head_diagram = db.Column(db.JSON)  # head_diagram = db.Column(db.String(355))
    status = db.Column(db.Enum('finish', 'active', 'inactive'), default="active")
    original_price = db.Column(db.INTEGER())  # 原价
    discount_price = db.Column(db.INTEGER())  # 单独购买价  / 砍价活动:底价
    prepayment = db.Column(db.INTEGER())
    team_limit = db.Column(db.INTEGER())  # 成团人数
    inventory = db.Column(db.INTEGER(), nullable=False)  # 库存
    finish_time = db.Column(db.INTEGER(), nullable=False)
    rules = db.Column(db.Text, default="")
    introduction = db.Column(db.Text)
    music = db.Column(db.JSON)  # {"id": music.id, "name": music.name, "url": music.url}
    effect = db.Column(db.JSON)
    video_url = db.Column(db.String(160, 'utf8mb4_bin'))
    category = db.Column(COURSE_TYPE, server_default=db.text("'美术'"), comment='课程分类')
    barrage = db.Column(db.Enum('close', 'active'), server_default=db.text("'close'"))  # 开启弹幕
    bargain_count = db.Column(db.INTEGER())  # 砍价活动:砍价人数
    special_params = db.Column(db.JSON)  # 不同类型的活动，特殊的参数 抽奖:{draws_count: int, unlocks_count: int}
    activity_types = db.Column(ACTIVITY_TYPES, comment='活动类型')
    view_count = db.Column(db.INTEGER(), default=0, comment='查看人数')
    enroll_count = db.Column(db.INTEGER(), default=0, comment='报名人数')
    create_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp)
    update_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp, onupdate=current_timestamp)
    background = db.Column(db.String(160, 'utf8mb4_bin'))

    def head_diagram_with_media(self):
        if not self.head_diagram:
            return self.head_diagram
        ret = []
        for media in self.head_diagram:
            if isinstance(media, str):  # 兼容之前的图片链接字符串列表格式
                media_type = "image" if IMAGE_PATTERN.match(media) else "video"
                ret.append({
                    "url": media,
                    "media": media_type,
                })
            else:
                ret.append(media)
        return ret

    def head_diagram_without_media(self):
        if not self.head_diagram:
            return self.head_diagram
        ret = []
        for media in self.head_diagram:
            if not isinstance(media, str):
                ret.append(media["url"])
            else:
                ret.append(media)
        return ret

    def head_diagram_without_video(self, default_diagram):
        if not self.head_diagram:
            return [default_diagram]
        ret = []
        for media in self.head_diagram:
            if not isinstance(media, str):
                if media["media"] == "image":
                    ret.append(media["url"])
            else:
                ret.append(media)
        if len(ret) == 0:
            ret.append(default_diagram)
        return ret[0:1]


class ActivityTemplate(BaseModel):
    __tablename__ = 'ActivityTemplate'

    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String(50, 'utf8mb4_bin'), nullable=False)
    activity_types = db.Column(ACTIVITY_TYPES)
    head_diagram = db.Column(db.String(1024, 'utf8mb4_bin'), nullable=False)
    cover = db.Column(db.String(1024, 'utf8mb4_bin'))
    background_type = db.Column(db.Enum('color', 'image'))
    background = db.Column(db.String(1024, 'utf8mb4_bin'))
    introduction = db.Column(db.Text)
    collect_num = db.Column(db.INTEGER(), default=0)
    status = db.Column(db.Enum('del', 'normal'), default='normal')
    create_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp)
    update_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp, onupdate=current_timestamp)


class ActivityDetail(BaseModel):
    __tablename__ = 'Activity_Detail'

    id = db.Column(db.BIGINT(), primary_key=True)
    activity_id = db.Column(db.BIGINT(), nullable=False)
    special_key = db.Column(db.JSON)
    special_value = db.Column(db.JSON)


class AdminUser(BaseModel):
    __tablename__ = 'Admin_User'

    id = db.Column(db.BIGINT(), primary_key=True)
    nickname = db.Column(db.String(60, 'utf8_bin'))
    password = db.Column(db.String(255, 'utf8_bin'))
    head_url = db.Column(db.String(255, 'utf8_bin'))
    access_token = db.Column(db.String(1500, 'utf8_bin'))
    type = db.Column(db.Enum('common'), default="common")
    create_time = db.Column(db.INTEGER(), default=current_timestamp)
    update_time = db.Column(db.INTEGER(), default=current_timestamp, onupdate=current_timestamp)
    login_time = db.Column(db.INTEGER())


class Advert(BaseModel):
    """广告"""
    __tablename__ = 'Advert'

    id = db.Column(db.BIGINT(), primary_key=True)
    type = db.Column(db.Enum('merchant', 'activity', 'activityPopup'), comment='广告类型')
    image_url = db.Column(db.String(1024, 'utf8mb4_bin'), comment='图片地址')
    target_url = db.Column(db.String(1024, 'utf8mb4_bin'), comment='跳转地址')
    number = db.Column(db.INTEGER(), nullable=False, default=0, comment='排序')
    status = db.Column(db.Enum('del', 'normal'), default='normal', comment='状态')
    create_time = db.Column(db.INTEGER(), default=current_timestamp, comment='创建时间')
    update_time = db.Column(db.INTEGER(), default=current_timestamp, comment='修改时间', onupdate=current_timestamp)


class Banner(BaseModel):
    __tablename__ = 'Banner'

    id = db.Column(db.INTEGER(), primary_key=True)
    img_url = db.Column(db.String(255, 'utf8_unicode_ci'), nullable=False)
    status = db.Column(db.Enum('common', 'del'))
    welfares_id = db.Column(db.INTEGER())
    create_time = db.Column(db.INTEGER(), default=current_timestamp)


class Barrage(BaseModel):
    """
    弹幕
    """
    __tablename__ = 'Barrage'

    id = db.Column(db.BIGINT(), primary_key=True)
    type = db.Column(db.Enum('merchant', 'user'), nullable=False)
    activity_id = db.Column(db.BIGINT())
    template_id = db.Column(db.BIGINT())
    merchant_id = db.Column(db.BIGINT())
    user_id = db.Column(db.BIGINT())
    content = db.Column(db.String(255, 'utf8mb4_bin'))
    nickname = db.Column(db.String(120, 'utf8mb4_bin'))
    head_url = db.Column(db.String(255, 'utf8mb4_bin'))
    status = db.Column(db.Enum('del', 'normal'), default="normal")
    create_time = db.Column(db.INTEGER(), default=current_timestamp)


class BookSubject(BaseModel):
    __tablename__ = 'Book_Subject'

    id = db.Column(db.BIGINT(), primary_key=True)
    merchant_id = db.Column(db.BIGINT(), nullable=False)
    subject_describe = db.Column(db.JSON)  # db.Column(db.String(120))
    subject = db.Column(db.Enum('enroll','service_fee','channel_fee','withdraw','reward','refund'), nullable=False)
    transaction_id = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.INTEGER(), nullable=False)
    create_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp)

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name))\
                    for col in class_mapper(obj.__class__).mapped_table.c)


class Category(BaseModel):
    __tablename__ = 'Category'

    id = db.Column(db.INTEGER(), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    category_level = db.Column(db.INTEGER(), nullable=False)
    parent_id = db.Column(db.INTEGER(), nullable=False)


class ChannelPay(BaseModel):
    __tablename__ = 'Channel_Pay'

    id = db.Column(db.BIGINT(), primary_key=True)
    openid = db.Column(db.String(60))
    user_id = db.Column(db.BIGINT())
    merchant_id = db.Column(db.BIGINT())
    mch_id = db.Column(db.String(50))
    total_fee = db.Column(db.String(30))
    attach = db.Column(db.String(128))
    out_trade_no = db.Column(db.String(80))
    transaction_id = db.Column(db.String(50))
    pay_time = db.Column(db.INTEGER())
    status = db.Column(db.Enum('success', 'paying', 'fail'))
    create_time = db.Column(db.INTEGER(), default=current_timestamp)


class Collect(BaseModel):
    __tablename__ = 'Collects'

    id = db.Column(db.BIGINT(), primary_key=True)
    product_id = db.Column(db.BIGINT())
    user_id = db.Column(db.BIGINT())
    merchant_id = db.Column(db.BIGINT())
    # merchant_name = db.Column(db.String(50, 'utf8_unicode_ci'))
    favorite_type = db.Column(PRODUCT_TYPE)
    # title = db.Column(db.String(80, 'utf8_unicode_ci'))
    # discount_price = db.Column(db.INTEGER())
    # img_url = db.Column(db.String(120, 'utf8_unicode_ci'))
    # issue_address = db.Column(db.String(160, 'utf8_unicode_ci'))
    status = db.Column(db.Enum('common', 'del'), default="common")
    create_time = db.Column(db.INTEGER(), default=current_timestamp)


class ConfigParam(BaseModel):
    __tablename__ = 'Config_Params'

    id = db.Column(db.INTEGER(), primary_key=True)
    param_name = db.Column(db.String(120, 'utf8_unicode_ci'), nullable=False)
    set_value = db.Column(db.String(120, 'utf8_unicode_ci'), nullable=False)


class PosterResources(BaseModel):
    __tablename__ = 'Poster_Resource'
    id = db.Column(db.INTEGER(), primary_key=True)
    share_url = db.Column(db.String(160, 'utf8_unicode_ci'), nullable=False)
    activity_types = db.Column(db.Enum('bargainWithPay', 'bargain', 'groups', 'groupsWithRetail', 'fissionCoupon', 'assist',
                                       'envelopeWithRetail', 'microEnroll', 'lottery', 'assistWithPay', 'collectCard'))


class CustomerService(BaseModel):
    """客服"""
    __tablename__ = 'CustomerService'

    id = db.Column(db.BIGINT(), primary_key=True)
    merchant_id = db.Column(db.BIGINT(), comment='商户 id')
    hotline = db.Column(db.String(20, 'utf8mb4_bin'), comment='客服热线')
    url = db.Column(db.String(1024, 'utf8mb4_bin'), comment='客服二维码')
    type = db.Column(db.Enum('system', 'merchant'), default='merchant', comment='客服类型')
    status = db.Column(db.Enum('del', 'normal'), default='normal', comment='状态')
    create_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp, comment='创建时间')
    update_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp, comment='修改时间',
                            onupdate=current_timestamp)


class Effects(BaseModel):
    """特效图片"""
    __tablename__ = 'Effects'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String(50, 'utf8mb4_bin'), comment='名称')
    url = db.Column(db.String(1024, 'utf8mb4_bin'), comment='图片地址')
    number = db.Column(db.INTEGER(), nullable=False, default=0, comment='排序')
    status = db.Column(db.Enum('del', 'normal'), default='normal', comment='状态')
    create_time = db.Column(db.INTEGER(), default=current_timestamp, comment='创建时间')
    update_time = db.Column(db.INTEGER(), default=current_timestamp, comment='更新时间',
                            onupdate=current_timestamp)


class Enroll(BaseModel):
    """报名名单"""
    __tablename__ = 'Enrolls'

    id = db.Column(db.BIGINT(), primary_key=True)
    product_type = db.Column(PRODUCT_TYPE)
    activity_id = db.Column(db.BIGINT(), nullable=False, default=0)
    course_id = db.Column(db.BIGINT, default=0)
    order_id = db.Column(db.BIGINT())
    user_id = db.Column(db.BIGINT())
    nickname = db.Column(db.String(150, 'utf8mb4_bin'))
    head_url = db.Column(db.String(255, 'utf8mb4_bin'))
    full_name = db.Column(db.String(60, 'utf8mb4_bin'))  # 姓名
    telephone = db.Column(db.String(150, 'utf8mb4_bin'))  # 手机号码
    price = db.Column(db.INTEGER())
    extra = db.Column(db.JSON)  # [{"extend_name": "sex", "value": ""}]
    status = db.Column(db.Enum('unpaid', 'normal', "del"), nullable=False, server_default=db.text("'unpaid'"))
    create_time = db.Column(db.INTEGER, default=current_timestamp)
    update_time = db.Column(db.INTEGER, default=current_timestamp, onupdate=current_timestamp)


class EnrollSetting(BaseModel):
    """
    """
    __tablename__ = "Enroll_Setting"
    id = db.Column(db.BIGINT(), primary_key=True)
    merchant_id = db.Column(db.BIGINT(), index=True)
    activity_id = db.Column(db.BIGINT(), nullable=False, default=0)
    course_id = db.Column(db.BIGINT, default=0)
    extend_key = db.Column(db.String(64))
    extend_name = db.Column(db.String(50))
    must_required = db.Column(db.Enum("yes", "no"))
    create_time = db.Column(db.INTEGER, default=current_timestamp)


class FormIdStore(BaseModel):
    __tablename__ = 'FormId_Store'

    id = db.Column(db.BIGINT(), primary_key=True)
    user_id = db.Column(db.BIGINT())
    form_id = db.Column(db.String(60))
    event_type = db.Column(db.Enum('withdraw', 'pay', 'dispache'))
    open_id = db.Column(db.String(120))
    expire_time = db.Column(db.INTEGER())
    create_time = db.Column(db.INTEGER(), default=current_timestamp)


class GroupMember(BaseModel):
    __tablename__ = 'GroupMember'

    id = db.Column(db.BIGINT(), primary_key=True)
    activity_id = db.Column(db.BIGINT())
    team_id = db.Column(db.BIGINT(), nullable=False)
    user_id = db.Column(db.BIGINT(), nullable=False)
    nickname = db.Column(db.String(120, 'utf8mb4_bin'))
    head_url = db.Column(db.String(255, 'utf8mb4_bin'))
    retail_user_id = db.Column(db.BIGINT())
    retail_user_award = db.Column(db.INTEGER(), default=0)
    status = db.Column(db.Enum("normal", "del", "unpaid"), default="normal")
    create_time = db.Column(db.INTEGER(), default=current_timestamp)
    update_time = db.Column(db.INTEGER(), default=current_timestamp, onupdate=current_timestamp)


class TeamGroup(BaseModel):
    __tablename__ = 'TeamGroup'

    id = db.Column(db.BIGINT(), primary_key=True)
    activity_id = db.Column(db.BIGINT())
    chief_id = db.Column(db.BIGINT())
    chief_nickname = db.Column(db.String(120, 'utf8mb4_bin'))
    chief_headurl = db.Column(db.String(120, 'utf8mb4_bin'))
    expire_time = db.Column(db.INTEGER())
    team_limit = db.Column(db.INTEGER())
    status = db.Column(db.Enum('success', 'active', 'dead'))
    members = db.Column(db.INTEGER(), comment='已参团人数', default=0)
    group_price = db.Column(db.INTEGER())
    finish_time = db.Column(db.INTEGER())
    create_time = db.Column(db.INTEGER(), default=current_timestamp)

    @hybrid_property
    def remain(self):
        return self.team_limit - self.members

    @remain.expression
    def remain(cls):
        return cls.team_limit - cls.members


class Member(BaseModel):
    """ Merchant 会员表 """
    __tablename__ = 'Member'

    id = db.Column(db.BIGINT(), primary_key=True)
    merchant_id = db.Column(db.BIGINT(), nullable=False)
    order_id = db.Column(db.BIGINT())
    type = db.Column(db.Enum('gold', 'silver', 'diamond'), nullable=False)
    expire_time = db.Column(db.INTEGER(), nullable=False)
    create_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp)
    status = db.Column(db.Enum('expire', 'valid'), nullable=False, server_default=db.text("'valid'"))  # 基本可以忽略


class MemberPackage(BaseModel):
    """ Merchant 会员套餐 """
    __tablename__ = 'Member_Package'

    id = db.Column(db.BIGINT(), primary_key=True)
    price = db.Column(db.INTEGER(), nullable=False)
    title = db.Column(db.String(150, 'utf8mb4_bin'), comment='套餐名称')
    type = db.Column(db.Enum('gold', 'silver', 'diamond'), nullable=False)
    use_time = db.Column(db.INTEGER(), nullable=False)


class Merchant(BaseModel):
    """商户"""
    __tablename__ = 'Merchants'

    id = db.Column(db.BIGINT(), primary_key=True, comment='商家id')
    user_id = db.Column(db.BIGINT(), nullable=False)
    head_url = db.Column(db.String(255))  # 商家 logo，暂时拷贝用户头像，弹幕处用到
    name = db.Column(db.String(150, 'utf8mb4_bin'), comment='商户登陆名')
    organization_name = db.Column(db.String(150), nullable=False, comment='商家名称')
    nickname = synonym("organization_name")
    address = db.Column(db.String(200, 'utf8mb4_bin'), comment='地址')
    telephone = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    banners = db.Column(db.JSON)
    introduction = db.Column(db.Text)
    member_id = db.Column(db.BIGINT())
    industry = db.Column(db.Enum(*MERCHANT_INDUSTRY))
    company_size = db.Column(db.Enum(*MERCHANT_SIZE))
    status = db.Column(db.Enum('normal', 'black'), server_default=db.text("'normal'"))
    openid = db.Column(db.String(200), unique=False, index=True)
    access_token = db.Column(db.String(1500), unique=False, index=False)
    login_time = db.Column(db.INTEGER(), default=current_timestamp)
    remark = db.Column(db.String(500), comment='备注')
    create_time = db.Column(db.INTEGER(), default=current_timestamp, comment='注册时间')
    update_time = db.Column(db.INTEGER(), default=current_timestamp, onupdate=current_timestamp)

    def get_member(self):
        return Member.query.filter(Member.merchant_id == self.id).order_by(Member.id.desc()).first()

    def info(self):
        data = self.as_dict()
        return {field: data[field] for field in data if field not in {
            "password", "banners", "openid", "access_token", "login_time", "remark", "create_time", "update_time"
        }}

    @staticmethod
    def info_by_id(merchant_id):
        m = Merchant.query.filter_by(id=merchant_id).first()
        if not m:
            return {}
        data = m.as_dict()
        customer_service = CustomerService.query.filter(CustomerService.merchant_id == int(merchant_id)).first()
        append_data = {field: data[field] for field in data if field not in {
            "telephone", "password", "banners", "openid", "access_token", "login_time", "remark", "create_time", "update_time"
        }}
        if customer_service:
            append_data['hotline'] = customer_service.hotline
        return append_data


class Message(BaseModel):
    __tablename__ = 'Message'

    id = db.Column(db.BIGINT(), primary_key=True)
    sender_id = db.Column(db.BIGINT())
    sender_name = db.Column(db.String(60))
    receiver_id = db.Column(db.BIGINT())
    receiver_name = db.Column(db.String(60))
    content = db.Column(db.JSON)
    message_type = db.Column(db.Enum('enroll', 'notify', 'reward'))
    status = db.Column(db.Enum('readed', 'unread'))
    create_time = db.Column(db.INTEGER(), default=current_timestamp)


class Music(BaseModel):
    """背景音乐"""
    __tablename__ = 'Music'

    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String(50, 'utf8mb4_bin'), comment='音乐名称')
    url = db.Column(db.String(1024, 'utf8mb4_bin'), comment='音乐地址')
    number = db.Column(db.INTEGER(), nullable=False, default=0, comment='排序')
    status = db.Column(db.Enum('del', 'normal'), default='normal', comment='状态')
    create_time = db.Column(db.INTEGER(), default=current_timestamp, comment='创建时间')
    update_time = db.Column(db.INTEGER(), default=current_timestamp, comment='更新时间', onupdate=current_timestamp)


class Notice(BaseModel):
    __tablename__ = 'Notice'

    id = db.Column(db.BIGINT(), primary_key=True)
    title = db.Column(db.String(100, 'utf8_unicode_ci'))
    content = db.Column(db.String(1024, 'utf8_unicode_ci'))
    create_time = db.Column(db.INTEGER(), default=current_timestamp)


class Transaction(BaseModel):
    """流水"""
    __tablename__ = 'Transaction'
    id = db.Column(db.Integer, primary_key=True)
    pay_id = db.Column(db.String(64), unique=False, index=True)  # 支付订单ID
    merchant_id = db.Column(db.Integer, unique=False, index=True)  # 卖家ID
    order_no = db.Column(db.String(120), unique=True, index=True)
    amount = db.Column(db.Integer, unique=False, index=True)  # 流水金额
    type = db.Column(db.Enum('enroll', 'refund', 'withdraw', 'reward','member'), unique=False, index=False)  # 报名，退款，提现，佣金奖励
    status = db.Column(db.Enum('unsettle', 'settled'), unique=False, index=False)  # 未结算和已结算
    create_time = db.Column(db.Integer, unique=False, index=True)
    settle_time = db.Column(db.Integer, unique=False, index=True)
    settle_amount = db.Column(db.Integer, unique=False, index=True)  # 结算金额


class Orders(BaseModel):
    __tablename__ = 'Orders'

    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(80), unique=True, index=True)
    product_id = db.Column(db.Integer)   # 产品(活动)id
    merchant_id = db.Column(db.Integer)  # 商家id
    user_id = db.Column(db.Integer)     # 参与用户ID
    title = db.Column(db.String(50), unique=False, index=False)  # 名称
    prepay_id = db.Column(db.String(120), unique=False, index=False)  # 预支付id
    img_url = db.Column(db.String(150), unique=False, index=False)  # 项目缩略图url
    attach = db.Column(db.JSON)  #
    create_time = db.Column(db.Integer, unique=False, index=True)
    finish_time = db.Column(db.Integer, unique=False, index=True)
    order_amount = db.Column(db.Integer)
    price = db.Column(db.Integer)
    shares = db.Column(db.Integer)
    order_type = db.Column(db.Enum('activity', 'member', 'course'), unique=False, index=True)
    status = db.Column(db.Enum('prepay', 'canceled', 'paying', 'payed', 'refunded', 'closed', 'complete'), unique=False, index=True)

    def __repr__(self):
        pass


class Bargains(BaseModel):
    """
    砍价
    当用户参加砍价时生成
    """
    __tablename__ = 'Bargains'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer)  # 活动id
    user_id = db.Column(db.Integer)  # 参加的用户id
    price = db.Column(db.Integer)  # 现在的价
    cut_count = db.Column(db.Integer, default=0)  # 已经有多少次砍价
    create_time = db.Column(db.Integer, unique=False, default=lambda: int(time.time()))
    status = db.Column(db.Enum("finish", "start"), default="start")
    finish_time = db.Column(db.Integer, unique=False, index=True)


class BargainsItem(BaseModel):
    """
    砍价项目表
    别的用户帮参加砍价的用户砍价时生成
    """
    __tablename__ = 'Bargains_Item'
    __table_args__ = (
        db.Index('pk', 'user_id', 'bargain_id', unique=True),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # 帮砍的用户
    bargain_id = db.Column(db.BIGINT)
    activity_id = db.Column(db.Integer)  # 活动id
    price = db.Column(db.Integer)  # 砍了多少价格
    create_time = db.Column(db.Integer, unique=False, index=True, default=lambda: int(time.time()))


class Courses(BaseModel):
    """课程
    """
    __tablename__ = "Courses"
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.BIGINT, nullable=False)
    head_diagram = db.Column(db.String(255))  # 课程图片
    title = db.Column(db.String(50))  # 课程标题
    count = db.Column(db.Integer)  # 课程节数
    age_range = db.Column(AGE_RANGE)  # 适学年龄
    course_type = db.Column(COURSE_TYPE)  # 课程类别
    origin_price = db.Column(db.Integer)  # 原价
    price = db.Column(db.Integer) # 现价
    plan = db.Column(db.String(100))  # 上课安排
    describe = db.Column(db.String(200))  # 描述
    is_experience = db.Column(db.Boolean())  # 是否体验
    experience_count = db.Column(db.Integer, default=0)  # 体验节数
    experience_price = db.Column(db.Integer, default=0)  # 体验价格
    status = db.Column(db.Enum("upper", "lower"), default="upper")
    create_time = db.Column(db.Integer, unique=False, index=False, default=current_timestamp)
    update_time = db.Column(db.Integer, unique=False, index=False, default=current_timestamp,
                            onupdate=current_timestamp)


class Reservation(BaseModel):
    """预约
    """
    __tablename__ = "Reservation"
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), default="")  # 宣传图
    describe = db.Column(db.String(200), default="")  # 描述
    merchant_id = db.Column(db.Integer, unique=True)
    create_time = db.Column(db.Integer, unique=False, index=False, default=current_timestamp)


class ReservationDetail(BaseModel):
    """预约详情
    """
    __tablename__ = "Reservation_Detail"
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer)  # Reservation
    name = db.Column(db.String(100))  # 姓名
    phone = db.Column(db.String(100))  # 手机
    age_range = db.Column(AGE_RANGE)
    user_id = db.Column(db.Integer)
    courses = db.Column(db.String(200)) # 预约的课程,json格式的列表 类似 [1,2]
    remark = db.Column(db.String(500))
    create_time = db.Column(db.Integer, unique=False, index=False, default=current_timestamp)


class Comments(BaseModel):
    """评论
    """
    __tablename__ = "Comments"
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer) # 活动或者课程的id
    comment = db.Column(db.String(200))
    user_id = db.Column(db.Integer)  # 用户id
    merchant_id = db.Column(db.Integer)  # 商户id
    type = db.Column(PRODUCT_TYPE)  # 评论类型
    status = db.Column(db.Enum('pass', 'pending', 'del'))  # 待审核、通过、删除
    create_time = db.Column(db.Integer, unique=False, index=False, default=current_timestamp)


class PostAddress(BaseModel):
    __tablename__ = 'Post_Address'

    id = db.Column(db.BIGINT(), primary_key=True)
    user_id = db.Column(db.BIGINT(), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    telephone = db.Column(db.String(12), nullable=False)
    post_region = db.Column(db.String(120), nullable=False)
    detail_address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(12), nullable=False)
    create_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp)


class Refund(BaseModel):
    __tablename__ = 'Refunds'

    id = db.Column(db.BIGINT(), primary_key=True, nullable=False)
    order_no = db.Column(db.String(64), primary_key=True, nullable=False)
    out_refund_no = db.Column(db.String(64))
    order_amount = db.Column(db.INTEGER())
    refund_fee = db.Column(db.INTEGER())
    delivery = db.Column(db.JSON)
    refund_id = db.Column(db.String(64))
    create_time = db.Column(db.INTEGER(), default=current_timestamp)
    return_memo = db.Column(db.String(200))
    refund_account = db.Column(db.Enum('REFUND_SOURCE_UNSETTLED_FUNDS', 'REFUND_SOURCE_RECHARGE_FUNDS'))
    refund_success_time = db.Column(db.INTEGER())


class RetailReward(BaseModel):
    __tablename__ = 'RetailReward'

    id = db.Column(db.BIGINT(), primary_key=True)
    merchant_id = db.Column(db.BIGINT(), nullable=False)
    user_id = db.Column(db.BIGINT(), nullable=False)
    share_id = db.Column(db.BIGINT(), nullable=False)
    activity_id = db.Column(db.BIGINT(), nullable=False)
    title = db.Column(db.String(150, 'utf8mb4_bin'))
    amount = db.Column(db.INTEGER(), nullable=False)
    activity_types = db.Column(db.Enum('bargainWithPay', 'groups', 'groupsWithRetail', 'assist', 'envelopeWithRetail'))
    order_id = db.Column(db.BIGINT())
    status = db.Column(db.Enum('bereward', 'canceled', 'rewarded'))
    nickname = db.Column(db.String(150, 'utf8mb4_bin'))
    head_url = db.Column(db.String(255, 'utf8mb4_bin'))
    partner_trade_no = db.Column(db.String(120, 'utf8mb4_bin'))
    payment_no = db.Column(db.String(120, 'utf8mb4_bin'))
    finish_time = db.Column(db.INTEGER())
    create_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp)


class RewardRank(BaseModel):
    __tablename__ = 'Reward_Rank'

    id = db.Column(db.BIGINT(), primary_key=True)
    share_id = db.Column(db.BIGINT(), nullable=False)
    activity_id = db.Column(db.BIGINT(), nullable=False)
    amount = db.Column(db.INTEGER(), nullable=False)
    nickname = db.Column(db.String(150, 'utf8mb4_bin'))
    head_url = db.Column(db.String(255, 'utf8mb4_bin'))


class SubMerchant(BaseModel):
    __tablename__ = 'SubMerchant'

    id = db.Column(db.BIGINT(), primary_key=True)
    parent_id = db.Column(db.BIGINT(), nullable=False)
    sort_num = db.Column(db.INTEGER(), nullable=False)
    title = db.Column(db.String(255, 'utf8mb4_bin'), nullable=False)
    address = db.Column(db.String(255, 'utf8mb4_bin'), nullable=False)
    longitude = db.Column(db.String(60), nullable=False)
    latitude = db.Column(db.String(60), nullable=False)
    create_time = db.Column(db.INTEGER(), default=current_timestamp)
    update_time = db.Column(db.INTEGER(), default=current_timestamp, onupdate=current_timestamp)


class ShareChain(BaseModel):
    __tablename__ = 'Share_Chain'

    id = db.Column(db.BIGINT(), primary_key=True)
    share_id = db.Column(db.BIGINT(), nullable=False)
    invited_id = db.Column(db.BIGINT(), nullable=False)
    activity_id = db.Column(db.BIGINT(), nullable=False)
    activity_type = db.Column(db.Enum('bargainWithPay','bargain','groups','groupsWithRetail','fissionCoupon','assist','envelopeWithRetail','microEnroll','lottery','assistWithPay','collectCard'))
    create_time = db.Column(db.INTEGER(), default=current_timestamp)


class AssistParter(BaseModel):
    __tablename__ = 'Assist_Parter'

    id = db.Column(db.BIGINT(), primary_key=True)
    share_id = db.Column(db.BIGINT(), nullable=False)
    activity_id = db.Column(db.BIGINT(), nullable=False)
    nickname = db.Column(db.String(60), unique=False, index=False)
    head_url = db.Column(db.String(255), unique=False, index=False, comment='头像')



class Tag(BaseModel):
    __tablename__ = 'Tag'

    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String(20, 'utf8mb4_bin'), nullable=False)
    status = db.Column(db.Enum('del', 'normal'), default="normal")
    number = db.Column(db.INTEGER(), nullable=False)
    create_time = db.Column(db.INTEGER(), default=current_timestamp)
    update_time = db.Column(db.INTEGER(), default=current_timestamp, onupdate=current_timestamp)


class TemplateTag(BaseModel):
    __tablename__ = 'TemplateTag'

    id = db.Column(db.BIGINT(), primary_key=True)
    number = db.Column(db.INTEGER(), nullable=False)
    template_id = db.Column(db.BIGINT(), nullable=False)
    tag_id = db.Column(db.BIGINT(), nullable=False)
    status = db.Column(db.Enum("del", "normal"), default="normal")
    create_time = db.Column(db.INTEGER(), default=current_timestamp)
    update_time = db.Column(db.INTEGER(), default=current_timestamp, onupdate=current_timestamp)


class UserRegion(BaseModel):
    __tablename__ = 'User_Region'

    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String(30, 'utf8_unicode_ci'))
    zip_code = db.Column(db.String(10, 'utf8_unicode_ci'))
    region_level = db.Column(db.INTEGER())
    parent_id = db.Column(db.INTEGER())


class WithDraw(BaseModel):
    __tablename__ = 'With_Draw'

    id = db.Column(db.BIGINT(), primary_key=True)
    merchant_id = db.Column(db.BIGINT(), nullable=False)
    amount = db.Column(db.INTEGER(), nullable=False)
    apply_id = db.Column(db.INTEGER())
    name = db.Column(db.String(50))
    create_time = db.Column(db.INTEGER(), nullable=False, default=current_timestamp)
    withdraw_no = db.Column(db.String(64))
    telephone = db.Column(db.String(15))


class WithdrawApply(BaseModel):
    __tablename__ = 'Withdraw_Apply'

    id = db.Column(db.INTEGER(), primary_key=True)
    merchant_id = db.Column(db.INTEGER())
    fee_rate = db.Column(db.DECIMAL(10, 2))
    fee = db.Column(db.INTEGER())
    amount = db.Column(db.INTEGER())
    status = db.Column(db.Enum('apply', 'approved', 'rejected'))
    remark = db.Column(db.String(200, 'utf8mb4_bin'))  # 备注
    telephone = db.Column(db.String(15))
    withdraw_bank = db.Column(db.JSON)
    create_time = db.Column(db.INTEGER(), default=current_timestamp)
    update_time = db.Column(db.INTEGER(), default=current_timestamp, onupdate=current_timestamp)
    last_time = db.Column(db.INTEGER())


class WithdrawBank(BaseModel):
    """商家开户信息"""
    __tablename__ = 'Withdraw_Bank'
    id = db.Column(db.INTEGER(), primary_key=True)
    merchant_id = db.Column(db.INTEGER(), comment='商家id')
    bank_name = db.Column(db.String(120, 'utf8mb4_bin'), comment='所属银行')
    card_no = db.Column(db.String(64, 'utf8mb4_bin'), comment='银行卡号')
    id_no = db.Column(db.String(64, 'utf8mb4_bin'), comment='身份证号')
    real_name = db.Column(db.String(120, 'utf8mb4_bin'), comment='真实姓名')
    bank_branch = db.Column(db.String(120, 'utf8mb4_bin'), comment='开户支行')
    create_time = db.Column(db.INTEGER(), default=current_timestamp, comment='创建时间')

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name))\
                    for col in class_mapper(obj.__class__).mapped_table.c)


class MerchantDetail(BaseModel):
    """商户官网"""

    __tablename__ = 'Merchant_Detail'
    id = db.Column(db.INTEGER(), primary_key=True)
    merchant_id = db.Column(db.INTEGER(), comment='商家id')
    media_resource = db.Column(db.JSON, comment='头图(不超过5个图片或视频)')
    desc = db.Column(db.String(500, 'utf8mb4_bin'), comment='机构介绍')
    bottom_text = db.Column(db.String(50), comment='按钮文字')
    target_url = db.Column(db.JSON, comment='跳转链接')
    activity_setting = db.Column(db.JSON, comment='活动设置')
    course_setting = db.Column(db.JSON, comment='课程设置')
    create_time = db.Column(db.INTEGER(), default=current_timestamp, comment='创建时间')
    update_time = db.Column(db.INTEGER(), default=current_timestamp, comment='修改时间', onupdate=current_timestamp)


class AssistRank(BaseModel):
    """助力捞锦鲤排行"""
    __tablename__ = 'Assist_Rank'
    id = db.Column(db.INTEGER(), primary_key=True)
    share_id = db.Column(db.INTEGER(), comment='分享用户id')
    activity_id = db.Column(db.INTEGER(), comment='活动id')
    assist_count = db.Column(db.INTEGER(), comment='助力次数')
    head_url = db.Column(db.String(255), comment='头像')
    nickname = db.Column(db.String(60), comment='昵称')
    finish_time = db.Column(db.INTEGER(), comment='完成时间')

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) \
                    for col in class_mapper(obj.__class__).mapped_table.c)

# class Prize(BaseModel):
#     """
#     奖品
#     """
#
#     __tablename__ = 'Prize'
#     id = db.Column(db.INTEGER(), primary_key=True)
#     activity_id = db.Column(db.BIGINT())
#     merchant_id = db.Column(db.BIGINT())
#     award = db.Column(db.String(50))  # 奖项
#     name = db.Column(db.String(100))  # 奖品名称
#     image = db.Column(db.String(1000))  # 图片url
#     count = db.Column(db.Integer())  # 数量
#     probability = db.Column(db.Integer())  # 万分之几的概率会中奖
#     create_time = db.Column(db.INTEGER(), default=current_timestamp, comment='创建时间')


class WinningDetail(BaseModel):
    """
    中奖详情
    """
    __tablename__ = 'Winning_Detail'
    id = db.Column(db.BIGINT(), primary_key=True)
    prize_id = db.Column(db.String(32))  # Prize.id
    prize_name = db.Column(db.String(100))  # 奖品名称
    activity_id = db.Column(db.Integer())
    award = db.Column(db.String(50))  # 奖项
    user_id = db.Column(db.BIGINT)  # User.id
    nickname = db.Column(db.String(60))
    head_url = db.Column(db.String(255))
    status = db.Column(db.Enum("yes", "no"))  # 中奖状态
    create_time = db.Column(db.INTEGER(), default=current_timestamp, comment='创建时间')


class Winning(BaseModel):
    """
    参与中奖
    """
    __tablename__ = 'Winning'
    id = db.Column(db.INTEGER(), primary_key=True)
    activity_id = db.Column(db.BIGINT())
    user_id = db.Column(db.BIGINT())
    help_times = db.Column(db.Integer, default=0)  # 帮忙次数
    can_user_help_times = db.Column(db.Integer, default=0)  # keyong帮忙次数
    remaining_times = db.Column(db.Integer, default=1)  # 剩余次数
    times = db.Column(db.Integer, default=0)  # 解锁多少次
    create_time = db.Column(db.INTEGER(), default=current_timestamp, comment='创建时间')


class WinningItem(BaseModel):
    __tablename__ = "Winning_Item"
    id = db.Column(db.INTEGER(), primary_key=True)
    user_id = db.Column(db.BIGINT)
    winning_id = db.Column(db.Integer)
    create_time = db.Column(db.INTEGER(), default=current_timestamp, comment='创建时间')
