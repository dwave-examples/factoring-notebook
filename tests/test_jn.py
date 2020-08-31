# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import unittest

def run_jn(jn, timeout):
    
    open_jn = open(jn, "r", encoding='utf-8')
    notebook = nbformat.read(open_jn, nbformat.current_nbformat)
    open_jn.close()
        
    preprocessor = ExecutePreprocessor(timeout=timeout, kernel_name='python3')
    preprocessor.allow_errors = True    
    preprocessor.preprocess(notebook, {'metadata': {'path': os.path.dirname(jn)}})

    return notebook

def collect_jn_errors(nb):

    errors = []
    for cell in nb.cells:
        if 'outputs' in cell:
            for output in cell['outputs']:
                if output.output_type == 'error':
                    errors.append(output)

    return errors

def embedding_fail(error_list):
    return error_list and error_list[0].evalue == 'no embedding found'

def robust_run_jn(jn, timeout, retries):

    run_num = 1
    notebook = run_jn(jn, timeout)
    errors = collect_jn_errors(notebook)

    while embedding_fail(errors) and run_num < retries:
        run_num += 1
        notebook = run_jn(jn, timeout)
        errors = collect_jn_errors(notebook)

    return notebook, errors

def cell_text(nb, cell):
    return nb["cells"][cell]["outputs"][0]["text"]

jn_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jn_file = os.path.join(jn_dir, '01-factoring-overview.ipynb')

class TestJupyterNotebook(unittest.TestCase):
    
    def test_jn(self):
        # Smoketest
        MAX_EMBEDDING_RETRIES = 3
        MAX_RUN_TIME = 100

        nb, errors = robust_run_jn(jn_file, MAX_RUN_TIME, MAX_EMBEDDING_RETRIES)

        self.assertEqual(errors, [])

        # Test cell outputs:
        # Section Step 1: Express as a CSP with Boolean Logic, verify csp constraint
        self.assertIn("True", nb["cells"][7]["outputs"][0]["data"]['text/plain'])

        # Section Step 2: Convert to a BQM, code cell 1 (all 3-bit binary combinations)
        self.assertIn('(0, 0, 0, 0)', nb["cells"][9]["outputs"][1]["data"]['text/plain'])

        # Section Step 2: Convert to a BQM, code cell 2, print(and_bqm.quadratic)
        self.assertIn('(\'x2\', \'x3\')', cell_text(nb, 11))

        # Section Step 3: Solve By Minimization, print ExactSolver solution
        self.assertIn("8 rows", cell_text(nb, 15))

        # Section Step 1: Express Factoring as Multiplication Circuit, print binary P
        self.assertIn("010101", cell_text(nb, 19))

        # Section Step 2: Convert to a BQM, print post-fix variables
        self.assertIn("21 non-fixed variables", cell_text(nb, 27))
