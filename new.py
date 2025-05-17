import pandas as pd
from io import StringIO

# Seu dado original como string (pode ser lido de um arquivo em vez disso)
raw_data = """
request_per_hour, data
1,14/Apr/2025:00
6,14/Apr/2025:01
6 14/Apr/2025:02
12 14/Apr/2025:11
12 14/Apr/2025:12
7 14/Apr/2025:14
1 14/Apr/2025:15
6 14/Apr/2025:16
30 14/Apr/2025:17
17 14/Apr/2025:18
4 14/Apr/2025:19
9 14/Apr/2025:22
15 14/Apr/2025:23
10 15/Apr/2025:00
10 15/Apr/2025:02
2 15/Apr/2025:04
2 15/Apr/2025:09
6 15/Apr/2025:11
3 15/Apr/2025:12
4 15/Apr/2025:13
4 15/Apr/2025:14
12 15/Apr/2025:17
13 15/Apr/2025:18
2 15/Apr/2025:19
1 15/Apr/2025:20
22 15/Apr/2025:22
1 15/Apr/2025:23
4 16/Apr/2025:00
1 16/Apr/2025:01
1 16/Apr/2025:02
1 16/Apr/2025:03
2 16/Apr/2025:04
6 16/Apr/2025:06
1 16/Apr/2025:07
1 16/Apr/2025:09
4 16/Apr/2025:10
12 16/Apr/2025:11
13 16/Apr/2025:12
51 16/Apr/2025:13
80 16/Apr/2025:14
53 16/Apr/2025:15
10 16/Apr/2025:16
18 16/Apr/2025:17
6 16/Apr/2025:18
22 16/Apr/2025:19
2 16/Apr/2025:20
5 16/Apr/2025:21
11 16/Apr/2025:22
10 17/Apr/2025:00
9 17/Apr/2025:01
6 17/Apr/2025:02
4 17/Apr/2025:03
1 17/Apr/2025:04
27 17/Apr/2025:10
12 17/Apr/2025:12
4 17/Apr/2025:13
8 17/Apr/2025:16
10 17/Apr/2025:19
5 17/Apr/2025:21
4 18/Apr/2025:03
2 18/Apr/2025:19
46 18/Apr/2025:20
4 18/Apr/2025:23
9 19/Apr/2025:00
1 19/Apr/2025:04
4 19/Apr/2025:05
1 19/Apr/2025:06
2 19/Apr/2025:08
4 19/Apr/2025:11
4 19/Apr/2025:13
4 19/Apr/2025:14
3 19/Apr/2025:15
2 19/Apr/2025:16
2 19/Apr/2025:17
34 19/Apr/2025:21
4 20/Apr/2025:00
4 20/Apr/2025:01
1 20/Apr/2025:04
1 20/Apr/2025:11
6 20/Apr/2025:13
6 20/Apr/2025:14
2 20/Apr/2025:18
2 21/Apr/2025:03
1 21/Apr/2025:07
3 21/Apr/2025:08
4 21/Apr/2025:10
5 21/Apr/2025:11
7 21/Apr/2025:12
12 21/Apr/2025:13
1 21/Apr/2025:14
1 21/Apr/2025:15
6 21/Apr/2025:16
2 21/Apr/2025:17
4 21/Apr/2025:18
22 21/Apr/2025:19
1 21/Apr/2025:22
9 21/Apr/2025:23
6 22/Apr/2025:00
3 22/Apr/2025:03
2 22/Apr/2025:05
13 22/Apr/2025:07
22 22/Apr/2025:08
8 22/Apr/2025:12
5 22/Apr/2025:13
6 22/Apr/2025:14
2 22/Apr/2025:15
4 22/Apr/2025:16
8 22/Apr/2025:19
20 22/Apr/2025:20
12 22/Apr/2025:21
16 22/Apr/2025:22
4 23/Apr/2025:00
2 23/Apr/2025:01
2 23/Apr/2025:02
5 23/Apr/2025:03
1 23/Apr/2025:04
16 23/Apr/2025:07
2 23/Apr/2025:08
15 23/Apr/2025:11
199 23/Apr/2025:12
232 23/Apr/2025:13
7 23/Apr/2025:14
30 23/Apr/2025:15
4 23/Apr/2025:16
12 23/Apr/2025:17
86 23/Apr/2025:18
6 23/Apr/2025:19
78 23/Apr/2025:20
23 23/Apr/2025:21
12 23/Apr/2025:22
12 23/Apr/2025:23
21 24/Apr/2025:00
4 24/Apr/2025:01
4 24/Apr/2025:02
4 24/Apr/2025:10
10 24/Apr/2025:11
75 24/Apr/2025:12
125 24/Apr/2025:13
229 24/Apr/2025:14
197 24/Apr/2025:15
301 24/Apr/2025:16
269 24/Apr/2025:17
1204 24/Apr/2025:18
101 24/Apr/2025:19
99 24/Apr/2025:20
100 24/Apr/2025:21
168 24/Apr/2025:22
116 24/Apr/2025:23
69 25/Apr/2025:00
139 25/Apr/2025:01
64 25/Apr/2025:02
18 25/Apr/2025:03
16 25/Apr/2025:04
2 25/Apr/2025:05
11 25/Apr/2025:06
16 25/Apr/2025:08
1 25/Apr/2025:09
168 25/Apr/2025:10
48 25/Apr/2025:11
91 25/Apr/2025:12
101 25/Apr/2025:13
60 25/Apr/2025:14
20 25/Apr/2025:15
60 25/Apr/2025:16
58 25/Apr/2025:17
80 25/Apr/2025:18
93 25/Apr/2025:19
100 25/Apr/2025:20
29 25/Apr/2025:21
43 25/Apr/2025:22
32 25/Apr/2025:23
4 26/Apr/2025:00
22 26/Apr/2025:01
112 26/Apr/2025:02
7 26/Apr/2025:03
4 26/Apr/2025:06
2 26/Apr/2025:09
4 26/Apr/2025:11
55 26/Apr/2025:12
62 26/Apr/2025:13
80 26/Apr/2025:14
1000 26/Apr/2025:15
23 26/Apr/2025:16
5 26/Apr/2025:17
35 26/Apr/2025:18
6 26/Apr/2025:19
29 26/Apr/2025:20
8 26/Apr/2025:21
4 26/Apr/2025:23
2 27/Apr/2025:00
4 27/Apr/2025:01
39 27/Apr/2025:02
6 27/Apr/2025:03
2 27/Apr/2025:06
3 27/Apr/2025:07
6 27/Apr/2025:10
8 27/Apr/2025:11
4 27/Apr/2025:12
3 27/Apr/2025:13
4 27/Apr/2025:14
16 27/Apr/2025:15
5 27/Apr/2025:16
8 27/Apr/2025:19
2 27/Apr/2025:21
9 27/Apr/2025:22
6 27/Apr/2025:23
10 28/Apr/2025:00
4 28/Apr/2025:04
7 28/Apr/2025:09
2 28/Apr/2025:12
26 28/Apr/2025:13
61 28/Apr/2025:14
36 28/Apr/2025:15
42 28/Apr/2025:16
19 28/Apr/2025:17
31 28/Apr/2025:18
"""

rows = []
for line in raw_data.strip().splitlines():
    parts = line.split(",", 1) if "," in line else line.split(None, 1)
    if len(parts) != 2:
        continue
    req_str, dt_str = parts
    # pula cabeçalho ou linhas não numéricas
    if not req_str.isdigit():
        continue
    rows.append({
        "request_per_hour": int(req_str),
        "datetime_str": dt_str
    })

df = pd.DataFrame(rows)

# converte a coluna de texto para datetime
df["datetime"] = pd.to_datetime(df["datetime_str"], format="%d/%b/%Y:%H")

# extrai dia, mês, ano e hora em colunas separadas
df["day"]   = df["datetime"].dt.day
df["month"] = df["datetime"].dt.month
df["year"]  = df["datetime"].dt.year
df["hour"]  = df["datetime"].dt.hour

# seleciona apenas as colunas finais
df_final = df[["request_per_hour", "day", "month", "year", "hour"]]
df_final.to_csv('requests.csv',index=False)