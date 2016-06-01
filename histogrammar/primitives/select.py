#!/usr/bin/env python

# Copyright 2016 Jim Pivarski
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from histogrammar.defs import *
from histogrammar.util import *

################################################################ Select

class Select(Factory, Container):
    @staticmethod
    def ed(entries, cut):
        if entries < 0.0:
            raise ContainerException("entries ({}) cannot be negative".format(entries))
        out = Select(None, cut)
        out.entries = entries
        return out

    @staticmethod
    def ing(quantity, cut):
        return Select(quantity, cut)

    def __init__(self, quantity, cut):
        self.entries = 0.0
        self.quantity = serializable(quantity)
        self.cut = cut
        super(Select, self).__init__()

    def fractionPassing(self):
        return self.cut.entries / self.entries

    def zero(self):
        return Select(self.quantity, self.cut.zero())

    def __add__(self, other):
        if isinstance(other, Select):
            out = Select(self.quantity, self.cut + other.cut)
            out.entries = self.entries + other.entries
            return out
        else:
            raise ContainerException("cannot add {} and {}".format(self.name, other.name))

    def fill(self, datum, weight=1.0):
        w = weight * self.quantity(datum)
        if w > 0.0:
            self.cut.fill(datum, w)
        # no possibility of exception from here on out (for rollback)
        self.entries += weight

    @property
    def children(self):
        return [self.cut]

    def toJsonFragment(self, suppressName): return maybeAdd({
        "entries": floatToJson(self.entries),
        "type": self.cut.name,
        "data": self.cut.toJsonFragment(False),
        }, name=(None if suppressName else self.quantity.name))

    @staticmethod
    def fromJsonFragment(json, nameFromParent):
        if isinstance(json, dict) and hasKeys(json.keys(), ["entries", "type", "data"], ["name"]):
            if isinstance(json["entries"], (int, long, float)):
                entries = float(json["entries"])
            else:
                raise JsonFormatException(json, "Select.entries")

            if isinstance(json.get("name", None), basestring):
                name = json["name"]
            elif json.get("name", None) is None:
                name = None
            else:
                raise JsonFormatException(json["name"], "Select.name")

            if isinstance(json["type"], basestring):
                factory = Factory.registered[json["type"]]
            else:
                raise JsonFormatException(json, "Select.type")

            cut = factory.fromJsonFragment(json["data"], None)

            out = Select.ed(entries, cut)
            out.quantity.name = nameFromParent if name is None else name
            return out

        else:
            raise JsonFormatException(json, "Select")

    def __repr__(self):
        return "<Select cut={}>".format(self.cut.name)

    def __eq__(self, other):
        return isinstance(other, Select) and numeq(self.entries, other.entries) and self.cut == other.cut

    def __hash__(self):
        return hash((self.entries, self.cut))

Factory.register(Select)

