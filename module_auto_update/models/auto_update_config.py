# -*- coding: utf-8 -*-

import subprocess
from odoo import api, exceptions, fields, models


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
    # _name = 'module_auto_update.config'
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
        super(ResConfigSettings, self).set_values()
        # buscar parametro
        #     si exite write
        #     si no existe crear
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
