# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from funcionario2_app import funcionario2_facade
from routes.funcionario2s import new, edit, rest
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import login_required

@login_required
@no_csrf
def index():
    cmd = funcionario2_facade.list_funcionario2s_cmd()
    funcionario2s = cmd()
    funcionario2_form = funcionario2_facade.funcionario2_form()

    context = {'rest_new_path': router.to_path(rest.new),
               'rest_list_path': router.to_path(rest.index),
               'rest_delete_path': router.to_path(rest.delete),
               'rest_edit_path': router.to_path(rest.edit)}

    return TemplateResponse(context, 'funcionario2s/funcionario2_home.html')

@login_required
def delete(funcionario2_id):
    funcionario2_facade.delete_funcionario2_cmd(funcionario2_id)()
    return RedirectResponse(router.to_path(index))

