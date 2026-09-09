import pytest
from bounded_stack import BoundedStack


def test_initial_size_is_zero():
    s = BoundedStack(5)
    assert s.size() == 0


def test_push_increases_size():
    s = BoundedStack(3)
    s.push(1)
    assert s.size() == 1
    s.push(2)
    assert s.size() == 2


def test_pop_decreases_size_and_returns_lifo_order():
    s = BoundedStack(3)
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.size() == 2
    assert s.pop() == 2
    assert s.size() == 1
    assert s.pop() == 1
    assert s.size() == 0


def test_peek_returns_top_without_removing():
    s = BoundedStack(2)
    s.push(10)
    s.push(20)
    assert s.peek() == 20
    assert s.size() == 2
    assert s.peek() == 20


def test_push_raises_when_at_capacity():
    s = BoundedStack(2)
    s.push(1)
    s.push(2)
    with pytest.raises(ValueError):
        s.push(3)


def test_pop_raises_when_empty():
    s = BoundedStack(2)
    with pytest.raises(IndexError):
        s.pop()


def test_peek_raises_when_empty():
    s = BoundedStack(2)
    with pytest.raises(IndexError):
        s.peek()


def test_size_never_exceeds_capacity():
    cap = 4
    s = BoundedStack(cap)
    for i in range(cap):
        s.push(i)
        assert 0 <= s.size() <= cap
    with pytest.raises(ValueError):
        s.push(999)
    assert s.size() == cap


def test_size_never_negative_after_pops():
    s = BoundedStack(3)
    s.push(1)
    s.push(2)
    s.pop()
    s.pop()
    assert s.size() == 0
    with pytest.raises(IndexError):
        s.pop()
    assert s.size() == 0


def test_capacity_getter():
    s = BoundedStack(7)
    assert s.capacity() == 7


def test_construction_with_invalid_capacity_zero_raises():
    with pytest.raises(ValueError):
        BoundedStack(0)


def test_construction_with_invalid_capacity_negative_raises():
    with pytest.raises(ValueError):
        BoundedStack(-1)


def test_construction_with_invalid_capacity_non_int_raises():
    with pytest.raises(ValueError):
        BoundedStack(2.5)  # type: ignore[arg-type]


def test_lifo_order_mixed_operations():
    s = BoundedStack(5)
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    s.push(3)
    s.push(4)
    assert s.pop() == 4
    assert s.pop() == 3
    assert s.pop() == 1
    assert s.size() == 0
