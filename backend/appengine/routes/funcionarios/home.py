# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from funcionario_app import funcionario_facade
from routes.funcionarios import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = funcionario_facade.list_funcionarios_cmd()
    funcionarios = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    funcionario_form = funcionario_facade.funcionario_form()

    def localize_funcionario(funcionario):
        funcionario_dct = funcionario_form.fill_with_model(funcionario)
        funcionario_dct['edit_path'] = router.to_path(edit_path, funcionario_dct['id'])
        funcionario_dct['delete_path'] = router.to_path(delete_path, funcionario_dct['id'])
        return funcionario_dct

    localized_funcionarios = [localize_funcionario(funcionario) for funcionario in funcionarios]
    context = {'funcionarios': localized_funcionarios,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'funcionarios/funcionario_home.html')


def delete(funcionario_id):
    funcionario_facade.delete_funcionario_cmd(funcionario_id)()
    return RedirectResponse(router.to_path(index))

