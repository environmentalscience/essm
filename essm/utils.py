# -*- coding: utf-8 -*-
"""Core equation type."""

from __future__ import absolute_import


def process_parents(parents, cls, attribute='definition'):
    """Process parents that subclass given class."""
    return tuple(
        getattr(parent, attribute) if issubclass(parent, cls) else parent
        for parent in parents)
