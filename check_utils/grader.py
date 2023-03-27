#!/usr/bin/python3 -u
# Copyright 2020 Darius Neatu (neatudarius@gmail.com)

import sys


class Grader(object):
    def __init__(self, input_path, output_path, ref_path, max_points, env_path=None, ):
        super().__init__()

        # paths
        self.path = '.check.grade'
        self.input_path = input_path
        self.output_path = output_path
        self.ref_path = ref_path
        self.env_path = env_path

        # min grade == 0, max grade == max_points
        self.grade = 0

        try:
            self.max_points = float(max_points)
        except:
            exit(
                code=4, err='BUG: points is not a floating point number - {}'.format(points))

    def add_points(self, points):
        self.grade += points

    def read(self):
        # parse values from args
        try:
            with open(self.input_path) as f:
                input = f.readlines()
        except:
            self.exit(code=1, err='{} is missing'.format(self.input_path))

        print(self.output_path)
        try:
            with open(self.output_path) as f:
                output = f.readlines()
        except:
            self.exit(code=2, err='{} is missing'.format(self.output_path))

        try:
            with open(self.ref_path) as f:
                ref = f.readlines()
        except:
            self.exit(code=3, err='{} is missing'.format(self.ref_path))

        return input, output, ref

    def exit(self, code=None, err=None):
        with open(self.path, 'w') as f:
            f.writelines('{:g}\n'.format(self.grade))

        if err is not None:
            sys.stderr.write('{}\n'.format(err))
        sys.exit(code)

    def grade_test(self):
        pass

    def grade_env(self):
        pass

    def run(self):
        # grade each subtask - stop at first error
        self.grade_test()

        # exit with code 0 if all resuls are OK
        self.exit(code=0)
