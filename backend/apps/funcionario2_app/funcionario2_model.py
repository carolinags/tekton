# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node, Arc
from gaeforms.ndb import property


class Funcionario2(Node):
    nome = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    telefone = ndb.StringProperty(required=True)
    nascimento = ndb.DateProperty(required=True)
    acesso = ndb.StringProperty(required=True)

class UsuarioArco(Arc):
    origin = ndb.KeyProperty(required=True)
    destination = ndb.KeyProperty(Funcionario2,required=True)

