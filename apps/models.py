# coding: utf-8

from . import db
from sqlalchemy import Column, DECIMAL, Enum, Index, JSON, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, ENUM, INTEGER, VARCHAR


class AccessToken(db.Model):
    __tablename__ = 'Access_token'

    id = Column(BIGINT(20), primary_key=True)
    access_token = Column(String(530), nullable=False)
    expire_in = Column(INTEGER(11), nullable=False)
    update_time = Column(INTEGER(11), nullable=False)


class Account(db.Model):
    __tablename__ = 'Account'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    balance = Column(INTEGER(11))
    unsettled = Column(INTEGER(11))
    available = Column(INTEGER(11))
    status = Column(Enum('common', 'black'), nullable=False)


class AdminUser(db.Model):
    __tablename__ = 'Admin_User'

    id = Column(BIGINT(20), primary_key=True)
    nickname = Column(VARCHAR(60))
    password = Column(VARCHAR(255))
    head_url = Column(VARCHAR(255))
    access_token = Column(VARCHAR(1500))
    type = Column(Enum('common'))
    create_time = Column(INTEGER(11))
    update_time = Column(INTEGER(11))
    login_time = Column(INTEGER(11))


class Advert(db.Model):
    __tablename__ = 'Advert'

    id = Column(BIGINT(20), primary_key=True)
    type = Column(Enum('merchant', 'activity', 'activityPopup'), comment='广告类型')
    image_url = Column(VARCHAR(1024), comment='图片地址')
    target_url = Column(VARCHAR(1024), comment='跳转地址')
    number = Column(INTEGER(11), nullable=False, comment='排序')
    status = Column(Enum('del', 'normal'), comment='状态')
    create_time = Column(INTEGER(11), comment='创建时间')
    update_time = Column(INTEGER(11), comment='修改时间')


class Barrage(db.Model):
    __tablename__ = 'Barrage'

    id = Column(BIGINT(20), primary_key=True)
    type = Column(Enum('reward', 'exchange', 'register'), nullable=False)
    user_id = Column(BIGINT(20))
    content = Column(VARCHAR(255))
    nickname = Column(VARCHAR(120))
    head_url = Column(VARCHAR(255))
    status = Column(Enum('del', 'normal'))
    create_time = Column(INTEGER(11))


class Blog(db.Model):
    __tablename__ = 'Blog'

    id = Column(BIGINT(12), primary_key=True)
    title = Column(String(140, 'utf8mb4_bin'))
    content = Column(Text(collation='utf8mb4_bin'))
    status = Column(ENUM('del', 'normal'))
    create_time = Column(INTEGER(11))
    update_time = Column(INTEGER(11))


class BookSubject(db.Model):
    __tablename__ = 'Book_Subject'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    subject_describe = Column(JSON)
    subject = Column(Enum('charge', 'service_fee', 'withdraw', 'reward'), nullable=False)
    transaction_id = Column(String(50), nullable=False)
    amount = Column(INTEGER(11), nullable=False)
    create_time = Column(INTEGER(11), nullable=False)


class Comment(db.Model):
    __tablename__ = 'Comments'

    id = Column(INTEGER(11), primary_key=True)
    activity_id = Column(BIGINT(12))
    comment = Column(String(200))
    user_id = Column(INTEGER(11))
    type = Column(Enum('activity', 'course', 'merchant'))
    status = Column(Enum('pass', 'pending', 'del'))
    create_time = Column(INTEGER(11))
    merchant_id = Column(INTEGER(11))


class ConfigParam(db.Model):
    __tablename__ = 'Config_Params'

    id = Column(INTEGER(11), primary_key=True)
    param_name = Column(VARCHAR(120), nullable=False)
    set_value = Column(VARCHAR(120), nullable=False)


class CreditCharge(db.Model):
    __tablename__ = 'Credit_Charge'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    order_id = Column(BIGINT(20))
    type = Column(Enum('gold', 'silver', 'diamond'))
    amount = Column(INTEGER(11), nullable=False)
    create_time = Column(INTEGER(11), nullable=False)
    status = Column(Enum('canceled', 'common'), nullable=False, server_default=text("'common'"))


class CreditPackage(db.Model):
    __tablename__ = 'Credit_Package'

    id = Column(BIGINT(20), primary_key=True)
    discount_price = Column(INTEGER(11), nullable=False, comment='折扣价')
    title = Column(VARCHAR(150), comment='套餐名称')
    type = Column(Enum('gold', 'silver', 'diamond'), nullable=False, comment='套餐类型')
    original_price = Column(INTEGER(11), nullable=False, comment='原价')
    amount = Column(INTEGER(10), comment='信用币数量')


class CustomerService(db.Model):
    __tablename__ = 'CustomerService'

    id = Column(BIGINT(20), primary_key=True)
    merchant_id = Column(BIGINT(20), comment='商户 id')
    hotline = Column(VARCHAR(20), comment='客服热线')
    url = Column(VARCHAR(1024), comment='客服二维码')
    type = Column(Enum('system', 'merchant'), comment='客服类型')
    status = Column(Enum('del', 'normal'), comment='状态')
    create_time = Column(INTEGER(11), nullable=False, comment='创建时间')
    update_time = Column(INTEGER(11), nullable=False, comment='修改时间')


class ExchangeProgres(db.Model):
    __tablename__ = 'Exchange_Progress'

    id = Column(BIGINT(12), primary_key=True)
    book_no = Column(String(64, 'utf8mb4_bin'), nullable=False, comment='挂单编号')
    user_id = Column(BIGINT(12), nullable=False, comment='用户id')
    status = Column(ENUM('canceled', 'matched', 'sended', 'received', 'set_wallet', 'payed', 'disputed', 'complete'), nullable=False, comment='状态')
    create_time = Column(INTEGER(11), nullable=False, comment='创建时间')
    expire_time = Column(INTEGER(11), comment='过期时间')
    extend_remark = Column(JSON, comment='备注')
    entrust_type = Column(ENUM('maker', 'taker'))


class MakerOrder(db.Model):
    __tablename__ = 'Maker_Order'

    id = Column(BIGINT(12), primary_key=True)
    book_no = Column(String(64, 'utf8mb4_bin'), nullable=False, comment='挂单编号')
    user_id = Column(BIGINT(12), nullable=False, comment='挂单用户id')
    hold_currency = Column(String(10, 'utf8mb4_bin'), nullable=False, comment='本币')
    exchange_currency = Column(String(10, 'utf8mb4_bin'), nullable=False, comment='换汇货币')
    hold_amount = Column(INTEGER(11), nullable=False, comment='本币金额')
    exchange_amount = Column(INTEGER(11), nullable=False, comment='换汇金额')
    exchange_rate = Column(DECIMAL(10, 3), nullable=False, comment='汇率')
    create_time = Column(INTEGER(11), nullable=False, comment='创建时间')
    status = Column(ENUM('canceled', 'matched', 'pending', 'sended', 'received', 'set_wallet', 'payed', 'disputed',
                         'createded', 'complete'), nullable=False, comment='挂单状态')


class Message(db.Model):
    __tablename__ = 'Message'

    id = Column(BIGINT(20), primary_key=True)
    sender_id = Column(BIGINT(20))
    sender_name = Column(String(60))
    receiver_id = Column(BIGINT(20))
    receiver_name = Column(String(60))
    content = Column(JSON)
    message_type = Column(Enum('enroll', 'notify', 'reward'))
    status = Column(Enum('readed', 'unread'))
    create_time = Column(INTEGER(11))


class Notice(db.Model):
    __tablename__ = 'Notice'

    id = Column(BIGINT(20), primary_key=True)
    title = Column(VARCHAR(100))
    content = Column(VARCHAR(1024))
    create_time = Column(INTEGER(11))


class ShareChain(db.Model):
    __tablename__ = 'Share_Chain'
    __table_args__ = (
        Index('index_sid_uid_aid', 'share_id', 'invited_id', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    share_id = Column(BIGINT(20), nullable=False)
    invited_id = Column(BIGINT(20), nullable=False)
    create_time = Column(INTEGER(11))


class Tag(db.Model):
    __tablename__ = 'Tag'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(VARCHAR(20), nullable=False)
    status = Column(Enum('del', 'normal'))
    number = Column(INTEGER(11), nullable=False)
    create_time = Column(INTEGER(11))
    update_time = Column(INTEGER(11))


class TakerOrder(db.Model):
    __tablename__ = 'Taker_Order'

    id = Column(BIGINT(12), primary_key=True)
    hold_currency = Column(String(10, 'utf8mb4_bin'), nullable=False, comment='本币')
    exchange_currency = Column(String(10, 'utf8mb4_bin'), nullable=False, comment='换汇货币')
    hold_amount = Column(INTEGER(11), nullable=False, comment='本币金额')
    exchange_amount = Column(INTEGER(11), nullable=False, comment='换汇金额')
    exchange_rate = Column(DECIMAL(10, 3), nullable=False, comment='汇率')
    user_id = Column(BIGINT(12), nullable=False, comment='吃单用户id')
    create_time = Column(INTEGER(11), nullable=False, comment='创建时间')
    status = Column(ENUM('canceled', 'matched', 'sended', 'received', 'set_wallet', 'payed', 'disputed', 'complete'), nullable=False, comment='吃单状态')
    book_no = Column(String(64, 'utf8mb4_bin'), nullable=False, comment='挂单编号')


class TelVerifyCode(db.Model):
    __tablename__ = 'Tel_VerifyCode'

    id = Column(INTEGER(11), primary_key=True)
    telephone = Column(String(64), unique=True)
    verifyCode = Column(String(64), index=True)
    create_time = Column(INTEGER(11), index=True)
    dead_line = Column(INTEGER(11), index=True)
    usable = Column(INTEGER(11))
    verify_type = Column(Enum('mch_register', 'add_phone', 'reset_pass', 'withdraw'), index=True)


class Transaction(db.Model):
    __tablename__ = 'Transaction'

    id = Column(INTEGER(11), primary_key=True)
    book_no = Column(String(120), unique=True)
    exchange_amount = Column(INTEGER(11))
    hold_amount = Column(INTEGER(11), index=True)
    send_wallets = Column(Enum('alipay', 'paypal', 'zelle', 'wxpay'))
    received_wallets = Column(Enum('alipay', 'paypal', 'zelle', 'wxpay'), index=True)
    user_id = Column(BIGINT(12), nullable=False)
    remark = Column(String(64))
    create_time = Column(INTEGER(11))


class User(db.Model):
    __tablename__ = 'User'

    id = Column(INTEGER(11), primary_key=True)
    user_name = Column(VARCHAR(120), comment='用户名')
    salt = Column(VARCHAR(120), comment='HASH随机盐')
    password = Column(VARCHAR(120), comment='密码')
    head_url = Column(String(255), comment='头像')
    telephone = Column(String(12), comment='手机')
    email = Column(String(120), comment='登录邮箱')
    access_token = db.Column(db.String(1500), unique=False, index=False)
    id_verify = Column(JSON, comment='身份证认证')
    login_time = Column(INTEGER(11), index=True)
    status = Column(Enum('normal', 'black', 'beVerified', 'rejected'), index=True)
    passport_verify = Column(JSON, comment='护照认证')
    verify_channel = Column(Enum('passport', 'ID'), comment='认证类型')
    verify_feedback = Column(JSON, comment='认证结果')
    invite_code = Column(String(32), comment='邀请码')
    additional_emails = Column(String(120), comment='补充邮箱')

    @property
    def password(self):
        raise AttributeError("当前属性不可读")


class UserReward(db.Model):
    __tablename__ = 'User_Reward'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    share_id = Column(BIGINT(20), nullable=False)
    title = Column(VARCHAR(150))
    amount = Column(INTEGER(11), nullable=False)
    order_id = Column(BIGINT(20), unique=True)
    status = Column(Enum('bereward', 'canceled', 'rewarded'))
    finish_time = Column(INTEGER(11))
    create_time = Column(INTEGER(11), nullable=False)


class Wallet(db.Model):
    __tablename__ = 'Wallets'

    id = Column(BIGINT(12), primary_key=True)
    cny_wallets = Column(JSON)
    usd_wallets = Column(JSON)
    cad_wallets = Column(JSON)
    gbp_wallets = Column(JSON)
    user_id = Column(BIGINT(12), nullable=False)
