import numpy as np
import pandas as pd
from datetime import datetime
import re
import os
import shutil
from WM_Translator import Translator
from WM_DREAM_beta import WM_DREAM
from SM_DREAM_beta import SM_DREAM



if __name__ == "__main__":

    # Link to Vito's secrete spreadsheet
    path = "N:\\Water Main\\ProjectDocs\\BOD Order Numbers.xls"
    # Link to WM-EAM download
    trail = "C:\\Users\\wwang\\Desktop\\Monty\\DREAM\\WM_DREAM.xlsx"
    # Link to SM-EAM download
    track = "C:\\Users\\wwang\\Desktop\\Monty\\DREAM\\SM_DREAM.xlsx"

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
    # 
    pathout = "N:\\Program Controls\\CTR Program Controls\\Scheduling\\IH Schedules\\IH Daily Progress Updates_Sewer_WM\\" + \
              year + "\\" + mon_int + " - " + mon_str + "\\EAM-Report_" + date_str + ".xlsx"

    writer = pd.ExcelWriter(pathout)
    df_wm.to_excel(writer, sheet_name = "IH_WM")
    df_sm.to_excel(writer, sheet_name = "IH_SM")
    writer.save()

    # Create copies of EAM data and save to archieve
    origin = "C:\\Users\\wwang\\Desktop\\Monty\\DREAM\\"
    target = "N:\\Program Controls\\CTR Program Controls\\Scheduling\\IH Schedules\\IH Daily Progress Updates_Sewer_WM\\" + \
             year + "\\DREAM_archieve\\"
    shutil.copy(os.path.join(origin, "WM_DREAM.xlsx"), os.path.join(target, ("WM_DREAM_" + date_str + ".xlsx")))
    shutil.copy(os.path.join(origin, "SM_DREAM.xlsx"), os.path.join(target, ("SM_DREAM_" + date_str + ".xlsx")))
