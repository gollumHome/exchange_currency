"""empty message

Revision ID: 90112bf1db3a
Revises: 
Create Date: 2019-05-23 22:43:22.759046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90112bf1db3a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Access_token',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('access_token', sa.String(length=530), nullable=False),
    sa.Column('expire_in', sa.INTEGER(), nullable=False),
    sa.Column('update_time', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Account',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('balance', sa.INTEGER(), nullable=True),
    sa.Column('unsettled', sa.INTEGER(), nullable=True),
    sa.Column('available', sa.INTEGER(), nullable=True),
    sa.Column('status', sa.Enum('common', 'black'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Activity',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('merchant_id', sa.BIGINT(), nullable=True),
    sa.Column('merchant_name', sa.String(length=150, collation='utf8mb4_bin'), nullable=False),
    sa.Column('template_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=True),
    sa.Column('title', sa.String(length=150, collation='utf8mb4_bin'), nullable=False),
    sa.Column('head_diagram', sa.JSON(), nullable=True),
    sa.Column('status', sa.Enum('finish', 'active', 'inactive'), nullable=True),
    sa.Column('original_price', sa.INTEGER(), nullable=True),
    sa.Column('discount_price', sa.INTEGER(), nullable=True),
    sa.Column('group_price', sa.INTEGER(), nullable=True),
    sa.Column('prepayment', sa.INTEGER(), nullable=True),
    sa.Column('min_size', sa.INTEGER(), nullable=True),
    sa.Column('inventory', sa.INTEGER(), nullable=False),
    sa.Column('finish_time', sa.INTEGER(), nullable=False),
    sa.Column('rules', sa.Text(), nullable=True),
    sa.Column('introduction', sa.Text(), nullable=True),
    sa.Column('music', sa.JSON(), nullable=True),
    sa.Column('effect', sa.JSON(), nullable=True),
    sa.Column('category', sa.Enum('美术', '练字', '书法', '英语', '魔方', '课外辅导', '作文', '钢琴', '舞蹈', '口才', '幼儿园', '乐高', '机器人', '编程', '跆拳道', '早教', '幼小衔接', '架子鼓', '托管', '围棋', '武术', '体育', '音乐', '其他'), server_default=sa.text("'美术'"), nullable=True),
    sa.Column('barrage', sa.Enum('close', 'active'), server_default=sa.text("'close'"), nullable=True),
    sa.Column('bargain_count', sa.INTEGER(), nullable=True),
    sa.Column('special_params', sa.JSON(), nullable=True),
    sa.Column('activity_types', sa.Enum('bargainWithPay', 'groups', 'groupsWithRetail', 'assist', 'envelopeWithRetail'), nullable=True),
    sa.Column('view_count', sa.INTEGER(), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=False),
    sa.Column('update_time', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'template_id')
    )
    op.create_table('ActivityTemplate',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.String(length=50, collation='utf8mb4_bin'), nullable=False),
    sa.Column('activity_types', sa.Enum('bargainWithPay', 'groups', 'groupsWithRetail', 'assist', 'envelopeWithRetail'), nullable=True),
    sa.Column('head_diagram', sa.String(length=1024, collation='utf8mb4_bin'), nullable=False),
    sa.Column('cover', sa.String(length=1024, collation='utf8mb4_bin'), nullable=True),
    sa.Column('background_type', sa.Enum('color', 'image'), nullable=True),
    sa.Column('background', sa.String(length=1024, collation='utf8mb4_bin'), nullable=True),
    sa.Column('introduction', sa.Text(), nullable=True),
    sa.Column('inventory', sa.INTEGER(), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('update_time', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Activity_Detail',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('activity_id', sa.BIGINT(), nullable=False),
    sa.Column('special_key', sa.JSON(), nullable=True),
    sa.Column('special_value', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Admin_User',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('nickname', sa.String(length=60, collation='utf8_bin'), nullable=True),
    sa.Column('password', sa.String(length=255, collation='utf8_bin'), nullable=True),
    sa.Column('head_url', sa.String(length=120, collation='utf8_bin'), nullable=True),
    sa.Column('access_token', sa.String(length=1500, collation='utf8_bin'), nullable=True),
    sa.Column('type', sa.Enum('common'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('update_time', sa.INTEGER(), nullable=True),
    sa.Column('login_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Advert',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('type', sa.Enum('merchant', 'activity', 'activityPopup'), nullable=True),
    sa.Column('image_url', sa.String(length=1024, collation='utf8mb4_bin'), nullable=True),
    sa.Column('target_url', sa.String(length=1024, collation='utf8mb4_bin'), nullable=True),
    sa.Column('number', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.Enum('del', 'normal'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('update_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Banner',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('img_url', sa.String(length=255, collation='utf8_unicode_ci'), nullable=False),
    sa.Column('status', sa.Enum('common', 'del'), nullable=True),
    sa.Column('welfares_id', sa.INTEGER(), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Bargains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('cut_count', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('finish', 'start'), nullable=True),
    sa.Column('finish_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Bargains_finish_time'), 'Bargains', ['finish_time'], unique=False)
    op.create_table('Bargains_Item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Bargains_Item_create_time'), 'Bargains_Item', ['create_time'], unique=False)
    op.create_index('pk', 'Bargains_Item', ['activity_id', 'user_id'], unique=True)
    op.create_table('Barrage',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('type', sa.Enum('merchant', 'user'), nullable=False),
    sa.Column('activity_id', sa.BIGINT(), nullable=True),
    sa.Column('merchant_id', sa.BIGINT(), nullable=True),
    sa.Column('user_id', sa.BIGINT(), nullable=True),
    sa.Column('content', sa.String(length=255, collation='utf8mb4_bin'), nullable=True),
    sa.Column('status', sa.Enum('del', 'normal'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Book_Subject',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('merchant_id', sa.BIGINT(), nullable=False),
    sa.Column('subject_describe', sa.String(length=120), nullable=True),
    sa.Column('subject', sa.Enum('enroll', 'service_fee', 'channel_fee', 'with_draw', 'reward', 'refund'), nullable=False),
    sa.Column('transaction_id', sa.String(length=50), nullable=False),
    sa.Column('amount', sa.INTEGER(), nullable=False),
    sa.Column('create_time', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Category',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('category_level', sa.INTEGER(), nullable=False),
    sa.Column('parent_id', sa.INTEGER(), nullable=False),
    sa.Column('img_url', sa.String(length=120), nullable=False),
    sa.Column('priority', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Channel_Pay',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('openid', sa.String(length=60), nullable=True),
    sa.Column('user_id', sa.BIGINT(), nullable=True),
    sa.Column('merchant_id', sa.BIGINT(), nullable=True),
    sa.Column('mch_id', sa.String(length=50), nullable=True),
    sa.Column('total_fee', sa.String(length=30), nullable=True),
    sa.Column('attach', sa.String(length=128), nullable=True),
    sa.Column('out_trade_no', sa.String(length=80), nullable=True),
    sa.Column('transaction_id', sa.String(length=50), nullable=True),
    sa.Column('pay_time', sa.INTEGER(), nullable=True),
    sa.Column('status', sa.Enum('success', 'paying', 'fail'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Collects',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('product_id', sa.BIGINT(), nullable=True),
    sa.Column('user_id', sa.BIGINT(), nullable=True),
    sa.Column('merchant_id', sa.BIGINT(), nullable=True),
    sa.Column('merchant_name', sa.String(length=50, collation='utf8_unicode_ci'), nullable=True),
    sa.Column('favorite_type', sa.Enum('product', 'house', 'usedcar'), nullable=True),
    sa.Column('title', sa.String(length=80, collation='utf8_unicode_ci'), nullable=True),
    sa.Column('discount_price', sa.INTEGER(), nullable=True),
    sa.Column('img_url', sa.String(length=120, collation='utf8_unicode_ci'), nullable=True),
    sa.Column('issue_address', sa.String(length=160, collation='utf8_unicode_ci'), nullable=True),
    sa.Column('status', sa.Enum('common', 'del'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=200), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.Enum('activity', 'course'), nullable=True),
    sa.Column('status', sa.Enum('pass', 'pending', 'del'), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Config_Params',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('param_name', sa.String(length=120, collation='utf8_unicode_ci'), nullable=False),
    sa.Column('set_value', sa.String(length=120, collation='utf8_unicode_ci'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('merchant_id', sa.BIGINT(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('age_range', sa.Enum('2岁-5岁', '5岁-7岁', '7岁-12岁', '12岁以上'), nullable=True),
    sa.Column('course_type', sa.Enum('美术', '练字', '书法', '英语', '魔方', '课外辅导', '作文', '钢琴', '舞蹈', '口才', '幼儿园', '乐高', '机器人', '编程', '跆拳道', '早教', '幼小衔接', '架子鼓', '托管', '围棋', '武术', '体育', '音乐', '其他'), nullable=True),
    sa.Column('origin_price', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('plan', sa.String(length=100), nullable=True),
    sa.Column('describe', sa.String(length=200), nullable=True),
    sa.Column('is_experience', sa.Boolean(), nullable=True),
    sa.Column('experience_count', sa.Integer(), nullable=True),
    sa.Column('experience_price', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('upper', 'lower'), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('CustomerService',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('hotline', sa.String(length=20, collation='utf8mb4_bin'), nullable=True),
    sa.Column('url', sa.String(length=1024, collation='utf8mb4_bin'), nullable=True),
    sa.Column('type', sa.Enum('system', 'merchant'), nullable=True),
    sa.Column('status', sa.Enum('del', 'normal'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=False),
    sa.Column('update_time', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Effects',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.String(length=50, collation='utf8mb4_bin'), nullable=True),
    sa.Column('url', sa.String(length=1024, collation='utf8mb4_bin'), nullable=True),
    sa.Column('number', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.Enum('del', 'normal'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('update_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Enroll_Setting',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('merchant_id', sa.BIGINT(), nullable=True),
    sa.Column('activity_id', sa.BIGINT(), nullable=False),
    sa.Column('extend_key', sa.String(length=64), nullable=True),
    sa.Column('extend_name', sa.String(length=50), nullable=True),
    sa.Column('must_required', sa.Enum('yes', 'no'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Enroll_Setting_merchant_id'), 'Enroll_Setting', ['merchant_id'], unique=False)
    op.create_table('Enrolls',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('product_type', sa.Enum('activity', 'course'), nullable=True),
    sa.Column('activity_id', sa.BIGINT(), nullable=False),
    sa.Column('order_id', sa.BIGINT(), nullable=True),
    sa.Column('user_id', sa.BIGINT(), nullable=True),
    sa.Column('referrer_user_id', sa.BIGINT(), nullable=True),
    sa.Column('nickname', sa.String(length=150, collation='utf8mb4_bin'), nullable=True),
    sa.Column('head_url', sa.String(length=150, collation='utf8mb4_bin'), nullable=True),
    sa.Column('full_name', sa.String(length=60, collation='utf8mb4_bin'), nullable=True),
    sa.Column('telephone', sa.String(length=150, collation='utf8mb4_bin'), nullable=True),
    sa.Column('price', sa.INTEGER(), nullable=True),
    sa.Column('extra', sa.JSON(), nullable=True),
    sa.Column('status', sa.Enum('unpaid', 'normal'), server_default=sa.text("'unpaid'"), nullable=False),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('update_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('FormId_Store',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=True),
    sa.Column('form_id', sa.String(length=60), nullable=True),
    sa.Column('event_type', sa.Enum('withdraw', 'pay', 'dispache'), nullable=True),
    sa.Column('open_id', sa.String(length=120), nullable=True),
    sa.Column('expire_time', sa.INTEGER(), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('GroupMember',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('activity_id', sa.BIGINT(), nullable=True),
    sa.Column('team_id', sa.BIGINT(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('nickname', sa.String(length=120, collation='utf8mb4_bin'), nullable=True),
    sa.Column('head_url', sa.String(length=150, collation='utf8mb4_bin'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Member',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('merchant_id', sa.BIGINT(), nullable=False),
    sa.Column('type', sa.Enum('gold', 'silver', 'diamond'), nullable=False),
    sa.Column('expire_time', sa.INTEGER(), nullable=False),
    sa.Column('create_time', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.Enum('expire', 'valid'), server_default=sa.text("'valid'"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Merchants',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('organization_name', sa.String(length=150), nullable=False),
    sa.Column('name', sa.String(length=150, collation='utf8mb4_bin'), nullable=True),
    sa.Column('address', sa.String(length=200, collation='utf8mb4_bin'), nullable=True),
    sa.Column('telephone', sa.String(length=12), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('banners', sa.JSON(), nullable=True),
    sa.Column('introduction', sa.Text(), nullable=True),
    sa.Column('member_id', sa.BIGINT(), nullable=True),
    sa.Column('industry', sa.Enum('教育培训'), nullable=True),
    sa.Column('company_size', sa.Enum('5-10人'), nullable=True),
    sa.Column('status', sa.Enum('normal', 'black'), server_default=sa.text("'normal'"), nullable=True),
    sa.Column('openid', sa.String(length=200), nullable=True),
    sa.Column('access_token', sa.String(length=1500), nullable=True),
    sa.Column('login_time', sa.INTEGER(), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('update_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Merchants_openid'), 'Merchants', ['openid'], unique=False)
    op.create_table('Message',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('sender_id', sa.BIGINT(), nullable=True),
    sa.Column('sender_name', sa.String(length=60), nullable=True),
    sa.Column('receiver_id', sa.BIGINT(), nullable=True),
    sa.Column('receiver_name', sa.String(length=60), nullable=True),
    sa.Column('content', sa.JSON(), nullable=True),
    sa.Column('message_type', sa.Enum('envelope', 'groups', 'retail'), nullable=True),
    sa.Column('status', sa.Enum('readed', 'unread'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Music',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.String(length=50, collation='utf8mb4_bin'), nullable=True),
    sa.Column('url', sa.String(length=1024, collation='utf8mb4_bin'), nullable=True),
    sa.Column('number', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.Enum('del', 'normal'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('update_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Notice',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('title', sa.String(length=100, collation='utf8_unicode_ci'), nullable=True),
    sa.Column('content', sa.String(length=1024, collation='utf8_unicode_ci'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_no', sa.String(length=80), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('merchant_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('prepay_id', sa.String(length=120), nullable=True),
    sa.Column('img_url', sa.String(length=150), nullable=True),
    sa.Column('attach', sa.String(length=255), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('order_amount', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('shares', sa.Integer(), nullable=True),
    sa.Column('order_type', sa.Enum('bargainWithPay', 'groups', 'groupsWithRetail', 'assist', 'envelopeWithRetail', 'open'), nullable=True),
    sa.Column('status', sa.Enum('prepay', 'canceled', 'paying', 'payed', 'closed', 'complete'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Orders_create_time'), 'Orders', ['create_time'], unique=False)
    op.create_index(op.f('ix_Orders_order_no'), 'Orders', ['order_no'], unique=True)
    op.create_index(op.f('ix_Orders_order_type'), 'Orders', ['order_type'], unique=False)
    op.create_index(op.f('ix_Orders_status'), 'Orders', ['status'], unique=False)
    op.create_table('Post_Address',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('telephone', sa.String(length=12), nullable=False),
    sa.Column('post_region', sa.String(length=120), nullable=False),
    sa.Column('detail_address', sa.String(length=255), nullable=False),
    sa.Column('zip_code', sa.String(length=12), nullable=False),
    sa.Column('create_time', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Refunds',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('order_no', sa.String(length=64), nullable=False),
    sa.Column('out_refund_no', sa.String(length=64), nullable=True),
    sa.Column('order_amount', sa.INTEGER(), nullable=True),
    sa.Column('refund_fee', sa.INTEGER(), nullable=True),
    sa.Column('delivery', sa.JSON(), nullable=True),
    sa.Column('refund_id', sa.String(length=64), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('return_memo', sa.String(length=200), nullable=True),
    sa.Column('refund_account', sa.Enum('REFUND_SOURCE_UNSETTLED_FUNDS', 'REFUND_SOURCE_RECHARGE_FUNDS'), nullable=True),
    sa.Column('refund_success_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'order_no')
    )
    op.create_table('Reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=150), nullable=True),
    sa.Column('describe', sa.String(length=200), nullable=True),
    sa.Column('merchant_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('merchant_id')
    )
    op.create_table('Reservation_Detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reservation_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=100), nullable=True),
    sa.Column('age_range', sa.Enum('2岁-5岁', '5岁-7岁', '7岁-12岁', '12岁以上'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('courses', sa.JSON(), nullable=True),
    sa.Column('remark', sa.String(length=500), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('RetailReward',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('user_id', sa.BIGINT(), nullable=False),
    sa.Column('share_id', sa.BIGINT(), nullable=False),
    sa.Column('activty_id', sa.BIGINT(), nullable=False),
    sa.Column('amount', sa.INTEGER(), nullable=False),
    sa.Column('activity_types', sa.Enum('bargainWithPay', 'groups', 'groupsWithRetail', 'assist', 'envelopeWithRetail'), nullable=True),
    sa.Column('order_id', sa.BIGINT(), nullable=True),
    sa.Column('nickname', sa.String(length=150, collation='utf8mb4_bin'), nullable=True),
    sa.Column('head_url', sa.String(length=120, collation='utf8mb4_bin'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Share_Chain',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('share_id', sa.BIGINT(), nullable=False),
    sa.Column('invited_id', sa.BIGINT(), nullable=False),
    sa.Column('activity_id', sa.BIGINT(), nullable=False),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('SubMerchant',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('parent_id', sa.BIGINT(), nullable=False),
    sa.Column('sort_num', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.String(length=255, collation='utf8mb4_bin'), nullable=False),
    sa.Column('address', sa.String(length=255, collation='utf8mb4_bin'), nullable=False),
    sa.Column('longitude', sa.String(length=60), nullable=False),
    sa.Column('latitude', sa.String(length=60), nullable=False),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('update_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Tag',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.String(length=20, collation='utf8mb4_bin'), nullable=False),
    sa.Column('status', sa.Enum('del', 'normal'), nullable=True),
    sa.Column('number', sa.INTEGER(), nullable=False),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('update_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('TeamGroup',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('activity_id', sa.BIGINT(), nullable=True),
    sa.Column('chief_id', sa.BIGINT(), nullable=True),
    sa.Column('chief_nickname', sa.String(length=120, collation='utf8mb4_bin'), nullable=True),
    sa.Column('chief_headurl', sa.String(length=120, collation='utf8mb4_bin'), nullable=True),
    sa.Column('expire_time', sa.INTEGER(), nullable=True),
    sa.Column('team_limit', sa.INTEGER(), nullable=True),
    sa.Column('status', sa.Enum('success', 'active', 'dead'), nullable=True),
    sa.Column('group_price', sa.INTEGER(), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Tel_VerifyCode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telephone', sa.String(length=64), nullable=True),
    sa.Column('verifyCode', sa.String(length=64), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('dead_line', sa.Integer(), nullable=True),
    sa.Column('usable', sa.Integer(), nullable=True),
    sa.Column('verify_type', sa.Enum('mch_register', 'add_phone', 'reset_pass', 'withdraw'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Tel_VerifyCode_create_time'), 'Tel_VerifyCode', ['create_time'], unique=False)
    op.create_index(op.f('ix_Tel_VerifyCode_dead_line'), 'Tel_VerifyCode', ['dead_line'], unique=False)
    op.create_index(op.f('ix_Tel_VerifyCode_telephone'), 'Tel_VerifyCode', ['telephone'], unique=True)
    op.create_index(op.f('ix_Tel_VerifyCode_verifyCode'), 'Tel_VerifyCode', ['verifyCode'], unique=False)
    op.create_index(op.f('ix_Tel_VerifyCode_verify_type'), 'Tel_VerifyCode', ['verify_type'], unique=False)
    op.create_table('TemplateTag',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('template_id', sa.BIGINT(), nullable=False),
    sa.Column('tag_id', sa.BIGINT(), nullable=False),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.Column('update_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pay_id', sa.Integer(), nullable=True),
    sa.Column('merchant_id', sa.Integer(), nullable=True),
    sa.Column('order_no', sa.String(length=120), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('type', sa.Enum('trade', 'refund', 'withdraw', 'change'), nullable=True),
    sa.Column('status', sa.Enum('unsettle', 'settled'), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('settle_time', sa.Integer(), nullable=True),
    sa.Column('settle_amount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Transaction_amount'), 'Transaction', ['amount'], unique=False)
    op.create_index(op.f('ix_Transaction_create_time'), 'Transaction', ['create_time'], unique=False)
    op.create_index(op.f('ix_Transaction_merchant_id'), 'Transaction', ['merchant_id'], unique=False)
    op.create_index(op.f('ix_Transaction_order_no'), 'Transaction', ['order_no'], unique=True)
    op.create_index(op.f('ix_Transaction_pay_id'), 'Transaction', ['pay_id'], unique=False)
    op.create_index(op.f('ix_Transaction_settle_amount'), 'Transaction', ['settle_amount'], unique=False)
    op.create_index(op.f('ix_Transaction_settle_time'), 'Transaction', ['settle_time'], unique=False)
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('openid', sa.String(length=130), nullable=True),
    sa.Column('nickname', sa.String(length=60), nullable=True),
    sa.Column('head_url', sa.String(length=80), nullable=True),
    sa.Column('telephone', sa.String(length=12), nullable=False),
    sa.Column('session_key', sa.String(length=120), nullable=True),
    sa.Column('access_token', sa.String(length=1500), nullable=True),
    sa.Column('favorite_course', sa.Enum('美术', '练字', '书法', '英语', '魔方', '课外辅导', '作文', '钢琴', '舞蹈', '口才', '幼儿园', '乐高', '机器人', '编程', '跆拳道', '早教', '幼小衔接', '架子鼓', '托管', '围棋', '武术', '体育', '音乐', '其他'), nullable=True),
    sa.Column('age_range', sa.Enum('2岁-5岁', '5岁-7岁', '7岁-12岁', '12岁以上'), nullable=True),
    sa.Column('province', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('create_time', sa.Integer(), nullable=True),
    sa.Column('expire_time', sa.Integer(), nullable=True),
    sa.Column('login_time', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('normal', 'black'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_User_create_time'), 'User', ['create_time'], unique=False)
    op.create_index(op.f('ix_User_expire_time'), 'User', ['expire_time'], unique=False)
    op.create_index(op.f('ix_User_login_time'), 'User', ['login_time'], unique=False)
    op.create_index(op.f('ix_User_openid'), 'User', ['openid'], unique=False)
    op.create_index(op.f('ix_User_status'), 'User', ['status'], unique=False)
    op.create_table('User_Region',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.String(length=30, collation='utf8_unicode_ci'), nullable=True),
    sa.Column('zip_code', sa.String(length=10, collation='utf8_unicode_ci'), nullable=True),
    sa.Column('region_level', sa.INTEGER(), nullable=True),
    sa.Column('parent_id', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('With_Draw',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('merchant_id', sa.BIGINT(), nullable=False),
    sa.Column('amount', sa.INTEGER(), nullable=False),
    sa.Column('apply_id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=False),
    sa.Column('withdraw_no', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('With_Draw_Bank',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('merchant_id', sa.INTEGER(), nullable=True),
    sa.Column('bank_name', sa.String(length=120, collation='utf8mb4_bin'), nullable=True),
    sa.Column('card_no', sa.String(length=64, collation='utf8mb4_bin'), nullable=True),
    sa.Column('id_no', sa.String(length=64, collation='utf8mb4_bin'), nullable=True),
    sa.Column('real_name', sa.String(length=120, collation='utf8mb4_bin'), nullable=True),
    sa.Column('bank_branch', sa.String(length=120, collation='utf8mb4_bin'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Withdraw_Apply',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('merchant_id', sa.INTEGER(), nullable=True),
    sa.Column('fee_rate', sa.INTEGER(), nullable=True),
    sa.Column('fee', sa.INTEGER(), nullable=True),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.Column('status', sa.Enum('apply', 'approved', 'reject'), nullable=True),
    sa.Column('remark', sa.String(length=200, collation='utf8mb4_bin'), nullable=True),
    sa.Column('create_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Withdraw_Apply')
    op.drop_table('With_Draw_Bank')
    op.drop_table('With_Draw')
    op.drop_table('User_Region')
    op.drop_index(op.f('ix_User_status'), table_name='User')
    op.drop_index(op.f('ix_User_openid'), table_name='User')
    op.drop_index(op.f('ix_User_login_time'), table_name='User')
    op.drop_index(op.f('ix_User_expire_time'), table_name='User')
    op.drop_index(op.f('ix_User_create_time'), table_name='User')
    op.drop_table('User')
    op.drop_index(op.f('ix_Transaction_settle_time'), table_name='Transaction')
    op.drop_index(op.f('ix_Transaction_settle_amount'), table_name='Transaction')
    op.drop_index(op.f('ix_Transaction_pay_id'), table_name='Transaction')
    op.drop_index(op.f('ix_Transaction_order_no'), table_name='Transaction')
    op.drop_index(op.f('ix_Transaction_merchant_id'), table_name='Transaction')
    op.drop_index(op.f('ix_Transaction_create_time'), table_name='Transaction')
    op.drop_index(op.f('ix_Transaction_amount'), table_name='Transaction')
    op.drop_table('Transaction')
    op.drop_table('TemplateTag')
    op.drop_index(op.f('ix_Tel_VerifyCode_verify_type'), table_name='Tel_VerifyCode')
    op.drop_index(op.f('ix_Tel_VerifyCode_verifyCode'), table_name='Tel_VerifyCode')
    op.drop_index(op.f('ix_Tel_VerifyCode_telephone'), table_name='Tel_VerifyCode')
    op.drop_index(op.f('ix_Tel_VerifyCode_dead_line'), table_name='Tel_VerifyCode')
    op.drop_index(op.f('ix_Tel_VerifyCode_create_time'), table_name='Tel_VerifyCode')
    op.drop_table('Tel_VerifyCode')
    op.drop_table('TeamGroup')
    op.drop_table('Tag')
    op.drop_table('SubMerchant')
    op.drop_table('Share_Chain')
    op.drop_table('RetailReward')
    op.drop_table('Reservation_Detail')
    op.drop_table('Reservation')
    op.drop_table('Refunds')
    op.drop_table('Post_Address')
    op.drop_index(op.f('ix_Orders_status'), table_name='Orders')
    op.drop_index(op.f('ix_Orders_order_type'), table_name='Orders')
    op.drop_index(op.f('ix_Orders_order_no'), table_name='Orders')
    op.drop_index(op.f('ix_Orders_create_time'), table_name='Orders')
    op.drop_table('Orders')
    op.drop_table('Notice')
    op.drop_table('Music')
    op.drop_table('Message')
    op.drop_index(op.f('ix_Merchants_openid'), table_name='Merchants')
    op.drop_table('Merchants')
    op.drop_table('Member')
    op.drop_table('GroupMember')
    op.drop_table('FormId_Store')
    op.drop_table('Enrolls')
    op.drop_index(op.f('ix_Enroll_Setting_merchant_id'), table_name='Enroll_Setting')
    op.drop_table('Enroll_Setting')
    op.drop_table('Effects')
    op.drop_table('CustomerService')
    op.drop_table('Courses')
    op.drop_table('Config_Params')
    op.drop_table('Comments')
    op.drop_table('Collects')
    op.drop_table('Channel_Pay')
    op.drop_table('Category')
    op.drop_table('Book_Subject')
    op.drop_table('Barrage')
    op.drop_index('pk', table_name='Bargains_Item')
    op.drop_index(op.f('ix_Bargains_Item_create_time'), table_name='Bargains_Item')
    op.drop_table('Bargains_Item')
    op.drop_index(op.f('ix_Bargains_finish_time'), table_name='Bargains')
    op.drop_table('Bargains')
    op.drop_table('Banner')
    op.drop_table('Advert')
    op.drop_table('Admin_User')
    op.drop_table('Activity_Detail')
    op.drop_table('ActivityTemplate')
    op.drop_table('Activity')
    op.drop_table('Account')
    op.drop_table('Access_token')
    # ### end Alembic commands ###
