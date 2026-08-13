from z3 import *

# ---------------------------------------------------------------------------
# Symbolic model of BoundedStack
#
# We model the stack abstractly:
#   - capacity: a positive integer, fixed at construction.
#   - size_before / size_after: integer sizes before/after an operation.
#   - Values: Int -> Int, an uninterpreted function mapping stack position
#             (0-indexed from the bottom) to the value stored there.
#
# Operations:
#   push(v): precondition size < capacity
#            size_after = size_before + 1
#            Values(size_before) = v   (new value placed at old top+1)
#
#   pop():   precondition size > 0
#            size_after = size_before - 1
#            returned value = Values(size_before - 1)  (the current top)
# ---------------------------------------------------------------------------

capacity = Int("capacity")
size = Int("size")
size_after_push = Int("size_after_push")
size_after_pop = Int("size_after_pop")
Values = Function("Values", IntSort(), IntSort())

# ---------------------------------------------------------------------------
# Invariant 1: capacity must be a positive integer (specification constraint)
# We prove: it is impossible to have a "valid construction" with capacity <= 0.
# ---------------------------------------------------------------------------
s1 = Solver()
valid_capacity = capacity > 0
# Negation: assert there exists a valid construction with capacity <= 0.
s1.add(Not(Implies(True, Implies(True, True))))  # placeholder tautology removed below

# Proper formulation: prove that capacity <= 0 and valid_capacity cannot both hold.
s1 = Solver()
s1.add(capacity <= 0)
s1.add(valid_capacity)
assert s1.check() == unsat, "Invariant 1 violated: capacity must be positive"

# ---------------------------------------------------------------------------
# Invariant 2: size is always between 0 and capacity inclusive.
# We prove: for any valid state (0 <= size <= capacity) and a push performed
# under its precondition (size < capacity), the resulting size still
# satisfies 0 <= size_after_push <= capacity.
# ---------------------------------------------------------------------------
s2 = Solver()
push_precondition = And(size >= 0, size <= capacity, capacity > 0, size < capacity)
push_effect = size_after_push == size + 1
invariant_after_push = And(size_after_push >= 0, size_after_push <= capacity)

s2.add(push_precondition)
s2.add(push_effect)
s2.add(Not(invariant_after_push))
assert s2.check() == unsat, "Invariant 2 violated: size out of bounds after push"

# ---------------------------------------------------------------------------
# Invariant 3: size after pop stays within [0, capacity], given pop's
# precondition (size > 0).
# ---------------------------------------------------------------------------
s3 = Solver()
pop_precondition = And(size >= 0, size <= capacity, capacity > 0, size > 0)
pop_effect = size_after_pop == size - 1
invariant_after_pop = And(size_after_pop >= 0, size_after_pop <= capacity)

s3.add(pop_precondition)
s3.add(pop_effect)
s3.add(Not(invariant_after_pop))
assert s3.check() == unsat, "Invariant 3 violated: size out of bounds after pop"

# ---------------------------------------------------------------------------
# Invariant 4: LIFO ordering. If we push v1 then push v2 (both under valid
# preconditions), a subsequent pop must return v2 (the most recently pushed
# value), not v1.
# ---------------------------------------------------------------------------
s4 = Solver()

size0 = Int("size0")
v1 = Int("v1")
v2 = Int("v2")

# Initial state constraints
s4.add(size0 >= 0)
s4.add(capacity > 0)

# push(v1) precondition & effect
s4.add(size0 < capacity)
size1 = size0 + 1
values_after_push1 = Values(size0) == v1  # Values updated at position size0

# push(v2) precondition & effect (only valid if size1 < capacity)
s4.add(size1 < capacity)
size2 = size1 + 1
values_after_push2 = Values(size1) == v2  # Values updated at position size1

s4.add(values_after_push1)
s4.add(values_after_push2)

# pop() after both pushes: top position is size2 - 1 = size1
pop_result = Values(size2 - 1)

# Negation: pop_result != v2 (i.e., LIFO order violated)
s4.add(Not(pop_result == v2))
assert s4.check() == unsat, "Invariant 4 violated: pop did not return most recently pushed value"

# ---------------------------------------------------------------------------
# Invariant 5: pop after a single push returns exactly the pushed value,
# and popping restores the original size (push then pop is identity on size).
# ---------------------------------------------------------------------------
s5 = Solver()

size_a = Int("size_a")
v = Int("v")

s5.add(size_a >= 0)
s5.add(capacity > 0)
s5.add(size_a < capacity)  # push precondition

size_b = size_a + 1  # after push
values_push = Values(size_a) == v

s5.add(values_push)

# pop precondition after push: size_b > 0 (always true since size_b >= 1)
size_c = size_b - 1  # after pop
popped_value = Values(size_b - 1)

s5.add(Not(And(size_c == size_a, popped_value == v)))
assert s5.check() == unsat, "Invariant 5 violated: push-then-pop must restore size and return pushed value"

print("All Z3 properties verified.")
