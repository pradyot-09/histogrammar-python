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

import math
import unittest

from histogrammar import *

class TestEverything(unittest.TestCase):
    simple = [3.4, 2.2, -1.8, 0.0, 7.3, -4.7, 1.6, 0.0, -3.0, -1.7]

    class Struct(object):
        def __init__(self, x, y, z, w):
            self.bool = x
            self.int = y
            self.double = z
            self.string = w
        def __repr__(self):
            return "Struct({}, {}, {}, {})".format(self.bool, self.int, self.double, self.string)

    struct = [
        Struct(True,  -2,  3.4, "one"),
        Struct(False, -1,  2.2, "two"),
        Struct(True,   0, -1.8, "three"),
        Struct(False,  1,  0.0, "four"),
        Struct(False,  2,  7.3, "five"),
        Struct(False,  3, -4.7, "six"),
        Struct(True,   4,  1.6, "seven"),
        Struct(True,   5,  0.0, "eight"),
        Struct(False,  6, -3.0, "nine"),
        Struct(True,   7, -1.7, "ten"),
        ]

    backward = list(reversed(struct))

    # straightforward mean and variance to complement the Tony Finch calculations used in the module

    @staticmethod
    def mean(x):
        if len(x) == 0:
            return 0.0
        else:
            return sum(x) / len(x)

    @staticmethod
    def meanWeighted(x, w):
        if not any(_ > 0.0 for _ in w):
            return 0.0
        else:
            return sum(xi * max(wi, 0.0) for xi, wi in zip(x, w)) / sum(_ > 0.0 for _ in w)

    @staticmethod
    def variance(x):
        if len(x) == 0:
            return 0.0
        else:
            return sum(math.pow(_, 2) for _ in x) / len(x) - math.pow(sum(x) / len(x), 2)

    @staticmethod
    def varianceWeighted(x, w):
        if not any(_ > 0.0 for _ in w):
            return 0.0
        else:
            return sum(xi**2 * max(wi, 0.0) for xi, wi in zip(x, w)) / sum(_ > 0.0 for _ in w) - math.pow(sum(xi * max(wi, 0.0) for xi, wi in zip(x, w)) / sum(_ > 0.0 for _ in w), 2)

    @staticmethod
    def mae(x):
        if len(x) == 0:
            return 0.0
        else:
            return sum(map(abs, x)) / len(x)

    @staticmethod
    def maeWeighted(x, w):
        if not any(_ > 0.0 for _ in w):
            return 0.0
        else:
            return sum(abs(xi) * max(wi, 0.0) for xi, wi in zip(x, w)) / sum(_ > 0.0 for _ in w)

    def checkJson(self, x):
        self.assertEqual(x.toJson(), Factory.fromJson(x.toJson()).toJson())

    ################################################################ Count

    def testCount(self):
        for i in xrange(11):
            left, right = self.simple[:i], self.simple[i:]

            leftCounting = Count()
            rightCounting = Count()

            for _ in left: leftCounting.fill(_)
            for _ in right: rightCounting.fill(_)

            self.assertEqual(leftCounting.entries, len(left))
            self.assertEqual(rightCounting.entries, len(right))

            finalResult = leftCounting + rightCounting

            self.assertEqual(finalResult.entries, len(self.simple))

            self.checkJson(leftCounting)
