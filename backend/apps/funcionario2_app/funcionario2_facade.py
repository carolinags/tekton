# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from funcionario2_app.funcionario2_commands import ListFuncionario2Command, SaveFuncionario2Command, UpdateFuncionario2Command, Funcionario2Form,\
    GetFuncionario2Command, DeleteFuncionario2Command


def save_funcionario2_cmd(**funcionario2_properties):
    """
    Command to save Funcionario2 entity
    :param funcionario2_properties: a dict of properties to save on model
    :return: a Command that save Funcionario2, validating and localizing properties received as strings
    """
    return SaveFuncionario2Command(**funcionario2_properties)


def update_funcionario2_cmd(funcionario2_id, **funcionario2_properties):
    """
    Command to update Funcionario2 entity with id equals 'funcionario2_id'
    :param funcionario2_properties: a dict of properties to update model
    :return: a Command that update Funcionario2, validating and localizing properties received as strings
    """
    return UpdateFuncionario2Command(funcionario2_id, **funcionario2_properties)


def list_funcionario2s_cmd():
    """
    Command to list Funcionario2 entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListFuncionario2Command()


def funcionario2_form(**kwargs):
    """
    Function to get Funcionario2's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return Funcionario2Form(**kwargs)


def get_funcionario2_cmd(funcionario2_id):
    """
    Find funcionario2 by her id
    :param funcionario2_id: the funcionario2 id
    :return: Command
    """
    return GetFuncionario2Command(funcionario2_id)



def delete_funcionario2_cmd(funcionario2_id):
    """
    Construct a command to delete a Funcionario2
    :param funcionario2_id: funcionario2's id
    :return: Command
    """
    return DeleteFuncionario2Command(funcionario2_id)

