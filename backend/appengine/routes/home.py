# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from google.appengine.api import users
from gaepermission.decorator import login_not_required
from config.template_middleware import TemplateResponse
from routes.login import google
from tekton import router

@login_not_required
@no_csrf
def index(ret_path='/'):
    g_path = router.to_path(google.index, ret_path='/admin2')
    dct = {'login_google_path': users.create_login_url(g_path)}
    return TemplateResponse(dct)

