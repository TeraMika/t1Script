## Current status:

Altering Alberto's files into one script (`performanceChecker.py`) instead. The originals are `clean_me.py` and `average_series.py` in that order.  

These scripts rely on a download from the page below:  
\> https://vande.gridpp.rl.ac.uk/next/d/qlK_dfLGz/echo-xrootd-gridftp-gw-host-view?orgId=1&viewPanel=3  
\> Click GridFTP Header Dropdown -> 'Inspect' -> 'Data Options' -> from 'show data frame' dropdown select 'series joined by time' -> 'Download CSV'  
The script then clears empty columns, creates a rolling average of the chosen columns.  
If any values deviate signicantly (`relative_distance>0.25`, so 25% difference) then the chart displayed includes an error at that time.  
\> The original script cleans the CSV and saves a new one, which is read by the second script.  

I've also included in the repository (`/data`) an example of an uncleaned (`last_test_alberto.csv`) and cleaned (`cleaned-last_test_alberto.csv`) file which was inherited from Alberto, if you're struggling to download from the Grafana link above then this will work as an example.

---

## Next steps

The obvious next step is to get data from this page without requiring a manual download of a file.

Looking through the page settings, the link above is connected to ceph-influxdb1 (`http://ceph-influxdb1.gridpp.rl.ac.uk:8086`). The JSON model also buried in the settings should have a query that can be adapted to get the same sort of data (probably the last day's worth?).

Examples like [this page](https://www.influxdata.com/blog/getting-started-python-influxdb/
) might be useful for doing this. I was able to read/write data with InfluxDB on localhost but didn't have any luck querying ceph-influxdb1 any more than `show databases`, even with credentials. I ran out of time to investigate this much further.  
It is definitely possible to get the data from influx into a usable-by-script dataframe format, but the specific implementation is unclear as I'm not sure exactly what format the ceph-influxdb1 data is in.  
\> The examples above should be useful, those Python modules seem the easiest way to do this.
\> If you'd like to view the test code I wrote to talk to Influx shoot me an email (Darren should have it), or tag me in an issue or something. It's really just following the tutorials on the Influx site though.

#### After that

After reading the data in from ceph-influxdb1, it should be easy to get it into a dataframe and usable.  
So the next step would be a better way to select the columns to be displayed by the script than just manually typing them. A list of options?  
And then a place for the script to be run more frequently/regularly, hosted somewhere, and how it might notify people of an issue when an error is detected (Jenkins?). These steps may require some meaningful change in functionality so I haven't considered these any further than that. It may be that something else is needed or better!