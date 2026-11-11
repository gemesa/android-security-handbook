# https://github.com/mrphrazer/msynth/blob/dfd0f9e2cd0890658fe752aa207a2cfda2aef8d7/tests/synthesis/test_synthesizer_more.py#L84

from miasm.expression.expression import ExprId, ExprInt
from msynth import Synthesizer
from msynth.synthesis.oracle import SynthesisOracle
from msynth.synthesis.grammar import Grammar
from msynth.synthesis.mutations import Mutator

def obf(i0):
    i1 = 1
    while i1 != 0:
        i2 = i0 ^ i1
        i1 = ((i0 & i1) * 2)
        i0 = i2
    return i0

xs = [0, 1, 2, 3]

samples = {}
for x in xs:
    inputs = (ExprInt(x, 32),) # tuple
    output = ExprInt(obf(x), 32)
    samples[inputs] = output

oracle = SynthesisOracle(samples)

x = ExprId("x", 32)
grammar = Grammar(32, [x])
mutator = Mutator(grammar)

synthesizer = Synthesizer()
state, _ = synthesizer.iterated_local_search(mutator, oracle)

print(state.get_expr_simplified())
