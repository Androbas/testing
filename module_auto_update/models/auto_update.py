# -*- coding: utf-8 -*-

import git
import subprocess
from odoo import api, exceptions, fields, models


class AutoUpdate(models.TransientModel):
    _name = 'auto_update.update'

    modules = fields.Char(
        string='Lista de módulos',
        help='Lista sin espacios, modulos separados por coma',
        required=True
    )

    @api.multi
    def update_module(self, models=None):
        # NOTE: crear lista limpia de los modulos a actualizar
        modules_list = self.modules.split(',')
        modules_list = [mod.strip() for mod in modules_list if mod.strip() != '']

        # NOTE: verificar que los modulas a actualizar existan y esten instalados
        bad_modules = []
        for module in modules_list:
            system_module = self.env['ir.module.module'].search([('name', '=', module)])
            if system_module.state != 'installed':
                bad_modules.append(module)
            elif not system_module:
                bad_modules.append(module)

        if bad_modules:
            text = "Lo siguientes modulos no existen o no están instalados:\n"
            for module in bad_modules:
                text += "{}\n".format(module)
            raise exceptions.UserError(text)
        else:
            modules = ','.join(modules_list)

        github_config = self.env['github.config'].search([])
        if github_config:
            g = git.cmd.Git(github_config.path)
            res = g.pull()
            print(res)
            if res == "Already up-to-date.":
                raise exceptions.ValidationError("El código ya esta actualizado")

            # NOTE: update /etc/.odooconf replaces all content
            if not modules:
                raise exceptions.UserError('Debe agregar la lista de modulos a actualizar')
            f = open("/etc/.odooconf", "w")
            f.write("ARG1=--update {modules}".format(modules=modules))
            f.close()

            # NOTE: restart server
            # TODO: run the service as odoo user without the fucking password
            command = "sudo systemctl restart odooupdate"
            subprocess.run(command, shell=True)
        else:
            raise exceptions.UserError('Por favor configure los datos de conexión de Github en el menú de configuración')


class GithubConfig(models.Model):
    _name = 'github.config'

    type = fields.Selection(
        selection=[
            ('https', 'HTTPS'),
            ('ssh', 'SSH')
        ],
        string='Tipo de Conexión'
    )
    https_user = fields.Char('Mail Github')
    https_psw = fields.Char('Password Github')
    ssh = fields.Char(string='Github SSH')
    https = fields.Char(string='Github HTTPS')
    path = fields.Char(string='Path')


class ResConfigSettings(models.TransientModel):
    """Configuration for automatic update from github"""
    _inherit = 'res.config.settings'

    github_type = fields.Selection(
        selection=[
            ('https', 'HTTPS'),
            ('ssh', 'SSH')
        ],
        string='Tipo de Conexión'
    )
    github_https_user = fields.Char('Mail Github')
    github_https_psw = fields.Char('Password Github')
    github_ssh = fields.Char(
        string='Github SSH',
        help='You need to configure an ssh key in the server'
    )
    github_https = fields.Char(
        string='Github HTTPS',
        help='You need to configure an ssh key in the server'
    )
    modules_path = fields.Char('Path al repositorio')

    @api.multi
    def test_github_conecction(self):
        github_config = self.env['github.config'].search([])
        if not github_config:
            exceptions.ValidationError('Debe configurar las credenciales de Github y guardarlas')
        else:
            if github_config.type == 'ssh':
                print('ssh connect')
                connect = "ssh -T git@github.com"
                res = subprocess.run(connect, shell=True)
            elif github_config.type == 'https':
                connect = ''
                res = subprocess.run(connect, shell=True)

        print(res)

    @api.multi
    def set_values(self):
        # NOTE: guarda los valores del wizard al modelo fijo
        # NOTE: buscar parametro si exite write si no existe crear
        super(ResConfigSettings, self).set_values()
        github_config = self.env['github.config'].search([])
        vals = {
            'type': self.github_type,
            'https_user': self.github_https_user,
            'https_psw': self.github_https_psw,
            'ssh': self.github_ssh,
            'https': self.github_https,
            'path': self.modules_path
        }
        if github_config:
            github_config.write(vals)
        else:
            github_config.create(vals)

    @api.multi
    def get_values(self):
        # NOTE: Busca los valores y los devuelve al wizard de configuracion
        res = super(ResConfigSettings, self).get_values()
        github_config = self.env['github.config'].search([])
        if github_config:
            res['github_type'] = github_config.type
            res['github_https_user'] = github_config.https_user
            res['github_https_psw'] = github_config.https_psw
            res['github_ssh'] = github_config.ssh
            res['github_https'] = github_config.https
            res['modules_path'] = github_config.path
        return res
