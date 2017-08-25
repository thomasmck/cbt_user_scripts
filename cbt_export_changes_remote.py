#!/usr/bin/env python

import sys
import XenAPI
from python2_nbd_client import new_nbd_client
import base64
from bitstring import BitStream
from xmlrpclib import ServerProxy

BLOCK_SIZE = 64 * 1024

def get_changed_blocks(host, export_name, bitmap):

    bitmap = BitStream(bytes=base64.b64decode(bitmap))
    with open('./bitmap', 'ab') as bit_out:
        for bit in bitmap:
            # The bits are written in the form "0" and "1" to the file
            bit_out.write(str(int(bit)))
    print "connecting to NBD"
    client = new_nbd_client(host, export_name[0])
    print "size: %s" % client.size()
    for i in range(0, len(bitmap)):
        if bitmap[i] == 1:
            offset = i * BLOCK_SIZE
            print "reading %d bytes from offset %d" % (BLOCK_SIZE, offset)
            data = client.read(offset=offset, length=BLOCK_SIZE)
            yield data
    print "closing NBD"
    client.close()


def save_changed_blocks(changed_blocks, output_file):

    with open(output_file, 'ab') as out:
        for b in changed_blocks:
            out.write(b)


def download_changed_blocks(session, bitmap, URI, output_file):

    print "downloading changed blocks"
    # Extract the host ip address from the URI
    host = URI[0].split("/")[2].split(":")[0]
    blocks = get_changed_blocks(host, URI, bitmap)
    save_changed_blocks(blocks, output_file)


vdi_uuid = sys.argv[1]
last_snapshot_uuid = sys.argv[2]


host = "cl14-02.xenrt.citrite.net"
p = ServerProxy("http://" + host)
session = p.session.login_with_password("root", "xenroot", "0.1", "CBT example")['Value']
try:
    vdi_ref = p.VDI.get_by_uuid(session, vdi_uuid)['Value']
    last_snapshot_ref = p.VDI.get_by_uuid(session, last_snapshot_uuid)['Value']
    new_snapshot_ref = p.VDI.snapshot(session, vdi_ref)['Value']
    bitmap = p.VDI.export_changed_blocks(session, last_snapshot_ref, new_snapshot_ref)['Value']
    download_changed_blocks(session, bitmap, p.VDI.get_nbd_info(session, new_snapshot_ref)['Value'], './testblocks.vhd')
    # Once you are done copying the blocks you want you can delete the snapshot data
    p.VDI.data_destroy(session, new_snapshot_ref)
    print "Snapshot uuid is: " + p.VDI.get_uuid(session, new_snapshot_ref)['Value']
finally:
    p.session.logout(session)
