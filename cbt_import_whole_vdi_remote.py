#!/usr/bin/env python

import shutil
import urllib3
import requests
import XenAPI
import sys
from xmlrpclib import ServerProxy

def import_vdi(host, session_id, vdi_uuid, file_format, import_path):
    url = ('https://%s/import_raw_vdi?session_id=%s&vdi=%s&format=%s'
           % (host, session_id, vdi_uuid, file_format))
    with open(import_path, 'r') as filehandle:
        # ToDo: Security - We need to verify the SSL certificate here.
        # Depends on CP-23051.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        with requests.Session() as session:
            request = session.put(url, filehandle, verify=False)
            request.raise_for_status()

def main():
    host = "cl14-02.xenrt.citrite.net"
    p = ServerProxy("http://" + host)
    session = p.session.login_with_password("root", "xenroot", "0.1", "CBT example")['Value']
    vdi_uuid = sys.argv[1]
    path = sys.argv[2]
    try:
        import_vdi(host, session, vdi_uuid, 'raw', path)
    finally:
        p.session.logout(session)


if __name__ == "__main__":
    main()
