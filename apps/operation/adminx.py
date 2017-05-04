# _*_ encoding:utf-8  _*_

import xadmin

from .models import UserAsk,UserMessage

class UserAskAdmin(object):
    pass

class UserMessageAdmin(object):
    pass

xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserAsk,UserAskAdmin)
