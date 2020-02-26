#!/usr/bin/env python3
# Copyright (c) 2020 Bitcoin Association
# Distributed under the Open BSV software license, see the accompanying file LICENSE.
"""
Test stalling isn't triggered just for large blocks.
"""
from test_framework.test_framework import ComparisonTestFramework
from test_framework.util import assert_equal, p2p_port, connect_nodes
from test_framework.comptool import TestInstance
from test_framework.cdefs import ONE_GIGABYTE, ONE_MEGABYTE, ONE_KILOBYTE
from test_framework.util import get_rpc_proxy, wait_until, check_for_log_msg

class StallingTest(ComparisonTestFramework):

    def set_test_params(self):
        self.num_nodes = 2
        self.setup_clean_chain = True
        self.genesisactivationheight = 101
        self.nocleanup = True
        self.extra_args = [
            [
            '-whitelist=127.0.0.1',
            '-excessiveblocksize=%d' % (ONE_GIGABYTE * 6),
            '-blockmaxsize=%d' % (ONE_GIGABYTE * 6),
            '-maxmempool=%d' % ONE_GIGABYTE * 10,
            '-maxtxsizepolicy=%d' % ONE_GIGABYTE * 2,
            '-maxscriptsizepolicy=0',
            '-rpcservertimeout=1000',
            '-genesisactivationheight=%d' % self.genesisactivationheight,
            "-txindex"
            ]
        ] * self.num_nodes

        self.num_blocks = 120

    def run_test(self):
        self.test.run()

    def get_tests(self):
        # shorthand for functions
        block = self.chain.next_block
        node = get_rpc_proxy(self.nodes[0].url, 1, timeout=6000, coveragedir=self.nodes[0].coverage_dir)

        # Create a new block
        self.chain.set_genesis_hash(int(node.getbestblockhash(), 16))
        block(0)
        self.chain.save_spendable_output()
        yield self.accepted()

        # Now we need that block to mature so we can spend the coinbase.
        test = TestInstance(sync_every_block=False)
        for i in range(self.num_blocks):
            block(5000 + i)
            test.blocks_and_transactions.append([self.chain.tip, True])
            self.chain.save_spendable_output()
        yield test

        # Collect spendable outputs now to avoid cluttering the code later on
        out = []
        for i in range(self.num_blocks + 1):
            out.append(self.chain.get_spendable_output())

        # Create 1GB block
        block(1, spend=out[0], block_size=1*ONE_GIGABYTE)
        yield self.accepted()

        # Create long chain of smaller blocks
        test = TestInstance(sync_every_block=False)
        for i in range(self.num_blocks):
            block(6000 + i, spend=out[i + 1], block_size=64*ONE_KILOBYTE)
            test.blocks_and_transactions.append([self.chain.tip, True])
        yield test

        # Launch another node with config that should avoid a stall during IBD
        self.log.info("Launching extra nodes")
        self.add_node(2, extra_args = [
                                    '-whitelist=127.0.0.1',
                                    '-excessiveblocksize=%d' % (ONE_GIGABYTE * 6),
                                    '-blockmaxsize=%d' % (ONE_GIGABYTE * 6),
                                    '-maxtxsizepolicy=%d' % ONE_GIGABYTE * 2,
                                    '-maxscriptsizepolicy=0',
                                    '-rpcservertimeout=1000',
                                    '-genesisactivationheight=%d' % self.genesisactivationheight,
                                    "-txindex",
                                    "-maxtipage=0",
                                    "-blockdownloadwindow=64",
                                    "-blockstallingtimeout=6"
                                      ],
                      init_data_dir=True)
        self.start_node(2)
        # Launch another node with a very high requried bandwidth that will cause it to hit the stall
        self.add_node(3, extra_args = [
                                    '-whitelist=127.0.0.1',
                                    '-excessiveblocksize=%d' % (ONE_GIGABYTE * 6),
                                    '-blockmaxsize=%d' % (ONE_GIGABYTE * 6),
                                    '-maxtxsizepolicy=%d' % ONE_GIGABYTE * 2,
                                    '-maxscriptsizepolicy=0',
                                    '-rpcservertimeout=1000',
                                    '-genesisactivationheight=%d' % self.genesisactivationheight,
                                    "-txindex",
                                    "-maxtipage=0",
                                    "-blockdownloadwindow=64",
                                    "-blockstallingmindownloadspeed=50000000",
                                    "-blockstallingtimeout=6"
                                      ],
                      init_data_dir=True)
        self.start_node(3)

        # Connect the new nodes up so they do IBD
        self.log.info("Starting IBD")
        connect_nodes(self.nodes[0], 2)
        connect_nodes(self.nodes[1], 2)
        connect_nodes(self.nodes[0], 3)
        connect_nodes(self.nodes[1], 3)
        self.sync_all(timeout=120)

        # Check we didn't hit a stall for node2
        assert(not check_for_log_msg("stalling block download", self.options.tmpdir + "/node2"))

        # Check we hit a stall for node3 (if this test starts failing, try increasing
        # -blockstallingmindownloadspeed above, if it still keeps failing then consider
        # getting rid of this test on node3 because it doesn't add much)
        assert(check_for_log_msg("stalling block download", self.options.tmpdir + "/node3"))

if __name__ == '__main__':
    StallingTest().main()
