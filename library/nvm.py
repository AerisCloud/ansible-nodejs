#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE


def check_output(cmd_args):
    process = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = process.communicate()
    return process.returncode, stdout, stderr


def nvm(*args, **kwargs):
    if 'nvm_dir' in kwargs:
        nvm_dir = kwargs['nvm_dir']
    else:
        nvm_dir = '${HOME}/.nvm'

    cmd_args = [
        'bash', '-c',
        'source "{0}" && nvm {1}'.format(
            os.path.join(nvm_dir, 'nvm.sh'),
            ' '.join(list(args))
        )
    ]
    return check_output(cmd_args)


def is_installed(version, nvm_dir):
    returncode, output, _ = nvm('ls', nvm_dir=nvm_dir)
    if returncode == 3:
        return False
    for line in output.split(b'\n'):
        if line and version.encode() in line:
            return True
    return False


def main():
    arg_spec = dict(
        version=dict(default=None),
        state=dict(default='present', choices=['present', 'absent']),
        default_alias=dict(default=False, type='bool'),
        nvm_dir=dict(default='${HOME}/.nvm')
    )
    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=False
    )

    version = module.params['version']
    state = module.params['state']
    default_alias = module.params['default_alias']
    nvm_dir = module.params['nvm_dir']

    changed = False

    if state == 'present':
        if not is_installed(version, nvm_dir):
            returncode, _, stderr = nvm('install', version, nvm_dir=nvm_dir)
            if returncode != 0:
                module.fail_json(msg="Unable to install the specified "
                                     "version of nodejs. Error: %s" % stderr)
            changed = True
        if default_alias:
            _, output, _ = nvm('alias', 'default', nvm_dir=nvm_dir)
            if version.encode() not in output:
                returncode, _, stderr = nvm('alias', 'default', version,
                                         nvm_dir=nvm_dir)
                if returncode != 0:
                    module.fail_json(msg="Unable to create an alias for the "
                                         "specified version of nodejs. "
                                         "Error: %s" % stderr)
                changed = True
    elif state == 'absent':
        if is_installed(version, nvm_dir):
            returncode, _, stderr = nvm('uninstall', version, nvm_dir=nvm_dir)
            if returncode != 0:
                module.fail_json(msg="Unable to uninstall the specified "
                                     "version of nodejs. Error: %s" % stderr)
            changed = True

    ansible_facts = dict({
        'nvm_npm_path': os.path.join(nvm_dir, version, 'bin', 'npm'),
        'nvm_node_path': os.path.join(nvm_dir, version, 'bin', 'node')

    })

    module.exit_json(changed=changed, ansible_facts=ansible_facts)

# import module snippets
from ansible.module_utils.basic import *

main()
