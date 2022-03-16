# Copyright 2022 D-Wave Systems Inc.
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
import matplotlib.pyplot as plt

def energy_of(results):
    x_range = [str(x) for x in results.keys()]

    plt.figure(figsize=(12, 5))
    ax = plt.gca()
    ax.set_title("Energy of samples")
    ax.scatter(x_range, list(results.values()))
    plt.xticks(rotation=90)
    plt.show()
