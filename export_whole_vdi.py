#!/usr/bin/env python

import shutil
import urllib3
import requests
import XenAPI
import sys


def export_vdi(host, session_id, vdi_uuid, file_format, export_path):
    url = ('https://%s/export_raw_vdi?session_id=%s&vdi=%s&format=%s'
           % (host, session_id, vdi_uuid, file_format))
    with requests.Session() as session:
        # ToDo: Security - We need to verify the SSL certificate here.
        # Depends on CP-23051.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        request = session.get(url, verify=False, stream=True)
        with open(export_path, 'wb') as filehandle:
            shutil.copyfileobj(request.raw, filehandle)
        request.raise_for_status()


def main():
    session = XenAPI.xapi_local()
    session.xenapi.login_with_password('root', '', '1.0', 'CBT Example')
    vdi_uuid = sys.argv[1]
    path = sys.argv[2]
    try:
        export_vdi('localhost', session._session, vdi_uuid, 'raw', path)
    finally:
        session.xenapi.logout()


if __name__ == "__main__":
    main()