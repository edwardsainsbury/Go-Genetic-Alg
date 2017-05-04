import random
import timeit

print(timeit.timeit('random.random()',setup = 'import random', number=10000))

print(timeit.timeit( 'random.SystemRandom().random()',setup ='import random',number=10000))