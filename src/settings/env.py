# -*- coding: UTF-8 -*-
import os
import sys
import json


class ENVOperator(object):
    def __init__(self, env, variable_name):
        self.variable_name = variable_name

        self.env_list = (env.get(variable_name) or '').split(os.pathsep)

    def remove(self, path):
        while path in self.env_list:
            self.env_list.remove(path)

    def prepend(self, path):
        if path in self.env_list:
            self.remove(path)
        self.env_list.insert(0, path)

    def append(self, path):
        if path in self.env_list:
            self.remove(path)
        self.env_list.append(path)

    def to_command(self):
        if os.name in ['nt']:
            if len(self.env_list) == 0:
                return 'set {}='.format(self.variable_name)
            else:
                return 'set {}={}'.format(self.variable_name, os.pathsep.join(self.env_list))
        else:
            if len(self.env_list) == 0:
                return 'unset {}='.format(self.variable_name)
            else:
                return 'export {}={}'.format(self.variable_name, os.pathsep.join(self.env_list))

    def to_env(self):
        return self.variable_name, os.pathsep.join(self.env_list)


class CommandOperator(object):
    def __init__(self, system, command):
        self.system = system
        self.command = command

    def is_system_match(self):
        if os.name in ['nt']:
            if self.system in ['windows', 'nt']:
                return True


class ENVBatch(object):
    def __init__(self, ops=None):
        self.ops = ops or []
        self.env_op_dict = {}

    def add(self, operation):
        self.ops.append(operation)

    def get_env_op(self, env_key):
        if env_key in self.env_op_dict:
            env_op = self.env_op_dict[env_key]
        else:
            env_op = ENVOperator(env=os.environ, variable_name=env_key)
            self.add(env_op)
            self.env_op_dict[env_key] = env_op
        return env_op

    def __add__(self, other):
        return ENVBatch(self.ops + other)

    def to_windows(self):
        result = []
        for op in self.ops:
            if isinstance(op, ENVOperator):
                result.append(op.to_command())
            elif isinstance(op, CommandOperator):
                if op.is_system_match():
                    result.append(op.command)
        return result

    def to_list(self):
        result = []
        for op in self.ops:
            if isinstance(op, ENVOperator):
                result.append(op.to_env())
        return result

    def to_env(self):
        env_dict = dict(self.to_list())
        os.environ.update(env_dict)

        if 'PATH' in env_dict:
            sys.path = []
            sys.path.extend(env_dict['PATH'].split(os.pathsep))
        if 'PYTHONPATH' in env_dict:
            sys.path.extend(env_dict['PYTHONPATH'].split(os.pathsep))


class FilterOperator(object):
    def __init__(self, filter_obj):
        self.filter_obj = filter_obj

    def is_match(self, args):
        if self.filter_obj[1] in ['is']:
            if self.filter_obj[2] in args:
                return True
        elif self.filter_obj[1] in ['in']:
            for obj in self.filter_obj[2]:
                if obj in args:
                    return True
        return False


class FilterParse(object):
    def __init__(self, filter_obj):
        self.filter_obj = filter_obj

    def is_match(self, args):
        if not self.filter_obj:
            return True
        if isinstance(self.filter_obj[0], list):
            return all(map(lambda x: FilterOperator(x).is_match(args=args), self.filter_obj))
        else:
            return FilterOperator(self.filter_obj).is_match(args=args)


class LoadSettings(object):
    def __init__(self, settings_path, args):
        self.settings_path = settings_path
        self.json_data_list = None
        self.env_batch = ENVBatch()
        self.args = args

    def _parse_cmd(self, data):
        commands = data.get('data')
        system = data.get('system')
        if isinstance(commands, list):
            for command in commands:
                self.env_batch.add(CommandOperator(system=system, command=command))
        else:
            self.env_batch.add(CommandOperator(system=system, command=commands))

    def _parse_env(self, data):
        env_op = self.env_batch.get_env_op(env_key=data.get('env_key'))
        environments = data.get('data')
        if isinstance(environments, list):
            for env in environments:
                env_op.append(env)
        else:
            env_op.append(environments)

    @staticmethod
    def _parse_nothing(data):
        print('Can not handle this:\n{}'.format(data))

    def _parse(self):
        if not self.json_data_list:
            return

        for json_data in self.json_data_list:
            if not FilterParse(json_data.get('filter', [])).is_match(self.args):
                continue

            data_list = json_data.get('data')
            for data in data_list:
                (getattr(self, '_parse_{}'.format(data.get('type'))) or self._parse_nothing)(data=data)

    def load(self):
        with open(self.settings_path) as f:
            self.json_data_list = json.load(f)
        self._parse()
        return self.env_batch
