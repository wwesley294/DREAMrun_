<div align="center">
  <a href="http://beesbeesbees.com/"><img width="300px" height="auto" src="doc/axe.jpg"></a>
</div>

---

**DREAMrun_** (**D**daily-**R**eport-**EAM**_run) extracts, transforms, and loads data from EAM. The end product is a comprehensive report that can then be used to update the schedules and fulfill other tracking-related tasks. The report is automatically archived and distributed to the designated locations.

## Installation
Since **DREAMrun_** is not yet a part of PyPI (booo...), you will just have to download everything manually.

## Quick Start
DREAMrun.py is the band leader and only thing you really care about. Before running, remember to update the user inputs.


```python

# Link to BOD Order Numbers
path = "USER INPUT"
# Link to WM-EAM download
trail = "USER INPUT"
# Link to SM-EAM download
track = "USER INPUT"

```

```python

# Export path of EAM-Report
pathout = "USER INPUT" + \
          year + "\\" + mon_int + " - " + mon_str + "\\EAM-Report_" + date_str + ".xlsx"
              
```

```python

# Create copies of EAM data and save to archive
origin = "USER INPUT"
target = "USER INPUT" + \
         year + "\\DREAM_archieve\\"
             
```

## Contributing
"When you cease to make a contribution, you begint to die"   -Eleanor Roosevelt

## Acknowledgement
**DREAMrun_** strives to provide a reliable data ETL platform without disclosing sensitive information.

