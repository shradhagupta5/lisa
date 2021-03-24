import collections
from typing import Any

from .assertpy import AssertionBuilder

Iterable = collections.abc.Iterable
__tracebackhide__: bool

class CollectionMixin:
    def is_iterable(self) -> AssertionBuilder: ...
    def is_not_iterable(self) -> AssertionBuilder: ...
    def is_subset_of(self, *supersets: Any) -> AssertionBuilder: ...
    def is_sorted(self, key: Any = ..., reverse: bool = ...) -> AssertionBuilder: ...