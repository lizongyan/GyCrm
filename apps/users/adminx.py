# _*_ encoding:utf-8  _*_
import xadmin
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row
#from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from .models import UserProfile,Banner,EmailVerifyRecord
class UserProfileAdmin(UserAdmin):
    #排版重载方法
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()

class BannerAdmin(object):
    pass

class EmailVerifyRecorddmin(object):
    pass


xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecorddmin)