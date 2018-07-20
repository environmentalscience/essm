# -*- coding: utf-8 -*-
#
# This file is part of essm.
# Copyright (C) 2017 ETH Zurich, Swiss Data Science Center.
#
# essm is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# essm is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with essm; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
"""Base classes."""

from __future__ import absolute_import

import warnings


class RegistryType(type):
    """Base registry operations."""

    def __setitem__(cls, expr, definition):
        """Register expression in registry."""
        if expr in cls.__registry__:
            warnings.warn(
                '"{0}" will be overridden by "{1}"'.format(
                    cls.__registry__[expr].__module__ + ':' +
                    cls.__registry__[expr].name,
                    definition.__module__ + ':' + str(cls),
                ),
                stacklevel=2
            )
        cls.__registry__[expr] = definition

    def __delitem__(cls, expr):
        """Remove a expr from the registry."""
        if expr in cls.__registry__:
            warnings.warn(
                '"{0}" will be unregistered.'.format(
                    cls.__registry__[expr].__module__
                ),
                stacklevel=2
            )
            del cls.__registry__[expr]
        else:
            raise KeyError(expr)
