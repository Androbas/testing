# -*- coding: utf-8 -*-

from odoo import fields, models


class TestModel(models.Model):
    _name = 'test.model'
    _description = ' Model para probar cambios a BD en actualizacion'

    name = fields.Char('Nombre')
    description = fields.Char('Descripcion')
    calle = fields.Char('Calle')
    calle2 = fields.Char('Calle2')
    dni = fields.Char('dni')
    edad = fields.Char('Edad')
    fecha_nac = fields.Date('Fecha de Nacimiento')
