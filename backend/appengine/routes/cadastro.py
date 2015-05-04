# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from time import sleep
from gaecookie.decorator import no_csrf
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node, Arc
from gaepermission.decorator import login_required
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse


@login_required
@no_csrf
def index(_logged_user):
    chave_do_usuario = _logged_user.key
    query = UsuarioArco.query(UsuarioArco.origin==chave_do_usuario)
    usuario_arco = query.fetch()
    chaves_de_funcionarios = [arco.destination for arco in usuario_arco]
    funcionario_lista = ndb.get_multi(chaves_de_funcionarios)
    funcionario_form = FuncionarioFormTable()
    funcionario_lista = [funcionario_form.fill_with_model(funcionario) for funcionario in funcionario_lista]
    editar_form_path = router.to_path(editar_form)
    delete_path = router.to_path(delete)
    for funcionario in funcionario_lista:
        funcionario['edit_path'] = '%s/%s'%(editar_form_path, funcionario['id'])
        funcionario['delete_path'] = '%s/%s'%(delete_path, funcionario['id'])
    ctx = {'funcionarios_lista': funcionario_lista,
           'form_path': router.to_path(form)}
    return TemplateResponse(ctx)

@login_required
@no_csrf
def form():
    ctx = {'save_path': router.to_path(salvar)}
    return TemplateResponse(ctx)


class Funcionario(Node):
    nome = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    telefone = ndb.StringProperty(required=True)
    nascimento = ndb.DateProperty()
    acesso = ndb.StringProperty(required=True)

class UsuarioArco(Arc):
    origin = ndb.KeyProperty(required=True)
    destination = ndb.KeyProperty(Funcionario,required=True)


class FuncionarioFormTable(ModelForm):
    _model_class = Funcionario
    _include = [Funcionario.nome, Funcionario.email, Funcionario.telefone, Funcionario.nascimento, Funcionario.acesso]


class FuncionarioForm(ModelForm):
    _model_class = Funcionario
    _include = [Funcionario.nome, Funcionario.email, Funcionario.telefone, Funcionario.nascimento, Funcionario.acesso]

@login_required
def salvar(_logged_user, **propriedades):
    func_form = FuncionarioForm(**propriedades)
    erros = func_form.validate()
    if erros:
        ctx = {'save_path': router.to_path(salvar),
               'erros': erros,
               'funcionario': func_form}
        return TemplateResponse(ctx,'cadastro/form.html')
    else:
         funcionario = func_form.fill_model()
         chave_funcionario = funcionario.put()
         chave_usuario = _logged_user.key
         usuario_arco = UsuarioArco(origin=chave_usuario, destination=chave_funcionario)
         usuario_arco.put()
         sleep(1)
         return RedirectResponse(router.to_path(index))

@login_required
@no_csrf
def editar_form(funcionario_id):
    funcionario_id = int(funcionario_id)
    funcionario = Funcionario.get_by_id(funcionario_id)
    funcionario_form = FuncionarioForm()
    funcionario_form.fill_with_model(funcionario)
    ctx = {'save_path': router.to_path(editar, funcionario_id),
           'funcionario': funcionario_form}
    return TemplateResponse(ctx,'cadastro/form.html')

@login_required
def editar(funcionario_id, **propriedades):
    funcionario_id = int(funcionario_id)
    funcionario = Funcionario.get_by_id(funcionario_id)
    func_form = FuncionarioForm(**propriedades)
    erros = func_form.validate()
    if erros:
        ctx = {'save_path': router.to_path(salvar),
               'erros': erros,
               'funcionario': func_form}
        return TemplateResponse(ctx,'cadastro/home.html')
    else:
         funcionario = func_form.fill_model(funcionario)
         funcionario.put()
         sleep(1)
         return RedirectResponse(router.to_path(index))

@login_required
def delete(funcionario_id):
    chave = ndb.Key(Funcionario, int(funcionario_id))
    chave.delete()
    sleep(1)
    return RedirectResponse(router.to_path(index))