#!/usr/bin/python3 -u
# Copyright 2020 Darius Neatu (neatudarius@gmail.com)

import argparse
import json
import os
import pathlib
import recordclass
import sys


def assert_path(path, is_executable=False):
    assert pathlib.Path(path).is_file(), path

    if is_executable:
        assert os.access(os.path.join('.', path), os.X_OK), path


def get_test(id, tests_path, test_no, points, tests_valgrind):
    test_id = '{:02d}-{}'.format(test_no, id)

    binary = './{}'.format(id)
    in_path = '{}/{}/{}.in'.format(tests_path, test_id, test_id)
    out_path = '{}/{}/{}.out'.format(tests_path, test_id, test_id)
    ref_path = '{}/{}/{}.ref'.format(tests_path, test_id, test_id)
    deps_path = '{}/{}/env'.format(tests_path, test_id)
    log_valgrind = '{}/{}/{}.valgrind'.format(tests_path, test_id, test_id)

    assert points > 0
    assert_path(in_path)
    assert_path(ref_path)

    test_config = {
        'id': test_id,
        'test_no': test_no,
        'points': points,
        'grade': 0.0,
        'binary': os.path.abspath(binary),
        'input': os.path.abspath(in_path),
        'output': os.path.abspath(out_path),
        'ref': os.path.abspath(ref_path),
        'deps': os.path.abspath(deps_path),
        'log_valgrind': os.path.abspath(log_valgrind),
        'use_valgrind': test_no in tests_valgrind
    }

    Test = recordclass.recordclass('Test', test_config.keys())
    return Test(**test_config)


def get_task(id=None, points=None, tests_no=None, points_distribution=None, timeout=None, memory=None, use_stdin=None, use_stdout=None, use_valgrind=None, use_env_deps=None, tests_valgrind=[]):
    task_path = 'tasks/{}'.format(id)

    grader_path = '{}/grader'.format(task_path)
    assert_path(grader_path)

    tests_path = '{}/tests'.format(task_path)
    tests = []
    for test_no in range(tests_no):
        test = get_test(id, tests_path, test_no,
                        points_distribution[str(test_no)], tests_valgrind)
        assert test is not None
        tests.append(test)

    assert len(tests) == tests_no, '{} vs {}'.format(len(tests), tests_no)

    config = {
        'id': id,
        'points': points,
        'grader': os.path.abspath(grader_path),
        'binary': tests[0].binary,
        'tests': tests,
        'timeout': timeout,
        'memory': memory,
        'use_stdin': use_stdin,
        'use_stdout': use_stdout,
        'use_valgrind': use_valgrind,
        'use_env_deps': use_env_deps,

        # checker internals
        'grade': 0,
    }

    Task = recordclass.recordclass('Task', config.keys())
    return Task(**config)


def parse_config(path):
    assert_path(path)

    config = None
    print(path)
    with open(path) as f:
        config = json.load(f)

    fields = [
        'name',
        'deadline',
        'deps',
        'tasks',

        # maximum points get from running tasks
        'tests_points',

        # final grade
        'grade',

        # extra tasks
        'coding_style',

        # penalties
        'penalty_warnings',
        'penalty_readme',

        # checker internals
        'log_indent',
        'grade_vmr',
    ]

    for field in fields:
        if field not in config:
            if field in ['tests_points', 'grade', 'coding_style', ]:
                config[field] = 0
            elif field in ['warnings', 'readme', ]:
                config[field] = 5  # default 5 points penalty
            elif field in ['log_indent', ]:
                config[field] = ''
            else:
                config[field] = None

    Config = recordclass.recordclass('Config', fields)
    return Config(**config)


def apply_args(config):
    task_ids = [task['name'] for task in config.tasks]
    assert len(task_ids) > 0

    parser = argparse.ArgumentParser(description='check homework')
    parser.add_argument('--task', type=str,
                        choices=task_ids, default=None,
                        help='task name')
    parser.add_argument('--legend', type=bool,
                        choices=[True, False], default=None,
                        help='print legend')
    args = parser.parse_args()

    if args.task is not None:
        config.tasks = [
            task for task in config.tasks if task['name'] == args.task]

    if args.legend is not None and args.legend is True:
        from .utils import print_legend
        print_legend()
        sys.exit(0)


def get_config(path='./tasks/config.json'):
    config = parse_config(path)
    assert config is not None

    # global computations in config
    config.tests_points = sum([t['points'] for t in config.tasks])

    apply_args(config)

    tasks = []
    for t in config.tasks:
        id, points, tests_no = t['name'], t['points'], t['tests']
        use_stdin = t['stdin'] if 'stdin' in t else False
        use_stdout = t['stdout'] if 'stdout' in t else False
        use_valgrind = t['valgrind'] if 'valgrind' in t else False
        use_env_deps = t['env_deps'] if 'env_deps' in t else False
        tests_valgrind = t['tests_valgrind'] if 'tests_valgrind' in t else []
        timeout = t['timeout'] if 'timeout' in t else 10
        memory = t['memory'] if 'memory' in t else None

        points_distribution = t['points_distribution'] if 'points_distribution' in t else {}
        assigned = sum(
            [points for tests_no, points in points_distribution.items()])
        assigned_no = len(points_distribution.keys())

        default_test_points = 0
        if tests_no - assigned_no != 0:
            default_test_points = 1.0 * \
                (points - assigned) / (tests_no - assigned_no)

        for test_no in range(0, tests_no):
            key = str(test_no)
            if key in points_distribution:
                continue
            points_distribution[key] = default_test_points

        task = get_task(
            id=id,
            points=points,
            tests_no=tests_no,
            points_distribution=points_distribution,
            timeout=timeout,
            memory=memory,
            use_stdin=use_stdin,
            use_stdout=use_stdout,
            use_valgrind=use_valgrind,
            use_env_deps=use_env_deps,
            tests_valgrind=tests_valgrind
        )
        tasks.append(task)
    config.tasks = tasks

    return config
