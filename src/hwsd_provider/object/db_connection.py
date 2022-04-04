import os
import platform
from pathlib import Path

import jaydebeapi
from pyodbc import connect


class DbConnection:
    def __init__(self, is_permanent):
        self.is_permanent = is_permanent
        self.connexion = None
        self.ms_db_pth = str(Path(os.environ['HWSD_DATA']) / 'HWSD' / 'HWSD.mdb')

    def open_connection(self):
        platform_sys = platform.system()
        if platform_sys == "Windows":
            driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
            con = connect('DRIVER={};DBQ={};'.format(driver, self.ms_db_pth))
        elif platform_sys == "Linux":
            ucanacess_file_path = os.environ["UCANACESS_FILE_PATH"]
            ucanaccess_jars = [
                f"{ucanacess_file_path}/UCanAccess-5.0.1.bin/lib/commons-lang3-3.8.1.jar",
                f"{ucanacess_file_path}/UCanAccess-5.0.1.bin/lib/commons-logging-1.2.jar",
                f"{ucanacess_file_path}/UCanAccess-5.0.1.bin/lib/hsqldb-2.5.0.jar",
                f"{ucanacess_file_path}/UCanAccess-5.0.1.bin/lib/jackcess-3.0.1.jar",
                f"{ucanacess_file_path}/UCanAccess-5.0.1.bin/ucanaccess-5.0.1.jar"
            ]
            classpath = ":".join(ucanaccess_jars)
            con = jaydebeapi.connect(
                "net.ucanaccess.jdbc.UcanaccessDriver",
                f"jdbc:ucanaccess://{self.ms_db_pth}",
                ["", ""],
                classpath
            )

        else:
            raise ValueError(f'{platform_sys} is not already supported')
        self.connexion = con

    def close_connection(self):
        self.connexion.close()
