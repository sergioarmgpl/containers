from datetime import timezone
import pytz
from datetime import datetime
country = pytz.timezone("America/Guatemala")
dtnow = datetime.now(country)
dtnow2 = dtnow.replace(tzinfo=timezone.utc)
print(dtnow,dtnow2)
