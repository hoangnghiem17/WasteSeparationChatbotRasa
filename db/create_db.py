import pandas as pd
import sqlite3

df = pd.read_excel('db/AbfallABC_RecyclingZentrumFrankfurt.xlsx')

conn = sqlite3.connect('abfallABC_entsorgung.db')
df.to_sql('abfallABC_entsorgung', conn, if_exists='replace', index=False)
conn.close()
