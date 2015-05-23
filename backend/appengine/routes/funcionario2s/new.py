# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from funcionario2_app import funcionario2_facade
from routes import funcionario2s
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import login_required

@login_required
@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'funcionario2s/funcionario2_form.html')

@login_required
def save(**funcionario2_properties):
    cmd = funcionario2_facade.save_funcionario2_cmd(**funcionario2_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'funcionario2': funcionario2_properties}

        return TemplateResponse(context, 'funcionario2s/funcionario2_form.html')
    return RedirectResponse(router.to_path(funcionario2s))

