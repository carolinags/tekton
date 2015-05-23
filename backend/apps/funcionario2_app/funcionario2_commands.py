# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from funcionario2_app.funcionario2_model import Funcionario2



class Funcionario2SaveForm(ModelForm):
    """
    Form used to save and update Funcionario2
    """
    _model_class = Funcionario2
    _include = [Funcionario2.nome, 
                Funcionario2.acesso, 
                Funcionario2.email, 
                Funcionario2.telefone, 
                Funcionario2.nascimento]


class Funcionario2Form(ModelForm):
    """
    Form used to expose Funcionario2's properties for list or json
    """
    _model_class = Funcionario2


class GetFuncionario2Command(NodeSearch):
    _model_class = Funcionario2


class DeleteFuncionario2Command(DeleteNode):
    _model_class = Funcionario2


class SaveFuncionario2Command(SaveCommand):
    _model_form_class = Funcionario2SaveForm


class UpdateFuncionario2Command(UpdateNode):
    _model_form_class = Funcionario2SaveForm


class ListFuncionario2Command(ModelSearchCommand):
    def __init__(self):
        super(ListFuncionario2Command, self).__init__(Funcionario2.query_by_creation())

