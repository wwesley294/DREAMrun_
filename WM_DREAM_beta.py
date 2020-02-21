import numpy as np
import pandas as pd
from datetime import datetime
import re
import dateutil.parser as dparser
from WM_Translator import Translator
import warnings


# WM_DREAM extracts, cleanses, and returns data from WM-EAM download.
class WM_DREAM(object):

    def __init__(self, path, trail):
        trans = Translator(path)
        self.trans = trans
        self.path = path
        self.trail = trail
        return

    # load_bodon creates a new DataFrame of corresponding A and BES numbers using Translator.
    def load_bodon(self):
        df_bodon = self.trans.bodon()
        self.df_bodon = df_bodon
        
    # dream_import creates a new DataFrame based on data from WM-EAM download.
    # dream_import also defines two unique lists of A numbers and project tasks respectively.
    def dream_import(self):

        # To mount data from WM-EAM download and store it in df_og for further cleansing.
        powerball = [1, 3, 4, 5, 6, 9, 10, 13, 14]
        df_og = pd.read_excel(self.trail, usecols = powerball)
        row = df_og.shape[0] - 1
        df_og = df_og.iloc[3:row, :]
        df_og.columns = df_og.loc[3]
        df_og = df_og.drop(3, axis = 0)
        cashmoney = ["A", "ReportNo", "Status", "Location", "WO_Date", "Foreman", "Task", "8in_Daily", "12in_Daily"]
        df_og.columns = cashmoney

        # To normalize time data, weed out cancelled projects, and sort by dates.
        df_og["WO_Date"] = pd.to_datetime(df_og["WO_Date"])
        df_og = df_og[df_og["Status"] != "Cancelled"]
        df_og = df_og.sort_values("WO_Date", ascending = False)

        # To generate two unique lists of A numbers and project tasks.
        anums = list(pd.Series(df_og["A"]).drop_duplicates())
        tasks = list(pd.Series(df_og["Task"]).drop_duplicates().dropna())

        self.df_og = df_og
        self.anums = anums
        self.tasks = tasks

    # output summarizes data in df_og by A numbers and their respective tasks.
    # output compiles a report for export in the form of a DataFrame.
    def output(self):

        # To create an empty dictionary to store the summaries of all projects.
        output_dict = {}

        # To loop through the A numbers and call temp_frame to produce summary of a particular project.
        # To update output_dict with the results returned by temp_frame.
        for anum in self.anums:
            output_dict.update(self.temp_frame(self.df_og, anum, self.tasks))

        # To transfer data in output_dict to a new DataFrame, df_output.
        # To re-organized and re-name columns for export.
        df_output = pd.DataFrame.from_dict(output_dict, orient = "index")
        qtip = ["BES", "Update_Date", "ReportNo", "Status", "Foreman", "Total_Footage", "Mobilization", \
                   "Pressure_S", "Pressure_E", "Chlorination_S", "Chlorination_E", "ChlorinationApp_S", \
                   "ChlorinationApp_E", "Final_S", "Final_E", "Completion"]
        df_output.columns = qtip

        self.df_output = df_output

    # temp_frame takes three arguments (df, anum, task) from output to generate metrics for a particular project.
    # temp_frame returns a dictionary to be added to output_dict in output later.
    def temp_frame(self, df_og, anum, tasks):

        # To create a temporary dictionary to hold the project metrics.
        temp_dict = {}

        # To verify the A number.
        bes = self.trans.bes_lookup(self.df_bodon, anum[2:8])

        # To extract all data pertaining to the project using its A number.
        df_temp = df_og[df_og["A"] == anum].sort_values("WO_Date", ascending = False)

        # To update project status to mode.
        # To reset the index of df_temp for further analysis.
        mode = str(pd.Series(df_temp["Status"]).mode())
        status = re.sub("[0-9 ]", "", mode).split("\n", 1)[0]
        df_temp = df_temp.reset_index(drop = True)

        # To record the date and report number of the most recent project update.
        update_date = df_temp.loc[0, "WO_Date"]
        report_no = df_temp.loc[0, "ReportNo"]
        
        # To determine the foreman responsible for the project.
        foreman = df_temp.loc[0, "Foreman"]

        # To remove duplicate data with criteria: report number, 8in daily footage, and 12in daily footage.
        df_footcalc = df_temp.drop_duplicates(subset = ["ReportNo", "8in_Daily", "12in_Daily"])

        # To calculate the total footage of the project.
        footage = round((df_footcalc["8in_Daily"].sum() + df_footcalc["12in_Daily"].sum()), 1)

        # To produce a new dictionary from the given sequence of task with a value of 0.
        template = dict.fromkeys(tasks, 0)

        # To acquire compute task milestons by call vladivostok.
        milestones = self.vladivostok(template, df_temp)

        # To assign specific milestones to corresponding variables.
        mob = milestones["MOBILIZATION"][0]
        p_start = milestones["PRESSURETEST"][0]
        p_end = milestones["PRESSURETEST"][1]
        c_start = milestones["CHLORINATION"][0]
        c_end = milestones["CHLORINATION"][1]
        ca_start = milestones["CHLORINATIONAPP"][0]
        ca_end = milestones["CHLORINATIONAPP"][1]
        f_start = milestones["FINALCONN"][0]
        f_end = milestones["FINALCONN"][1]
        comp = milestones["WMCOMP"][0]

        # To combine the A number with its milestones (in variables) into a tempory dictonary for return.
        temp_dict = {anum : [bes, update_date, report_no, status, foreman, footage, mob, p_start, p_end, c_start, c_end, \
                          ca_start, ca_end, f_start, f_end, comp]}

        return temp_dict

    # vladivostok is very remote yet highly critical to the delicate balance of the universe.
    # vladivostok takes two arguments from temp_frame (template, df_temp) to compute task milestones.
    # vladivostok stores milestones in and returns template.
    def vladivostok(self, template, df_temp):

        # To loop through all assigned tasks in template.
        for item in template:

            # To create a temporary list to store miletones.
            list_vlad = []
            
            # To extract all data pertaining to a particular task.
            df_vlad = df_temp[df_temp["Task"]==item]
            df_vlad = df_vlad.reset_index(drop = True)
            
            # If no milestone is present, mark the temporary list empty.
            if df_vlad.empty:
                list_vlad = ["-", "-"]
            
            # If milestones are detected, retrieve the first and last date to represent the start and end date.
            # To normalize time data. 
            else:
                start_date = df_vlad.loc[(df_vlad.shape[0] - 1), "WO_Date"].strftime("%m/%d/%Y")
                end_date = df_vlad.loc[0, "WO_Date"].strftime("%m/%d/%Y") + " (" + str(df_vlad.shape[0]) + ")"
                list_vlad = [start_date, end_date]

            # To store the milestone results in template under corresponding task.
            template[item] = list_vlad

        return template
