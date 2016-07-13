import pandas as pd
from yhat.utils import create_tests

# df = pd.read_csv('./wrk_results.csv')
df = pd.DataFrame({
    'title': ["harry potter", "war and peace", "lord of the rings"],
    'pages': ["800", "875", "500"]
  })


create_tests(df, "myclientresults.ldjson")
