#!/usr/bin/env python3
from prettytable import PrettyTable
from pyln.client import LightningRpc
import math

l1 = LightningRpc("/home/lightning/.lightning/bitcoin/lightning-rpc")
t = PrettyTable(['Alias', 'SCID', 'In htlcs', 'Out htlcs', 'Soonest expiry blocks', 'Soonest expiry hours', 'Connected'])
blockheight = (l1.getinfo()['blockheight'])
peers = l1.listpeers()
sumin = 0
sumout = 0
for peer in peers['peers']:
    if peer['connected'] == True:
        conn = "True"
    else:
        conn = "False"
    for channel in peer['channels']:
        outhtlc = 0
        inhtlc = 0
        htlcexpire = 9999999
        for htlc in channel['htlcs']:
            if htlc['direction'] == "out":
                outhtlc += 1
                if htlc['expiry'] < htlcexpire:
                    htlcexpire = htlc['expiry']
            elif htlc['direction'] == "in":
                inhtlc += 1
                if htlc['expiry'] < htlcexpire:
                    htlcexpire = htlc['expiry']
        if ( inhtlc != 0 or outhtlc != 0):
            nodes = l1.listnodes(peer['id'])
            for node in nodes['nodes']:
                alias = node['alias']
            exp = htlcexpire - blockheight
            exptime = round(exp * 10 / 60, 1)
            if exp > 0:
                sumin += inhtlc
                sumout += outhtlc
                t.add_row([alias, channel['short_channel_id'], inhtlc, outhtlc, exp, exptime, conn])
t.add_row(["Total", "-", sumin, sumout, "-", "-", "-"])
print(t)
