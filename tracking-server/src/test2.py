from datetime import timezone
from datetime import datetime
import pytz

country = pytz.timezone("America/Guatemala")
#dtnow = datetime.now(country)
dtnow = datetime.strptime("03-06-22-22:31:00","%d-%m-%y-%H:%M:%S")
dtxt = str(dtnow).split(".")[0]
ts = int(datetime.timestamp(dtnow))
#print(dtxt)

fmt = '%d-%m-%Y-%H:%M:%S'
utc_dt = pytz.utc.localize(datetime.utcfromtimestamp(ts))
a = utc_dt.strftime(fmt)
#print (a)
#print(dtnow,"==>",utc_dt,int(utc_dt.timestamp()))
utc_now = datetime.utcnow()
print("utcnow",utc_now,utc_now.timestamp())

dtnow = datetime.strptime(a,"%d-%m-%Y-%H:%M:%S")
dtxt = str(dtnow).split(".")[0]
print(dtxt,dtnow.timestamp())



dt = datetime.now(timezone.utc)
utc_time = dt.replace(tzinfo=timezone.utc)
utc_timestamp = utc_time.timestamp()
#print(utc_time,int(utc_timestamp))

