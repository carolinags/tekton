# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from funcionario_app import funcionario_facade


def index():
    cmd = funcionario_facade.list_funcionarios_cmd()
    funcionario_list = cmd()
    funcionario_form = funcionario_facade.funcionario_form()
    funcionario_dcts = [funcionario_form.fill_with_model(m) for m in funcionario_list]
    return JsonResponse(funcionario_dcts)


def new(_resp, **funcionario_properties):
    cmd = funcionario_facade.save_funcionario_cmd(**funcionario_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **funcionario_properties):
    cmd = funcionario_facade.update_funcionario_cmd(id, **funcionario_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = funcionario_facade.delete_funcionario_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        funcionario = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    funcionario_form = funcionario_facade.funcionario_form()
    return JsonResponse(funcionario_form.fill_with_model(funcionario))

