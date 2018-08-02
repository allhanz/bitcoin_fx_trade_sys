from yahoo_finance import Share
import pandas as pd
import os
yahoo=Share("YHOO")
print(yahoo.get_open())
