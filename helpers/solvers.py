#    Copyright 2018 D-Wave Systems Inc.

#    Licensed under the Apache License, Version 2.0 (the "License")
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http: // www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
from IPython.display import Markdown, display

def print_markdown(string):
    display(Markdown(string))

def default_solver():
    my_default_solver = os.getenv('DWAVE_API_SOLVER')
    my_default_token  = os.getenv('DWAVE_API_TOKEN')
    if not my_default_solver or (my_default_solver == "None"):
       print_markdown("<span style='color:red;font-weight:bold'>No default solver.</span>")
       ds = False
    else:
       ds = "Solver: " + my_default_solver
       print(ds)
    if not my_default_token or (my_default_token == "None"):
       print_markdown("<span style='color:red;font-weight:bold'>No default API token.</span>")
       dt = False
    else:
       dt = "API Token: " + my_default_token[:10] + "***" + my_default_token[-5:]
       print(dt)
    if not (dt and ds):
       print("Minimal default solver configuration (solver name and API token) is not set for this environment.")
       print("Please uncomment the relevant line(s) below and paste in the missing solver name and/or token.")
       print_markdown("You can find available solver names and your API token on the <span style='font-weight:bold'>Leap dashboard</span>.")
    return(my_default_solver, my_default_token)


