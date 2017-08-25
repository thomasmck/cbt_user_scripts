#!/usr/bin/env python

import sys
import XenAPI
import shutil
import urllib3
import requests
from xmlrpclib import ServerProxy

def export_vdi(host, session_id, vdi_uuid, file_format, export_path):
    url = ('https://%s/export_raw_vdi?session_id=%s&vdi=%s&format=%s'
           % (host, session_id, vdi_uuid, file_format))
    with requests.Session() as session:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        request = session.get(url, verify=False, stream=True)
        with open(export_path, 'wb') as filehandle:
            shutil.copyfileobj(request.raw, filehandle)
        request.raise_for_status()

# Add your host address here
host = "cl14-02.xenrt.citrite.net"
vdi_uuid = sys.argv[1]

p = ServerProxy("http://" + host)
# Add your host details here
session = p.session.login_with_password("root", "xenroot", "0.1", "CBT example")['Value']

try:
    vdi_ref = p.VDI.get_by_uuid(session, vdi_uuid)['Value']
    p.VDI.enable_cbt(session, vdi_ref)

    snapshot_ref = p.VDI.snapshot(session, vdi_ref)['Value']
    export_vdi('cl14-02.xenrt.citrite.net', session, p.VDI.get_uuid(session, snapshot_ref)['Value'], 'raw', './testvdi.vhd')
    # Once you are done copying the blocks, delete the snapshot data
    p.VDI.data_destroy(session, snapshot_ref)
    print "Base snapshot uuid is: " + p.VDI.get_uuid(session, snapshot_ref)['Value']

finally:
    p.session.logout()
