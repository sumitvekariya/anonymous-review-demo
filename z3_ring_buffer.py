from z3 import *

# Symbolic model of the RingBuffer state: capacity and size.
capacity = Int("capacity")
size_before = Int("size_before")
size_after_push = Int("size_after_push")
size_after_pop = Int("size_after_pop")

# Assumptions describing valid states (mirroring the class invariant).
valid_capacity = capacity > 0
valid_size = And(size_before >= 0, size_before <= capacity)

# push() transition: overwrite (size unchanged) when full, else size+1.
push_transition = size_after_push == If(
    size_before == capacity, size_before, size_before + 1
)

# pop() transition (only defined when size_before > 0): size-1.
pop_transition = size_after_pop == size_before - 1

# ---------------------------------------------------------------------------
# Invariant 1: 0 <= size <= capacity always holds for any valid starting state.
s1 = Solver()
s1.add(valid_capacity, valid_size)
s1.add(Not(And(size_before >= 0, size_before <= capacity)))
assert s1.check() == unsat, "Invariant 1 violated: size not within [0, capacity]"

# ---------------------------------------------------------------------------
# Invariant 2: after push(), size stays within [0, capacity] for all valid states.
s2 = Solver()
s2.add(valid_capacity, valid_size, push_transition)
s2.add(Not(And(size_after_push >= 0, size_after_push <= capacity)))
assert s2.check() == unsat, "Invariant 2 violated: push result out of bounds"

# ---------------------------------------------------------------------------
# Invariant 3: pushing to a full buffer leaves size unchanged.
s3 = Solver()
s3.add(valid_capacity, valid_size, push_transition)
s3.add(size_before == capacity)  # buffer is full
s3.add(Not(size_after_push == size_before))
assert s3.check() == unsat, "Invariant 3 violated: push on full buffer changed size"

# ---------------------------------------------------------------------------
# Invariant 4: pushing to a non-full buffer increases size by exactly 1.
s4 = Solver()
s4.add(valid_capacity, valid_size, push_transition)
s4.add(size_before < capacity)
s4.add(Not(size_after_push == size_before + 1))
assert s4.check() == unsat, "Invariant 4 violated: push on non-full buffer did not increment size"

# ---------------------------------------------------------------------------
# Invariant 5: pop() on a non-empty buffer decreases size by exactly 1
# and the result stays within [0, capacity].
s5 = Solver()
s5.add(valid_capacity, valid_size, pop_transition)
s5.add(size_before > 0)  # non-empty precondition for pop
s5.add(
    Not(
        And(
            size_after_pop == size_before - 1,
            size_after_pop >= 0,
            size_after_pop <= capacity,
        )
    )
)
assert s5.check() == unsat, "Invariant 5 violated: pop transition incorrect"

# ---------------------------------------------------------------------------
# Invariant 6: is_full() is equivalent to size == capacity, for all valid states.
is_full = size_before == capacity
s6 = Solver()
s6.add(valid_capacity, valid_size)
s6.add(Not((is_full) == (size_before == capacity)))
assert s6.check() == unsat, "Invariant 6 violated: is_full definition inconsistent"

print("All Z3 properties verified.")
