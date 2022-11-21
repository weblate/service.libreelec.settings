# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2020-present Team LibreELEC (https://libreelec.tv)

'''This module holds support functions for interacting with the underlying OS.

Support functions are grouped by purpose:
1. File access: read / write / copy / move / download
2. System access: executing system commands
'''

import os
import subprocess

import log


### FILE ACCESS ###
def read_shell_setting(file, default):
    setting = default
    if os.path.isfile(file):
        with open(file) as input:
            setting = input.readline().strip()
    return setting


def read_shell_settings(file, defaults={}):
    settings = defaults
    if os.path.isfile(file):
        with open(file) as input:
            for line in input:
                name, value = line.strip().split('=', 1)
                if len(value) and value[0] in ['"', '"'] and value[0] == value[-1]:
                    value = value[1:-1]
                settings[name] = value
    return settings


### SYSTEM ACCESS ###
def execute(command, get_result=False):
    '''Run command, waiting for it to finish. Returns: command output or None'''
    log.log(f'Executing command: {command}', log.DEBUG)
    try:
        cmd_status = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        log.log(f'Command failed: {command}', log.ERROR)
        log.log(f'Executed command: {e.cmd}', log.DEBUG)
        # with shell=True, this is the shell's exit code
        log.log(f'shell exit code: {e.returncode}', log.ERROR)
        log.log(f'START COMMAND OUTPUT:\n{e.stdout.decode()}\nEND COMMAND OUTPUT', log.ERROR)
        # return None on failure. Commands that want output get nothing; remainder weren't expecting output
        return None
    except FileNotFoundError:
        # this will be whether the shell is found while shell=True
#        log.log(f'os_tools.execute: Command not found: {command.split(" ")[0]}', log.ERROR)
        log.log('os_tools.execute: Failed to find shell.', log.ERROR)
        return None
    # return output if requested, otherwise None
    return cmd_status.stdout.decode() if get_result else None
