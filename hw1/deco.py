#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import update_wrapper, wraps


def disable(func):
    """
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    """
    return func


def decorator(decorator_func):
    """
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    """
    return update_wrapper(decorator_func, 1)


def countcalls(func):
    """Decorator that counts calls made to the function decorated."""
    @wraps(func)
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return func(*args, **kwargs)

    wrapped.calls = 0
    return wrapped


def memo(func):
    """
    Memoize a function so that it caches all return values for
    faster future lookups.
    """
    memory = {}

    @wraps(func)
    def decorated(*args):
        if args in memory:
            return memory[args]

        answer = func(*args)
        memory[args] = answer

        return answer

    return decorated


def n_ary(func):
    """
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    """
    @wraps(func)
    def wrapped(*args):
        if len(args) == 1:
            return args[0]
        if len(args) == 2:
            return func(*args)
        return func(args[0], wrapped(*args[1:]))
    return wrapped


def trace(ident):
    """Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    """
    def deco(func):

        @wraps(func)
        def wrapped(*args, **kwargs):
            arguments = [str(a) for a in args] + ["%s=%s" % (key, value) for key, value in kwargs.iteritems()]
            argument_string = ",".join(arguments)
            func_name = "%s(%s)" % (func.__name__, argument_string)
            wrapped.call_level += 1
            print ident * wrapped.call_level, "-->", func_name
            answer = func(*args, **kwargs)
            print ident * wrapped.call_level, "<--", func_name, "==", answer
            wrapped.call_level -= 1
            return answer

        wrapped.call_level = 0
        return wrapped

    return deco


@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace("####")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print foo(4, 3)
    print foo(4, 3, 2)
    print foo(4, 3)
    print "foo was called", foo.calls, "times"

    print bar(4, 3)
    print bar(4, 3, 2)
    print bar(4, 3, 2, 1)
    print "bar was called", bar.calls, "times"

    print fib.__doc__
    fib(3)
    print fib.calls, 'calls made'


if __name__ == '__main__':
    main()
