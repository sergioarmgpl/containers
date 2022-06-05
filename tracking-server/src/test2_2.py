from datetime import timezone
from datetime import datetime
import pytz

#country = pytz.timezone("America/Guatemala")
#dtnow = datetime.now(country)
dtnow = datetime.strptime("03-06-22-22:31:00","%d-%m-%y-%H:%M:%S")
dtxt = str(dtnow).split(".")[0]
ts = int(datetime.timestamp(dtnow))

fmt = '%d-%m-%Y-%H:%M:%S'
utc_dt = pytz.utc.localize(datetime.utcfromtimestamp(ts))
t_dt = utc_dt.strftime(fmt)

dtnow = datetime.strptime(t_dt,"%d-%m-%Y-%H:%M:%S")
dtxt = str(dtnow).split(".")[0]
print(dtxt,dtnow.timestamp())

utc_now = datetime.utcnow()
print("utcnow",utc_now,utc_now.timestamp())
