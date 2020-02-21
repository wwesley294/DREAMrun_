import numpy as np
import pandas as pd
from datetime import datetime
import re
import dateutil.parser as dparser
import warnings


# SM_DREAM extracts, cleanses, and returns data from SM-EAM download.
class SM_DREAM(object):

    def __init__(self, track):
        self.track = track
        return

    # dream_import creates a new DataFrame based on data from SM-EAM download.
    # dream_import also defines an unique list of BES numbers. 
    def dream_import(self):

        # To mount data from SM-EAM download and store it in df_og for further cleansing.
        lost = [0, 2, 3, 4, 5, 8, 9, 12, 11, 13]
        df_og = pd.read_excel(self.track, usecols = lost)
        row = df_og.shape[0] - 1
        df_og = df_og.iloc[3:row, :]
        df_og.columns = df_og.loc[3]
        df_og = df_og.drop(3, axis = 0)
        trashtaco = ["BES", "ReportNo", "Status", "Location", "WO_Date", "Foreman", "Task", "Type", "Size", "Daily_ft"]
        df_og.columns = trashtaco

        # To normalize data and sort by dates.
        df_og["WO_Date"] = pd.to_datetime(df_og["WO_Date"])
        df_og = df_og.sort_values("WO_Date", ascending = False)

        # To generate an unique list of BES numbers.
        bes_list = list(pd.Series(df_og["BES"]).drop_duplicates())

        self.df_og = df_og
        self.bes_list = bes_list

    # output summarizes data in df_og by BES numbers.
    # output compiles a report for export in the form of a DataFrame.
    def output(self):

        # To create an empty dictionary to store the summaries of all projects.
        output_dict = {}

        # To loop through the BES numbders and call temp_frame to produce summary of a particular project.
        # To update output_dict with the results returned by temp_frame.
        for bes in self.bes_list:
            output_dict.update(self.temp_frame(self.df_og, bes))

        # To transfer data in output_dict to a new DataFrame, df_output.
        # To re-organize and re-name columns for export.
        df_output = pd.DataFrame.from_dict(output_dict, orient = "index")
        fatfingaz = ["Update_Date", "ReportNo", "Status", "Foreman", "Total_Footage"]
        df_output.columns = fatfingaz
        
        self.df_output = df_output

    # temp_frame takes two arguments (df, bes) from output to generate metrics for a particular project.
    # temp_frame returns a dictionary to be added to output_dict in output later.
    def temp_frame(self, df_og, bes):

        # To create a temporary dictionary to hold the proejct metrics.
        temp_dict = {}

        # To extract all data pertaining to the project using its BES number.
        df_temp = df_og[df_og["BES"] == bes].sort_values("WO_Date", ascending = False)

        # To update project status to mode.
        # To reset the index of df_temp for further analysis.
        mode = str(pd.Series(df_temp["Status"]).mode())
        status = re.sub("[0-9 ]", "", mode).split("\n", 1)[0]
        df_temp = df_temp.reset_index(drop = True)

        # To record the data and report numbers of the most recent project update.
        update_date = df_temp.loc[0, "WO_Date"]
        report_no = df_temp.loc[0, "ReportNo"]

        # To determine the foreman responsible for the project.
        foreman = df_temp.loc[0, "Foreman"]

        # To limit computation to only side-connection and daily-pipe footage.
        df_footcal = df_temp[(df_temp["Task"] == "SIDECONN") | (df_temp["Task"] == "DAILYPIPE")]

        # To remove duplicate data with criteria: report numebr, type, size, and daily footage.
        df_footcal = df_footcal.drop_duplicates(subset = ["ReportNo", "Type", "Size", "Daily_ft"])    

        # To calculate the total footage of the project.
        footage = round(df_footcal["Daily_ft"].sum(), 1)
        
        # To standardize BES numbers.
        bes = re.sub("[ -]", "", bes)

        # To combine the BES number with its milestones (in variables) into a temporary dictionary for return.
        temp_dict = {bes : [update_date, report_no, status, foreman, footage]}
        
        return temp_dict
