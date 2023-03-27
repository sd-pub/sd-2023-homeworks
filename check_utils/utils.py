#!/usr/bin/python3 -u
# Copyright 2020 Darius Neatu (neatudarius@gmail.com)

import sys
import resource
from datetime import datetime, timedelta

LOG_INDENT = ''


def delete_line_from_stdout():
    sys.stdout.write('\033[F')


def log(*args, **kwargs):
    global LOG_INDENT
    if len(LOG_INDENT) > 0:
        print('{}'.format(LOG_INDENT), end='')
    print(*args, **kwargs)


def log_replace(*args, **kwargs):
    delete_line_from_stdout()
    log(*args, **kwargs)


def indent_log(levels=1):
    global LOG_INDENT
    for level in range(levels):
        LOG_INDENT += '\t'


def unindent_log(levels=1):
    global LOG_INDENT
    for level in range(levels):
        LOG_INDENT = LOG_INDENT[:-1]


def bug():
    assert False, 'BUG - please send an email to neatudarius@gmail.com with the log'


def extract_stdout(process):
    return process.stdout.decode("utf-8").rstrip()


def extract_stderr(process):
    return process.stderr.decode("utf-8").rstrip()


global_mem_bytes = None


def set_mem_bytes(bytes):
    global global_mem_bytes
    global_mem_bytes = bytes


def limit_process_memory():
    if global_mem_bytes is not None:
        resource.setrlimit(resource.RLIMIT_AS,
                           (global_mem_bytes, global_mem_bytes))


def print_legend():
    log('Legend:')
    indent_log()
    log('UPS       - Ups, program crashed')
    log('TLE       - Time Limit Exceed')
    log('MLE       - Memory Limit Exceed')
    log('MEM_UPS   - Memory leaks or errors')
    log('WA        - Wrong Answer (wrong or partial output)')
    log('OK        - Everything is OK')
    log('')
    unindent_log()


def run_and_measure(func):
    start = datetime.now()
    ret = func()
    stop = datetime.now()

    return ret, (stop - start)
