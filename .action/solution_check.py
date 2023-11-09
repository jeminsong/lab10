#!/usr/bin/env python3
#
# Copyright 2021-2023 Michael Shafae
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
""" Check student's submission; requires the main file and the
    template file from the original repository. """
# pexpect documentation
#  https://pexpect.readthedocs.io/en/stable/index.html

# ex.
# .action/solution_check_p1.py  part-1 asgt

import io
import math
import sys
import os
import re
import pexpect
from assessment import csv_solution_check_make
from logger import setup_logger

import lab_config as cfg


def regex_it(s):
    combine_white_space_regex = re.compile(r"\s+")
    s = combine_white_space_regex.sub(" ", s).strip()
    s = s.replace(' ', '\\s+').replace('\n', '\\s+')
    return f'\\s*{s}\\s*'


def run_p1(binary):
    """Run part-1"""
    logger = setup_logger()
    status = []
    error_values = (
        ['Empty', 'Please provide a path to a file'], # 0 arguments, too few
        ['foobar', 'Could not open the file foobar'], # non-existant file
    )
    values = (
                ['small_file.txt', '2 13 17'],
                ['medium_file.txt', '5 157 181 373 733 1103 1223 1511 1753 3733'],
                ['large_file.txt', '5 157 181 373 733 1103 1223 1511 1753 3733 11939 19391 37199 39119 91193 93911 193939 199933 319993 331999 391939 393919 919393 939193 939391 999331 7 37 919 1657 3169 3571 7057 9241 11719 13267 16651 33391 35317'],
            )
    for index, val in enumerate(error_values):
        test_number = index + 1
        logger.info('Test %d - %s', test_number, val)
        rv = _run_p1_error(binary, val)
        if not rv:
            logger.error("Did not receive expected response for test %d.", test_number)
        status.append(rv)

    for index, val in enumerate(values):
        test_number = len(error_values) + index + 1
        logger.info('Test %d - %s', test_number, val)
        rv = _run_p1(binary, val)
        if not rv:
            logger.error("Did not receive expected response for test %d.", test_number)
        status.append(rv)
    return status

def _run_p1_error(binary, values):
    logger = setup_logger()
    status = False
    if values[0] == "Empty":
        proc = pexpect.spawn(binary, timeout=1)
    else:
        proc = pexpect.spawn(binary, timeout=1, args=[values[0]])
    # proc.logfile = sys.stdout.buffer
    values = list(map(str, values))

    with io.BytesIO() as log_stream:
        proc.logfile = log_stream
        try:
            regex = values[1].replace(' ', '\\s+')
            proc.expect(
                fr'(?i).*{regex}.*'
            )
        except (pexpect.exceptions.TIMEOUT, pexpect.exceptions.EOF) as exception:
            expected_output = values[1].replace(' ', '\n')
            logger.error(f'Expected: "{expected_output}"')
            logger.error('Could not find expected output.')
            logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
            logger.debug("%s", str(exception))
            logger.debug(str(proc))
            return status

        proc.expect(pexpect.EOF)
        proc.close()
        if proc.exitstatus == 0:
            logger.error("Expected: non-zero exit code.")
            logger.error(f'Exit code was {proc.exitstatus}.')
            logger.error("Program returned zero, but non-zero is required")
            logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
            return status
    status = True
    return status    

def _run_p1(binary, values):
    """The actual test with the expected input and output"""
    logger = setup_logger()
    status = False
    proc = pexpect.spawn(binary, timeout=1, args=[values[0]])
    # proc.logfile = sys.stdout.buffer
    values = list(map(str, values))

    with io.BytesIO() as log_stream:
        proc.logfile = log_stream
        try:
            regex = values[1].replace(' ', '\\s+')
            proc.expect(
                fr'(?i)\s*{regex}\s*'
            )
        except (pexpect.exceptions.TIMEOUT, pexpect.exceptions.EOF) as exception:
            expected_output = values[1].replace(' ', '\n')
            logger.error(f'Expected: "{expected_output}"')
            logger.error('Could not find expected output.')
            logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
            logger.debug("%s", str(exception))
            logger.debug(str(proc))
            return status

        proc.expect(pexpect.EOF)
        proc.close()
        if proc.exitstatus != 0:
            logger.error("Expected: zero exit code.")
            logger.error(f'Exit code was {proc.exitstatus}.')
            logger.error("Program returned non-zero, but zero is required")
            logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
            return status
    status = True
    return status


def run_p2(binary):
    """Run part-2"""
    logger = setup_logger()
    status = []
    error_values = (
        ['Empty', 'Please specify a county name on the command line. Exiting.'], # 0 arguments, too few
        ['foobar', 'Error: foobar is not in the vector. Please check your spelling.'], # Non-existant county
    )
    values = (
                ['Alameda', '1648556'],
                ['Alpine', '1235'],
                ['Amador', '41259'],
                ['Butte', '208309'],
                ['Calaveras', '46221'],
                ['Colusa', '21917'],
                ['Contra Costa', '1161413'],
                ['Del Norte', '28100'],
                ['El Dorado', '193221'],
                ['Fresno', '1013581'],
                ['Glenn', '28805'],
                ['Humboldt', '136310'],
                ['Imperial', '179851'],
                ['Inyo', '18970'],
                ['Kern', '917673'],
                ['Kings', '153443'],
                ['Lake', '68766'],
                ['Lassen', '33159'],
                ['Los Angeles', '9829544'],
                ['Madera', '159410'],
                ['Marin', '260206'],
                ['Mariposa', '17147'],
                ['Mendocino', '91305'],
                ['Merced', '286461'],
                ['Modoc', '8661'],
                ['Mono', '13247'],
                ['Monterey', '437325'],
                ['Napa', '136207'],
                ['Nevada', '103487'],
                ['Orange', '3167809'],
                ['Placer', '412300'],
                ['Plumas', '19915'],
                ['Riverside', '2458395'],
                ['Sacramento', '1588921'],
                ['San Benito', '66677'],
                ['San Bernardino', '2194710'],
                ['San Diego', '3286069'],
                ['San Francisco', '815201'],
                ['San Joaquin', '789410'],
                ['San Luis Obispo', '283159'],
                ['San Mateo', '737888'],
                ['Santa Barbara', '446475'],
                ['Santa Clara', '1885508'],
                ['Santa Cruz', '267792'],
                ['Shasta', '182139'],
                ['Sierra', '3283'],
                ['Siskiyou', '44118'],
                ['Solano', '451716'],
                ['Sonoma', '485887'],
                ['Stanislaus', '552999'],
                ['Sutter', '99063'],
                ['Tehama', '65498'],
                ['Trinity', '16060'],
                ['Tulare', '477054'],
                ['Tuolumne', '55810'],
                ['Ventura', '839784'],
                ['Yolo', '216986'],
                ['Yuba', '83421'],
            )
    for index, val in enumerate(error_values):
        test_number = index + 1
        logger.info('Test %d - %s', test_number, val)
        rv = _run_p1_error(binary, val)
        if not rv:
            logger.error("Did not receive expected response for test %d.", test_number)
        status.append(rv)

    for index, val in enumerate(values):
        test_number = len(error_values) + index + 1
        logger.info('Test %d - %s', test_number, val)
        rv = _run_p2(binary, val)
        if not rv:
            logger.error("Did not receive expected response for test %d.", test_number)
        status.append(rv)
    return status


def _run_p2(binary, values):
    logger = setup_logger()
    status = False
    proc = pexpect.spawn(binary, timeout=1, args=[values[0]])
    # proc.logfile = sys.stdout.buffer
    # values = list(map(str, values))

    with io.BytesIO() as log_stream:
        proc.logfile = log_stream
        expected_output = "The population of {} County is {}.".format(*values)
        try:
            regex = expected_output.replace(' ', '\\s+')
            proc.expect(
                fr'(?i).*{regex}.*'
            )
        except (pexpect.exceptions.TIMEOUT, pexpect.exceptions.EOF) as exception:
            logger.error(f'Expected: "{expected_output}"')
            logger.error('Could not find expected output.')
            logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
            logger.debug("%s", str(exception))
            logger.debug(str(proc))
            return status

        proc.expect(pexpect.EOF)
        proc.close()
        if proc.exitstatus != 0:
            logger.error("Expected: zero exit code.")
            logger.error(f'Exit code was {proc.exitstatus}.')
            logger.error("Program returned non-zero, but zero is required")
            logger.error('Your output: "%s"', log_stream.getvalue().decode('utf-8'))
            return status
    status = True
    return status


tidy_opts = (
    '-checks="*,-misc-unused-parameters,'
    '-modernize-use-trailing-return-type,-google-build-using-namespace,'
    '-cppcoreguidelines-avoid-magic-numbers,-readability-magic-numbers,'
    '-fuchsia-default-arguments-calls,-clang-analyzer-deadcode.DeadStores,'
    '-modernize-use-nodiscard,-modernize-pass-by-value,'
    '-bugprone-exception-escape,-llvm-header-guard"'
    ' -config="{CheckOptions: [{key: readability-identifier-naming.ClassCase, value: CamelCase}, '
    '{key: readability-identifier-naming.ClassMemberCase, value: lower_case}, '
    '{key: readability-identifier-naming.ConstexprVariableCase, value: CamelCase}, '
    '{key: readability-identifier-naming.ConstexprVariablePrefix, value: k}, '
    '{key: readability-identifier-naming.EnumCase, value: CamelCase}, '
    '{key: readability-identifier-naming.EnumConstantCase, value: CamelCase}, '
    '{key: readability-identifier-naming.EnumConstantPrefix, value: k}, '
    '{key: readability-identifier-naming.FunctionCase, value: CamelCase}, '
    '{key: readability-identifier-naming.GlobalConstantCase, value: CamelCase}, '
    '{key: readability-identifier-naming.GlobalConstantPrefix, value: k}, '
    '{key: readability-identifier-naming.StaticConstantCase, value: CamelCase}, '
    '{key: readability-identifier-naming.StaticConstantPrefix, value: k}, '
    '{key: readability-identifier-naming.StaticVariableCase, value: lower_case}, '
    '{key: readability-identifier-naming.MacroDefinitionCase, value: UPPER_CASE}, '
    '{key: readability-identifier-naming.MacroDefinitionIgnoredRegexp, value: \'^[A-Z]+(_[A-Z]+)*_$\'}, '
    '{key: readability-identifier-naming.MemberCase, value: lower_case}, '
    '{key: readability-identifier-naming.PrivateMemberSuffix, value: _}, '
    '{key: readability-identifier-naming.PublicMemberSuffix, value: \'\'}, '
    '{key: readability-identifier-naming.NamespaceCase, value: lower_case}, '
    '{key: readability-identifier-naming.ParameterCase, value: lower_case}, '
    '{key: readability-identifier-naming.TypeAliasCase, value: CamelCase}, '
    '{key: readability-identifier-naming.TypedefCase, value: CamelCase}, '
    '{key: readability-identifier-naming.VariableCase, value: lower_case}, '
    '{key: readability-identifier-naming.IgnoreMainLikeFunctions, value: 1}]}"'
)

if __name__ == '__main__':
    cwd = os.getcwd()
    repo_name = os.path.basename(cwd)
    td = sys.argv[1]
    # print(td)
    if sys.argv[1] == 'part-1':
        part_config = cfg.lab['parts'][0]
    elif sys.argv[1] == 'part-2':
        part_config = cfg.lab['parts'][1]
    else:
        print(f'Error: {sys.argv[0]} no match.')
        sys.exit(1)

    _program_name = part_config['target']
    _files = part_config['src'].split() + part_config['header'].split()
    _do_format_check = part_config['do_format_check']
    _do_lint_check = part_config['do_lint_check']
    _do_unit_tests = part_config['do_unit_tests']
    _tidy_options = part_config['tidy_opts']
    _skip_compile_cmd = part_config['skip_compile_cmd']
    # There needs to be some magic here to figure out which due date to use.
    _lab_due_date = cfg.lab['mon_duedate'].isoformat()
    _run_func = locals()[part_config['test_main']]

    # Execute the solution check
    csv_solution_check_make(
        csv_key=repo_name,
        target_directory=td,
        program_name=_program_name,
        run=_run_func,
        files=_files,
        do_format_check=_do_format_check,
        do_lint_check=_do_lint_check,
        do_unit_tests=_do_unit_tests,
        tidy_options=_tidy_options,
        skip_compile_cmd=_skip_compile_cmd,
        lab_due_date=_lab_due_date,
    )
