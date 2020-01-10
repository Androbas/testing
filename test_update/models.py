# -*- coding: utf-8 -*-

from odoo import fields, models


class TestModel(models.Model):
    _name = 'test.model'
    _description = ' Model para probar cambios a BD en actualizacion'

    name = fields.Char('Nombre')
