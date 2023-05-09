# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2020-present Team LibreELEC (https://libreelec.tv)

import os

import config
import os_tools


def get_hostname():
    return os_tools.read_shell_setting(config.HOSTNAME, config.OS_RELEASE['NAME'])


def set_hostname(hostname):
    # network-base.service handles user created persistent settings
    if os.path.isfile(config.HOSTNAME):
        with open(config.HOSTNAME, 'r') as input:
            current_hostname = input.read().strip()
        if current_hostname != hostname:
            with open(config.HOSTNAME, 'w') as output:
                output.write(hostname)
            os_tools.execute('systemctl restart network-base')
