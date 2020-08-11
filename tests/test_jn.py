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

    errors = []
    for cell in notebook.cells:
        if 'outputs' in cell:
            for output in cell['outputs']:
                if output.output_type == 'error':
                    if output.evalue == 'no embedding found':
                        return notebook, ["Embedding failed"]
                    else:
                        errors.append(output)

    return notebook, errors

jn_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jn_file = os.path.join(jn_dir, '01-factoring-overview.ipynb')

class TestJupyterNotebook(unittest.TestCase):
    
    def test_jn(self):
        # Smoketest
        MAX_EMBEDDING_RETRIES = 3
        MAX_RUN_TIME = 100

        run_num = 1
        nb, errors = run_jn(jn_file, MAX_RUN_TIME)
        while errors == ['Embedding failed'] and run_num < MAX_EMBEDDING_RETRIES:
            run_num += 1
            nb, errors = run_jn(jn_file, MAX_RUN_TIME)

        self.assertEqual(errors, [])

        # Test cell outputs:
        # Section Step 1: Express as a CSP with Boolean Logic, verify csp constraint
        self.assertIn("True", nb["cells"][7]["outputs"][0]["data"])

        # Section Step 2: Convert to a BQM, code cell 1 (all 3-bit binary combinations)
        self.assertIn('(0, 0, 0, 0)', nb["cells"][9]["outputs"][1]["data"]['text/plain'])

        # Section Step 2: Convert to a BQM, code cell 2, print(and_bqm.quadratic)
        self.assertIn('(\'x2\', \'x3\')', nb["cells"][11]["outputs"][0]["text"])

        # Section Step 3: Solve By Minimization, print ExactSolver solution
        self.assertIn("8 rows", nb["cells"][15]["outputs"][0]["text"])

        # Section Step 1: Express Factoring as Multiplication Circuit, print binary P
        self.assertIn("010101", nb["cells"][19]["outputs"][0]["text"])

        # Section Step 2: Convert to a BQM, print post-fix variables
        self.assertIn("21 non-fixed variables", nb["cells"][27]["outputs"][0]["text"])

