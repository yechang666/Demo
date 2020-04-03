import pandas as pd
import numpy as np
import json
dd1 = {
    "id":123,
    "name":[{'status':{'jack','make'}},{'isis':{'mak','kit'}}],
	"sex":'男'
}
dd = json.dumps(dd1)
print(dd)