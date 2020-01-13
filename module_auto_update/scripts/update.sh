#!/bin/bash
cd /home/androba/odoo/odoo11/addons-testing
git pull
# aqui deberia cambiar los updates que se le pasen
# aunque deberia probar si con el service odoo restart -u 'modules' los actualiza
odoo-tests -u module_auto_update -d testing