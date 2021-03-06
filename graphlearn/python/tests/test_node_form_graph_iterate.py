# Copyright 2020 Alibaba Group Holding Limited. All Rights Reserved.
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
# =============================================================================
""" Local UT test, run with `sh test_python_ut.sh`.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest

import graphlearn as gl
import graphlearn.python.tests.utils as utils
from graphlearn.python.tests.test_edge import EdgeTestCase


class NodeFromGraphIterateTestCase(EdgeTestCase):
  def test_node_iterate_from_graph(self):
    file_path = self.gen_test_data([utils.ATTRIBUTED], False)
    decoder = gl.Decoder(attr_types=utils.ATTR_TYPES)
    g = gl.Graph() \
      .edge(source=file_path, edge_type=self.edge_tuple_, decoder=decoder)
    g.init(server_id=0, server_count=1, tracker=utils.TRACKER_PATH)

    batch_size = 4
    sampler = g.node_sampler('first',
                             batch_size=batch_size,
                             strategy="by_order", node_from=gl.EDGE_SRC)
    res_ids = []
    max_iter = 100
    for i in range(max_iter):
      try:
        nodes = sampler.get()
        utils.check_node_type(nodes, "user")
        res_ids.extend(list(nodes.ids))
      except gl.OutOfRangeError:
        break
    ids = range(self.src_range_[0], self.src_range_[1])
    utils.check_sorted_equal(res_ids, ids)

    sampler = g.node_sampler('first', batch_size=batch_size,
                             strategy="random", node_from=gl.EDGE_SRC)
    max_iter = 10
    for i in range(max_iter):
      nodes = sampler.get()
      utils.check_subset(nodes.ids, ids)

    sampler = g.node_sampler('first',
                             batch_size=batch_size,
                             strategy="by_order", node_from=gl.EDGE_DST)
    res_ids = []
    max_iter = 100
    for i in range(max_iter):
      try:
        nodes = sampler.get()
        utils.check_node_type(nodes, "item")
        res_ids.extend(list(nodes.ids))
      except gl.OutOfRangeError:
        break
    ids = range(self.dst_range_[0], self.dst_range_[1])
    utils.check_sorted_equal(res_ids, ids)

    sampler = g.node_sampler('first', batch_size=batch_size,
                             strategy="random", node_from=gl.EDGE_DST)
    max_iter = 10
    for i in range(max_iter):
      nodes = sampler.get()
      utils.check_subset(nodes.ids, ids)


if __name__ == "__main__":
  unittest.main()
