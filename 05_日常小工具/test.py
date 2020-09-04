import pandas as pd
data = []

s1 = data["PicFixationDuration"].value_counts()
s2 = data["WordFixationDuration"].value_counts()
result = pd.DataFrame(list(zip(s1,s2)))
print(result)