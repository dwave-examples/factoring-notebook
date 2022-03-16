# Copyright 2020 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import math
import networkx as nx

def frequency_of(results):
    x_range = [str(x) for x in results.keys()]

    p = figure(x_range=x_range, plot_height=250,
               title='Frequency of samples', toolbar_location=None, tools="")
    p.vbar(x=x_range, top=list(results.values()), width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)

def energy_of(results):
    x_range = [str(x) for x in results.keys()]

    p = figure(x_range=x_range, plot_height=250,
            title='Energy of samples', toolbar_location=None, tools="")
    p.scatter(x_range, list(results.values()))

    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = math.pi/2

    show(p)
