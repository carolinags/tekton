# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from funcionario_app import funcionario_facade
from routes import funcionarios
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'funcionarios/funcionario_form.html')


def save(**funcionario_properties):
    cmd = funcionario_facade.save_funcionario_cmd(**funcionario_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'funcionario': funcionario_properties}

        return TemplateResponse(context, 'funcionarios/funcionario_form.html')
    return RedirectResponse(router.to_path(funcionarios))

