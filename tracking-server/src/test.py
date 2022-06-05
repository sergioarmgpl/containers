import datetime
#from datetime import timezone
import pytz
from pytz import timezone
utc = pytz.utc



sdate = "03-06-22-00:44:00"
edate = "03-06-22-00:45:40"
st = datetime.datetime.strptime(sdate,"%d-%m-%y-%H:%M:%S")
st = int(datetime.datetime.timestamp(st))
#print(st)
#utc_dt = utc.localize(datetime.datetime.utcfromtimestamp(st))
#print(utc_dt)

et = datetime.datetime.strptime(edate,"%d-%m-%y-%H:%M:%S")
et = int(datetime.datetime.timestamp(et))
print(st,et)


#    dtnow = datetime.now(country)
#    dtxt = str(dtnow).split(".")[0]
#    ts = int(datetime.timestamp(dtnow))


fmt = '%d-%m-%Y-%H:%M:%S'
eastern = timezone('America/Guatemala')
#utc_dt = datetime.datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)
utc_dt = datetime.datetime.now(tzinfo=utc)
loc_dt = utc_dt.astimezone(eastern)
xyz=loc_dt.strftime(fmt)
print(utc_dt,loc_dt,xyz)

u=datetime.datetime.strptime(xyz,fmt).replace(tzinfo=datetime.timezone.utc).timestamp()
print(u)
