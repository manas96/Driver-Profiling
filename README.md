# StuntRally
Modifying game code to log input events for driver profiling and sentiment analysis.

# Notes:

-Always exit the game properly(no Altf4!) to ensure the log file is porperly generated and stored.

-grep "EDITED MANAS" to find edits.

# Done:

-Added basic keypress logging.(Up,down,left,right,ctrl,space).

-Added car name.

-Added lap counter.

-LogReader.py processes logfile and creates appropriate data structures for each log.

-ml.py , compare.py used to view data.
