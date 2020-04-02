import numpy as np
import pandas as pd
import re


# Translator extracts and cleanses data from BOD Order Numbers.
# Translator allows A numbers to be translated into BES numbers and vice versa.
class Translator(object):

    def __init__(self, path):
        self.path = path
        return

    # bodon creats a new DataFrame of corresponding A and BES numbers.   
    def bodon(self):
        df_bodon = pd.DataFrame()

        # To mount data from BOD Order Numbers and store it in df_bodon for cleansing.
        xlsx = pd.ExcelFile(self.path)
        sheet_list = xlsx.sheet_names
        for sheet in sheet_list:
            df_temp = pd.read_excel(self.path, sheet_name = sheet)
            df_temp = df_temp.iloc[:, 0:2]
            column_list = ["BOD_Order", "BES"]
            df_temp.columns = column_list
            df_bodon = pd.concat([df_bodon, df_temp])

        # To cleanse df_bodon.
        df_bodon.fillna("DNE", inplace=True)

        # To collect only the number portion of the A numbers.
        df_bodon["BOD_Num"] = np.nan
        df_bodon["BOD_Num"] = df_bodon["BOD_Order"].apply(lambda x: str(x)[2:8])

        # To standardize BES numbers.
        df_bodon["BES_Num"] = np.nan
        df_bodon["BES_Num"] = df_bodon["BES"].apply(lambda y: re.sub("[:-]", "", str(y)))

        # To abandon the original data from BOD Order Numebers.
        df_bodon = df_bodon.drop("BOD_Order", axis=1)
        df_bodon = df_bodon.drop("BES", axis=1)
        
        return df_bodon

    # bes_lookup takes an A-number argument and returns the corresponding BES number.
    def bes_lookup(self, df, anum):
        return df["BES_Num"][df["BOD_Num"] == anum].item()
    
    # anum_lookup takes a BES-number argument and returns the corresponding A number.
    def anum_lookup(self, df, bes):
        return df["BOD_Num"][df["BES_Num"] == bes].item()


# WM_Translator as a stand-alone module can also translate A numbers into BES numbers directly.
# WM_Translator takes user inputs and operates using the Translator class.
if __name__ == "__main__":
    trans = Translator()
    user_input = input("What you looking for? (bes/anum)")
    if "bes" in user_input:
        answer = input("Please enter the A number: ")
        print (trans.bes_lookup(answer))
    elif "anum" in user_input:
        answer = input("Please enter the BES number: ")
        print (trans.anum_lookup(answer))
    else:
        print ("Bruh can you type?")

