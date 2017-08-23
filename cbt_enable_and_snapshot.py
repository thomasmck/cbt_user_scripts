#!/usr/bin/env python

import sys
import XenAPI

def export_vdi(snapshot_ref):
    pass


def todo_download_changed_blocks(bitmap, nbd_info):
    pass

vdi_uuid = sys.argv[1]

session = XenAPI.xapi_local()
session.login_with_password("root", "xenroot", "0.1", "CBT example")
try:
    vdi_ref = session.xenapi.VDI.get_by_uuid(vdi_uuid)
    session.xenapi.VDI.enable_cbt(vdi_ref)

    snapshot_ref = session.xenapi.VDI.snapshot(vdi_ref)
    export_vdi(snapshot_ref)
    # Once you are done copying the blocks, delete the snapshot data
    session.xenapi.VDI.data_destroy(snapshot_ref)

    print session.xenapi.VDI.get_uuid(snapshot_ref)
finally:
    session.xenapi.session.logout()