# -*- coding: utf-8 -*-

import git
import logging
import subprocess
from odoo import api, models

_logger = logging.getLogger(__name__)


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
            # NOTE: update /etc/.odooconf replaces all content
            # TODO: replace test_update,module_auto_update with variable value
            f = open("/etc/.odooconf", "w")
            f.write("ARG1=--update test_update,module_auto_update")
            f.close()

            # NOTE: restart server
            # TODO: run the service as odoo user without the fucking password

            # import pdb; pdb.set_trace()
            process = subprocess.Popen('whoami', stdout=subprocess.PIPE)
            stdout = process.communicate()[0]
            _logger.info('--------------WHOAMI----------------------')
            _logger.info('STDOUT:{}'.format(stdout))
            print('STDOUT:{}'.format(stdout))

            print('----------------------')
            print(res)
            command = "sudo systemctl restart odooupdate"
            subprocess.run(command, shell=True)
