#!/usr/bin/env python3
from pyln.client import LightningRpc
import time

# Here you MUST set the location of lightning-rpc socket. It should be in the lightning home dir, under bitcoin
l1 = LightningRpc("/home/lightning/.lightning/bitcoin/lightning-rpc")

# Since payment hashes are not unique, meaning a payment hash can be a successful and a failed payment as well
# we first get all payments that have failed, and all payments that are successful.
# Then we remove all self-payments from the failed payments list, where a successful payment with the same hash exists.
# Then we remove duplicate hashes, and we send these hashes to cln for deletion.


deletepays = []
nodeid = (l1.getinfo()['id'])
listpays = l1.listpays(status="failed")
listcompletepays = l1.listpays(status="complete")
for pays in listpays['pays']:
    if pays['destination'] != nodeid:
        continue
    delit = True
    for completepays in listcompletepays['pays']:
        if pays['payment_hash'] == completepays['payment_hash']:
            delit = False
            break
    if delit == True:
        deletepays.append(pays['payment_hash'])

deletepays = list(set(deletepays))
totalamount = len(deletepays)
for i in range(len(deletepays)):
    #pct_complete = ( i / totalamount * 100)     # Uncomment this, and the line below if you want a realtime counter
    #print(f"Deleting number: {i}\t\t\tTotal amount: {totalamount}\t\t\tComplete: {pct_complete}%\n")
    result = l1.delpay(deletepays[i],"failed")
    
