# -*- coding: utf-8 -*-

import git
from odoo import api, models


class AutoUpdate(models.TransientModel):
    _name = 'auto_update.update'

    @api.multi
    def update_module(self, models=None):
        github_config = self.env['github.config'].search([])
        if github_config:
            g = git.cmd.Git(github_config.path)
            res = g.pull()
            print('-------------res git ---------------')
            print(res)
