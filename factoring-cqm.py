import functools as ft
import itertools as it

from dimod import CQM, Binary
from dwave.system import LeapHybridCQMSampler


def multiplication_model(num_arg1_bits, num_arg2_bits = None):
    cqm = CQM()

    if num_arg1_bits < 1:
        raise ValueError("num_arg1_bits must be a positive integer")

    num_arg2_bits = num_arg2_bits or num_arg1_bits

    if num_arg2_bits < 1:
        raise ValueError("the arg2 must have a positive size")

    num_product_bits = num_arg1_bits + num_arg2_bits

    # throughout, we will use the following convention:
    #   i to refer to the bits of arg1
    #   j to refer to the bits of arg2

    def relabel_gate(gate, labels):
        assert len(labels) <= gate.num_variables
        return gate.relabel_variables(
            (
                dict(
                    enumerate(
                        labels
                        + tuple(
                            uuid.uuid4().hex
                            for _ in range(gate.num_variables - len(labels))
                        )
                    )
                )
            ),
            inplace=False,
        )


    def and_gate(a, b, out):
        cqm.add_constraint(a * b - out == 0, f"{a} and {b} == {out}")
 
    def half_adder(a, b, sum_in, sum_out, carry_out):
        cqm.add_constraint(a * b + sum_in - (2*carry_out + sum_out) == 0,
                           f"{a} * {b} + {sum_in} == 2*{carry_out} + {sum_out}")

    def full_adder(a, b, sum_in, carry_in, sum_out, carry_out):
        cqm.add_constraint(a * b + sum_in + carry_in - (2*carry_out + sum_out) == 0,
                           f"{a} * {b} + {sum_in} + {carry_in} == 2*{carry_out} + {sum_out}")

    constraints = dict(
        enumerate([and_gate, half_adder, full_adder], 2)
    )

    def SUM(i, j):
        return (
            f"p{i}"
            if j == 0
            else (f"p{i + j}" if i == num_arg1_bits - 1 else f"sum{i},{j}")
        )

    def CARRY(i, j):
        return (
            f"p{num_product_bits - 1}"
            if i + j == num_product_bits - 2
            else f"carry{i},{j}"
        )

    def connections(i, j):
        inputs = [f"a{i}", f"b{j}"]
        if i > 0:
            if j < num_arg2_bits - 1:
                inputs.append(SUM(i - 1, j + 1))
            elif i > 1:
                inputs.append(CARRY(i - 1, j))
            if j > 0:
                inputs.append(CARRY(i, j - 1))
        outputs = [SUM(i, j)]
        if i > 0:
            outputs.append(CARRY(i, j))
        return inputs, outputs

    for inputs, outputs in it.starmap(connections, it.product(range(num_arg1_bits), range(num_arg2_bits))):
        constraints[len(inputs)](*map(Binary, inputs+outputs))

    return cqm


def bits2int(bits):
    bits = list(bits)
    res =  ft.reduce(lambda x, y: 2 * x + y, bits, 0)
    #ic(bits, res)
    assert res == int(res)
    assert 0 <= res <= 2**len(bits)
    return res


def factor_vars(factor, sample):
    var_len = len(factor)
    res = sorted((var for var in sample.keys() if var.startswith(factor) and var[var_len:]),
                  key=lambda x: int(x[var_len:]),
                  reverse=True)
    #ic(factor, sample, res)
    return res


def factor_val(factor, sample):
    res =  bits2int(sample[v] > 0 for v in factor_vars(factor, sample))
    #ic(factor, sample, res)
    return res

#%%time
#P=35

# https://primes.utm.edu/lists/2small/0bit.html
# A = 2**32 - 5
# B = 2**32 - 17

#A = 2**10 - 3
#B = 2**10 - 5

#A = 2**8 - 5
#B = 2**8 - 15

#A = 33
#B = 47

#A=13
#B=11

A=29
B=31

P = A * B
print(A, B, P)

bP = "{0:b}".format(P)
p_vars = list(reversed([f"p{i}" for i in range(len(bP))]))
nbits1 = len(p_vars) // 2
nbits2 = len(p_vars)-nbits1
                 

# Convert P from decimal to binary
fixed_variables = dict(zip(p_vars, map(int, bP)))

cqm = multiplication_model(nbits1, nbits2)

# Fix product variables
for var, value in fixed_variables.items():
    cqm.add_constraint(Binary(var) == value, f"{var} == {value}")

sampler = LeapHybridCQMSampler()#solver="Advantage_system4.1")
# sampler = DWaveSampler(solver='Advantage_system4.1')
print(sampler.solver.name)

sampleset = sampler.sample_cqm(cqm, 60)

df = sampleset.aggregate().to_pandas_dataframe(True)
for sample in df['sample'][df.is_feasible]:
    aa, bb = (factor_val(v, sample) for v in 'ab')
    print(F"Success: {P} => {aa} * {bb} == {aa*bb}")
    
