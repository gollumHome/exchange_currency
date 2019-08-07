
# coding: utf-8
from sqlalchemy import Column, DECIMAL, Enum, ForeignKey, Index, JSON, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, ENUM, INTEGER, LONGTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MakerOrder(Base):
    __tablename__ = 'maker_order'

    id = Column(BIGINT(12), primary_key=True)
    book_no = Column(String(64, u'utf8mb4_bin'), nullable=False, comment=u'????')
    user_id = Column(BIGINT(12), nullable=False, comment=u'????id')
    hold_currency = Column(String(10, u'utf8mb4_bin'), nullable=False, comment=u'??')
    exchange_currency = Column(String(10, u'utf8mb4_bin'), nullable=False, comment=u'????')
    hold_amount = Column(INTEGER(11), nullable=False, comment=u'????')
    exchange_amount = Column(INTEGER(11), nullable=False, comment=u'????')
    exchange_rate = Column(DECIMAL(10, 3), nullable=False, comment=u'??')
    create_time = Column(INTEGER(11), nullable=False, comment=u'????')
    status = Column(ENUM(u' pending', u'matched', u'canceled', u'sended', u'received', u'set_wallet', u'payed', u'disputed', u'complete'), nullable=False, server_default=text("'sended'"), comment=u'????')

class TakerOrder(Base):
    __tablename__ = 'taker_order'

    id = Column(BIGINT(12), primary_key=True)
    hold_currency = Column(String(10, u'utf8mb4_bin'), nullable=False, comment=u'??')
    exchange_currency = Column(String(10, u'utf8mb4_bin'), nullable=False, comment=u'????')
    hold_amount = Column(INTEGER(11), nullable=False, comment=u'????')
    exchange_amount = Column(INTEGER(11), nullable=False, comment=u'????')
    exchange_rate = Column(DECIMAL(10, 3), nullable=False, comment=u'??')
    user_id = Column(BIGINT(12), nullable=False, comment=u'????id')
    create_time = Column(INTEGER(11), nullable=False, comment=u'????')
    status = Column(ENUM(u'canceled', u'matched', u'sended', u'received', u'set_wallet', u'payed', u'disputed', u'complete'), nullable=False, comment=u'????')
    book_no = Column(String(64, u'utf8mb4_bin'), nullable=False, comment=u'????')


class AccessToken(Base):
    __tablename__ = 'access_token'

    id = Column(BIGINT(20), primary_key=True)
    access_token = Column(String(530), nullable=False)
    expire_in = Column(INTEGER(11), nullable=False)
    update_time = Column(INTEGER(11), nullable=False)


class Account(Base):
    __tablename__ = 'account'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    balance = Column(INTEGER(11))
    unsettled = Column(INTEGER(11))
    available = Column(INTEGER(11))
    status = Column(Enum(u'common', u'black'), nullable=False)


class AdminUser(Base):
    __tablename__ = 'admin_user'

    id = Column(BIGINT(20), primary_key=True)
    nickname = Column(VARCHAR(60))
    password = Column(VARCHAR(255))
    head_url = Column(VARCHAR(255))
    access_token = Column(VARCHAR(1500))
    type = Column(Enum(u'common'))
    create_time = Column(INTEGER(11))
    update_time = Column(INTEGER(11))
    login_time = Column(INTEGER(11))


class Advert(Base):
    __tablename__ = 'advert'

    id = Column(BIGINT(20), primary_key=True)
    type = Column(Enum(u'merchant', u'activity', u'activityPopup'), comment=u'????')
    image_url = Column(VARCHAR(1024), comment=u'????')
    target_url = Column(VARCHAR(1024), comment=u'????')
    number = Column(INTEGER(11), nullable=False, comment=u'??')
    status = Column(Enum(u'del', u'normal'), comment=u'??')
    create_time = Column(INTEGER(11), comment=u'????')
    update_time = Column(INTEGER(11), comment=u'????')


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(80), nullable=False, unique=True)


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(INTEGER(11), primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DATETIME(fsp=6))
    is_superuser = Column(TINYINT(1), nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(TINYINT(1), nullable=False)
    is_active = Column(TINYINT(1), nullable=False)
    date_joined = Column(DATETIME(fsp=6), nullable=False)


class Barrage(Base):
    __tablename__ = 'barrage'

    id = Column(BIGINT(20), primary_key=True)
    type = Column(Enum(u'reward', u'exchange', u'register'), nullable=False)
    user_id = Column(BIGINT(20))
    content = Column(VARCHAR(255))
    nickname = Column(VARCHAR(120))
    head_url = Column(VARCHAR(255))
    status = Column(Enum(u'del', u'normal'))
    create_time = Column(INTEGER(11))


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(BIGINT(12), primary_key=True)
    title = Column(String(140, u'utf8mb4_bin'))
    content = Column(Text(collation=u'utf8mb4_bin'))
    status = Column(ENUM(u'del', u'normal'))
    create_time = Column(INTEGER(11))
    update_time = Column(INTEGER(11))


class BookSubject(Base):
    __tablename__ = 'book_subject'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    subject_describe = Column(JSON)
    subject = Column(Enum(u'charge', u'service_fee', u'withdraw', u'reward'), nullable=False)
    transaction_id = Column(String(50), nullable=False)
    amount = Column(INTEGER(11), nullable=False)
    create_time = Column(INTEGER(11), nullable=False)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(INTEGER(11), primary_key=True)
    activity_id = Column(BIGINT(12))
    comment = Column(String(200))
    user_id = Column(INTEGER(11))
    type = Column(Enum(u'activity', u'course', u'merchant'))
    status = Column(Enum(u'pass', u'pending', u'del'))
    create_time = Column(INTEGER(11))
    merchant_id = Column(INTEGER(11))


class ConfigParam(Base):
    __tablename__ = 'config_params'

    id = Column(INTEGER(11), primary_key=True)
    param_name = Column(VARCHAR(120), nullable=False)
    set_value = Column(VARCHAR(120), nullable=False)


class CreditCharge(Base):
    __tablename__ = 'credit_charge'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    order_id = Column(BIGINT(20))
    type = Column(Enum(u'gold', u'silver', u'diamond'))
    amount = Column(INTEGER(11), nullable=False)
    create_time = Column(INTEGER(11), nullable=False)
    status = Column(Enum(u'canceled', u'common'), nullable=False, server_default=text("'common'"))


class CreditPackage(Base):
    __tablename__ = 'credit_package'

    id = Column(BIGINT(20), primary_key=True)
    discount_price = Column(INTEGER(11), nullable=False, comment=u'???')
    title = Column(VARCHAR(150), comment=u'????')
    type = Column(Enum(u'gold', u'silver', u'diamond'), nullable=False, comment=u'????')
    original_price = Column(INTEGER(11), nullable=False, comment=u'??')
    amount = Column(INTEGER(10), comment=u'?????')


class Customerservice(Base):
    __tablename__ = 'customerservice'

    id = Column(BIGINT(20), primary_key=True)
    merchant_id = Column(BIGINT(20), comment=u'?? id')
    hotline = Column(VARCHAR(20), comment=u'????')
    url = Column(VARCHAR(1024), comment=u'?????')
    type = Column(Enum(u'system', u'merchant'), comment=u'????')
    status = Column(Enum(u'del', u'normal'), comment=u'??')
    create_time = Column(INTEGER(11), nullable=False, comment=u'????')
    update_time = Column(INTEGER(11), nullable=False, comment=u'????')


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(INTEGER(11), primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DATETIME(fsp=6), nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40), primary_key=True)
    session_data = Column(LONGTEXT, nullable=False)
    expire_date = Column(DATETIME(fsp=6), nullable=False, index=True)


class ExchangeProgres(Base):
    __tablename__ = 'exchange_progress'

    id = Column(BIGINT(12), primary_key=True)
    book_no = Column(String(64, u'utf8mb4_bin'), nullable=False, comment=u'????')
    user_id = Column(BIGINT(12), nullable=False, comment=u'??id')
    status = Column(ENUM(u'canceled', u'matched', u'sended', u'received', u'set_wallet', u'payed', u'disputed', u'complete'), nullable=False, comment=u'??')
    create_time = Column(INTEGER(11), nullable=False, comment=u'????')
    expire_time = Column(INTEGER(11), comment=u'????')
    extend_remark = Column(JSON, comment=u'??')
    entrust_type = Column(ENUM(u'maker', u'taker'))





class Message(Base):
    __tablename__ = 'message'

    id = Column(BIGINT(20), primary_key=True)
    sender_id = Column(BIGINT(20))
    sender_name = Column(String(60))
    receiver_id = Column(BIGINT(20))
    receiver_name = Column(String(60))
    content = Column(JSON)
    message_type = Column(Enum(u'enroll', u'notify', u'reward'))
    status = Column(Enum(u'readed', u'unread'))
    create_time = Column(INTEGER(11))


class Notice(Base):
    __tablename__ = 'notice'

    id = Column(BIGINT(20), primary_key=True)
    title = Column(VARCHAR(100))
    content = Column(VARCHAR(1024))
    create_time = Column(INTEGER(11))


class ShareChain(Base):
    __tablename__ = 'share_chain'
    __table_args__ = (
        Index('index_sid_uid_aid', 'share_id', 'invited_id', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    share_id = Column(BIGINT(20), nullable=False)
    invited_id = Column(BIGINT(20), nullable=False)
    create_time = Column(INTEGER(11))


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(BIGINT(20), primary_key=True)
    name = Column(VARCHAR(20), nullable=False)
    status = Column(Enum(u'del', u'normal'))
    number = Column(INTEGER(11), nullable=False)
    create_time = Column(INTEGER(11))
    update_time = Column(INTEGER(11))



class TelVerifycode(Base):
    __tablename__ = 'tel_verifycode'

    id = Column(INTEGER(11), primary_key=True)
    telephone = Column(String(64), unique=True)
    verifyCode = Column(String(64), index=True)
    create_time = Column(INTEGER(11), index=True)
    dead_line = Column(INTEGER(11), index=True)
    usable = Column(INTEGER(11))
    verify_type = Column(Enum(u'mch_register', u'add_phone', u'reset_pass', u'withdraw'), index=True)


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(INTEGER(11), primary_key=True)
    book_no = Column(String(120), unique=True)
    exchange_amount = Column(INTEGER(11))
    hold_amount = Column(INTEGER(11), index=True)
    send_wallets = Column(Enum(u'alipay', u'paypal', u'zelle', u'wxpay'))
    received_wallets = Column(Enum(u'alipay', u'paypal', u'zelle', u'wxpay'), index=True)
    user_id = Column(BIGINT(12), nullable=False)
    remark = Column(String(64))
    create_time = Column(INTEGER(11))


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(VARCHAR(120), comment=u'???')
    head_url = Column(String(255), comment=u'??')
    telephone = Column(String(12), comment=u'??')
    access_token = Column(String(1500))
    email = Column(String(120), comment=u'????')
    ID_verify = Column(JSON, comment=u'?????')
    expire_time = Column(INTEGER(11), index=True)
    login_time = Column(INTEGER(11), index=True)
    status = Column(Enum(u'normal', u'black', u'beVerified', u'rejected'), index=True)
    Passport_verify = Column(JSON, comment=u'????')
    verify_channel = Column(Enum(u'passport', u'ID'), comment=u'????')
    verify_feedback = Column(JSON, comment=u'????')
    invite_code = Column(String(32), comment=u'???')
    additional_emails = Column(String(120), comment=u'????')


class UserReward(Base):
    __tablename__ = 'user_reward'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    share_id = Column(BIGINT(20), nullable=False)
    title = Column(VARCHAR(150))
    amount = Column(INTEGER(11), nullable=False)
    order_id = Column(BIGINT(20), unique=True)
    status = Column(Enum(u'bereward', u'canceled', u'rewarded'))
    finish_time = Column(INTEGER(11))
    create_time = Column(INTEGER(11), nullable=False)


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(BIGINT(12), primary_key=True)
    cny_wallets = Column(JSON)
    usd_wallets = Column(JSON)
    cad_wallets = Column(JSON)
    gbp_wallets = Column(JSON)
    user_id = Column(BIGINT(12), nullable=False)


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    content_type_id = Column(ForeignKey(u'django_content_type.id'), nullable=False)
    codename = Column(String(100), nullable=False)

    content_type = relationship(u'DjangoContentType')


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey(u'auth_user.id'), nullable=False)
    group_id = Column(ForeignKey(u'auth_group.id'), nullable=False, index=True)

    group = relationship(u'AuthGroup')
    user = relationship(u'AuthUser')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'

    id = Column(INTEGER(11), primary_key=True)
    action_time = Column(DATETIME(fsp=6), nullable=False)
    object_id = Column(LONGTEXT)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SMALLINT(5), nullable=False)
    change_message = Column(LONGTEXT, nullable=False)
    content_type_id = Column(ForeignKey(u'django_content_type.id'), index=True)
    user_id = Column(ForeignKey(u'auth_user.id'), nullable=False, index=True)

    content_type = relationship(u'DjangoContentType')
    user = relationship(u'AuthUser')


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    group_id = Column(ForeignKey(u'auth_group.id'), nullable=False)
    permission_id = Column(ForeignKey(u'auth_permission.id'), nullable=False, index=True)

    group = relationship(u'AuthGroup')
    permission = relationship(u'AuthPermission')


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey(u'auth_user.id'), nullable=False)
    permission_id = Column(ForeignKey(u'auth_permission.id'), nullable=False, index=True)

    permission = relationship(u'AuthPermission')
    user = relationship(u'AuthUser')
