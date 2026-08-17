import pytest

from ring_buffer import RingBuffer


def test_constructor_valid_capacity():
    rb = RingBuffer(3)
    assert rb.capacity == 3
    assert rb.size() == 0
    assert not rb.is_full()


def test_constructor_invalid_raises():
    with pytest.raises(ValueError):
        RingBuffer(0)
    with pytest.raises(ValueError):
        RingBuffer(-5)


def test_push_increases_size():
    rb = RingBuffer(3)
    rb.push(1)
    assert rb.size() == 1
    rb.push(2)
    assert rb.size() == 2


def test_push_never_exceeds_capacity():
    rb = RingBuffer(2)
    rb.push(1)
    rb.push(2)
    rb.push(3)  # overwrites oldest
    assert rb.size() == 2
    assert rb.is_full()


def test_push_overwrites_oldest_when_full():
    rb = RingBuffer(2)
    rb.push(1)
    rb.push(2)
    rb.push(3)  # 1 should be overwritten
    assert rb.pop() == 2
    assert rb.pop() == 3


def test_pop_fifo_order():
    rb = RingBuffer(5)
    rb.push(10)
    rb.push(20)
    rb.push(30)
    assert rb.pop() == 10
    assert rb.pop() == 20
    assert rb.pop() == 30


def test_pop_reduces_size():
    rb = RingBuffer(3)
    rb.push(1)
    rb.push(2)
    assert rb.size() == 2
    rb.pop()
    assert rb.size() == 1


def test_pop_empty_raises():
    rb = RingBuffer(3)
    with pytest.raises(IndexError):
        rb.pop()


def test_is_full_true_when_at_capacity():
    rb = RingBuffer(2)
    rb.push(1)
    rb.push(2)
    assert rb.is_full()


def test_is_full_false_when_below_capacity():
    rb = RingBuffer(2)
    rb.push(1)
    assert not rb.is_full()


def test_size_never_negative_or_over_capacity():
    rb = RingBuffer(3)
    assert rb.size() >= 0
    rb.push(1)
    rb.push(2)
    rb.push(3)
    rb.push(4)
    assert 0 <= rb.size() <= rb.capacity


def test_push_after_full_size_unchanged():
    rb = RingBuffer(2)
    rb.push(1)
    rb.push(2)
    size_before = rb.size()
    rb.push(3)
    assert rb.size() == size_before
