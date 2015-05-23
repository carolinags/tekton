# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from time import sleep
from google.appengine.ext import ndb
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from funcionario2_app import funcionario2_facade
from funcionario2_app.funcionario2_model import UsuarioArco
from gaepermission.decorator import login_required

@login_required
def index(_logged_user):
    # cmd = funcionario2_facade.list_funcionario2s_cmd()
    # funcionario2_list = cmd()
    query = UsuarioArco.query(UsuarioArco.origin==_logged_user.key)
    usuario_arco = query.fetch()
    chaves_de_funcionarios = [arco.destination for arco in usuario_arco]
    funcionario2_list = ndb.get_multi(chaves_de_funcionarios)
    funcionario2_form = funcionario2_facade.funcionario2_form()
    funcionario2_dcts = [funcionario2_form.fill_with_model(m) for m in funcionario2_list]
    return JsonResponse(funcionario2_dcts)

@login_required
def new(_resp, _logged_user, **funcionario2_properties):
    cmd = funcionario2_facade.save_funcionario2_cmd(**funcionario2_properties)
    try:
        funcionario = cmd()
        usuario_arco = UsuarioArco(origin=_logged_user.key, destination=funcionario.key)
        usuario_arco.put()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    return _save_or_update_json_response(funcionario, _resp)

@login_required
def edit(_resp, id, **funcionario2_properties):
    cmd = funcionario2_facade.update_funcionario2_cmd(id, **funcionario2_properties)
    cmd = cmd()
    return _save_or_update_json_response(cmd, _resp)

@login_required
def delete(_resp, id):
    cmd = funcionario2_facade.delete_funcionario2_cmd(id)
    try:
        cmd()
        query = UsuarioArco.find_origins(id)
        chaves_dos_arcos = query.fetch(keys_only=True)
        ndb.delete_multi(chaves_dos_arcos)
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)

@login_required
def _save_or_update_json_response(cmd, _resp):
    funcionario2_form = funcionario2_facade.funcionario2_form()
    return JsonResponse(funcionario2_form.fill_with_model(cmd))