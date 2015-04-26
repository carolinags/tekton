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
def index(funcionario_id):
    funcionario = funcionario_facade.get_funcionario_cmd(funcionario_id)()
    funcionario_form = funcionario_facade.funcionario_form()
    context = {'save_path': router.to_path(save, funcionario_id), 'funcionario': funcionario_form.fill_with_model(funcionario)}
    return TemplateResponse(context, 'funcionarios/funcionario_form.html')


def save(funcionario_id, **funcionario_properties):
    cmd = funcionario_facade.update_funcionario_cmd(funcionario_id, **funcionario_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'funcionario': funcionario_properties}

        return TemplateResponse(context, 'funcionarios/funcionario_form.html')
    return RedirectResponse(router.to_path(funcionarios))

