#    Copyright 2018 D-Wave Systems Inc.

def to_base_ten(sample):
    a = b = 0
    
    # we know that multiplication_circuit() has created these variables
    a_vars = ['a0', 'a1', 'a2']
    b_vars = ['b0', 'b1', 'b2']
    
    for lbl in reversed(a_vars):
        a = (a << 1) | sample[lbl]
    for lbl in reversed(b_vars):
        b = (b << 1) | sample[lbl] 
        
    return a,b



