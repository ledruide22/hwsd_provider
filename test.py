import jaydebeapi
import pandas as pd


db_path='/src/resources/HWSD/HWSD.mdb'

ucanaccess_jars = [
    "/src/UCanAccess-5.0.1.bin/lib/commons-lang3-3.8.1.jar",
    "/src/UCanAccess-5.0.1.bin//lib/commons-logging-1.2.jar",
    "/src/UCanAccess-5.0.1.bin//lib/hsqldb-2.5.0.jar",
    "/src/UCanAccess-5.0.1.bin//lib/jackcess-3.0.1.jar",
    "/src/UCanAccess-5.0.1.bin//lib/ucanaccess-5.0.1.jar",
]
classpath = ":".join(ucanaccess_jars)
cnxn = jaydebeapi.connect(
    "net.ucanaccess.jdbc.UcanaccessDriver",
    f"jdbc:ucanaccess://{db_path}",
    ["", ""],
    classpath,
)
requesta = 'SELECT T_GRAVEL, T_SAND, T_SILT , T_REF_BULK_DENSITY, T_BULK_DENSITY, T_OC, T_PH_H2O, T_CEC_CLAY, T_CEC_SOIL, T_BS, T_TEB, T_CACO3, T_CASO4,T_ESP,T_ECE FROM HWSD_DATA WHERE ID IN (9483, 9483)'
df = pd.read_sql_query(requesta, cnxn)
print(df)