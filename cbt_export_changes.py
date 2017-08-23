#!/usr/bin/env python

import sys
import XenAPI

def todo_download_changed_blocks(bitmap, nbd_info):
    pass

vdi_uuid = sys.argv[1]
last_snapshot_uuid = sys.argv[2]

session = XenAPI.xapi_local()
session.login_with_password("root", "xenroot", "0.1", "CBT example")
try:
    vdi_ref = session.xenapi.VDI.get_by_uuid(vdi_uuid)
    last_snapshot_ref = session.xenapi.VDI.get_by_uuid(last_snapshot_uuid)
    new_snapshot_ref = session.xenapi.VDI.snapshot(vdi_ref)
    bitmap = session.xenapi.VDI.export_changed_blocks(last_snapshot_ref, new_snapshot_ref)
    todo_download_changed_blocks(bitmap, session.xenapi.VDI.get_nbd_info(new_snapshot_ref))
    # Once you are done copying the blocks you want you can delete the snapshot data
    session.xenapi.VDI.data_destroy(new_snapshot_ref)
finally:
    session.xenapi.session.logout()