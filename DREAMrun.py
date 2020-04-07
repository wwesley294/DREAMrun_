import pandas as pd
from datetime import datetime
import os
import shutil
from WM_DREAM import WM_DREAM
from SM_DREAM import SM_DREAM


if __name__ == "__main__":

    # Link to BOD Order Numbers
    path = "USER INPUT"
    # Link to WM-EAM download
    trail = "USER INPUT"
    # Link to SM-EAM download
    track = "USER INPUT"

    box = WM_DREAM(path, trail)
    box.load_bodon()
    box.dream_import()
    box.output()
    df_wm = box.df_output

    jar = SM_DREAM(track)
    jar.dream_import()
    jar.output()
    df_sm = jar.df_output

    mon_int = datetime.now().strftime("%m")
    mon_str = datetime.now().strftime("%b")
    year = datetime.now().strftime("%Y")
    date_str = datetime.strftime(datetime.now(), "%m%d%Y")

    # Export path of EAM-Report
    pathout = "USER INPUT" + \
              year + "\\" + mon_int + " - " + mon_str + "\\EAM-Report_" + date_str + ".xlsx"

    writer = pd.ExcelWriter(pathout)
    df_wm.to_excel(writer, sheet_name = "IH_WM")
    df_sm.to_excel(writer, sheet_name = "IH_SM")
    writer.save()

    # Create copies of EAM data and save to archive
    origin = "USER INPUT"
    target = "USER INPUT" + \
             year + "\\DREAM_archieve\\"
    shutil.copy(os.path.join(origin, "WM_DREAM.xlsx"), os.path.join(target, ("WM_DREAM_" + date_str + ".xlsx")))
    shutil.copy(os.path.join(origin, "SM_DREAM.xlsx"), os.path.join(target, ("SM_DREAM_" + date_str + ".xlsx")))
