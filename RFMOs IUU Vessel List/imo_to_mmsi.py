# -*- coding: utf-8 -*-
"""IMO_to_MMSI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WCtrMOIE04xBuI8uNqiuLqofqWEzeHz6
"""

# importing module
from pandas import *
 
# reading CSV file
data = read_csv("IMO_List_IUU_20220803.csv")
 
# converting column data to list
imo = data['IMO'].tolist()

# printing list data
print('IMO:', imo)

import requests

mmsi = []

for x in imo:
  # API Request last mai dekh imo[0] hai usse apan imo ki list se uska mmsi search karenge, isko loop mai daalna hai for every element of the imo list
  response = requests.get(f"https://gateway.api.globalfishingwatch.org/v2/vessels/advanced-search?datasets=public-global-carrier-vessels:latest,public-global-fishing-vessels:latest,public-global-support-vessels:latest&query=imo%20%3D%20%27"+str(x)+"%27&limit=1&offset=0",
  headers={
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpZEtleSJ9.eyJkYXRhIjp7Im5hbWUiOiJpdXVfZmlzaGluZyIsInVzZXJJZCI6MTk4NDEsImFwcGxpY2F0aW9uTmFtZSI6Iml1dV9maXNoaW5nIiwiaWQiOjMyNSwidHlwZSI6InVzZXItYXBwbGljYXRpb24ifSwiaWF0IjoxNjY3NjUxMzk2LCJleHAiOjE5ODMwMTEzOTYsImF1ZCI6ImdmdyIsImlzcyI6ImdmdyJ9.En37YiQThXrQ36FPR1yeBeQnw2RVS6JggAL56HEO5eXOmV39R0xUAQWYYghxj8lcdx5vOlN-mzHR8H_ODjy6dMoyhiaccpD6NoJ3esUZ_V6Xjqvrt69Ld0aB_fVJ8Sqo1_tKVsUX5wxCYguW5Yxn2TE0Xxa5FVSVdh1O_N1AhIP7U428UGzKLHeK1ZmPlGxcdcQKHMH36luC8r1FBOVzvXiYq6pv7tV_KvLYUmT5_6Rq3iICvoQMXaujx6kYbFcdy0wuKoQu-lkrv_r21FXNtANfoKxOvdz0OKkNdcz1i1PGLSViv_uWn_5d_KlOzsMO9PdR1CWIfq72AMLX9E9GlpxU7hUJwv_SUmt7XtO17uZMs8Zuc2DqxkH6RYa2Dar2jNAxDfHIBTmNb6MgjqXEEcm0INoHBXE7iij6Rq5rfrPbWd1RM-Ey3dcMxMO5RSQ2YtSABrmYkmbpdV0gwyxS_cq0Poi0dqBua4kJl2nXzxvf18Cq9GUeqUgLd_7Jowkq"
  }
  )

  # poora response print ke liye
  # print(response.json())
  # siraf mmsi print karne ke liye, isko variable mai daalke list mai append kar denge
  temp = response.json()["entries"][0]['mmsi'] if len(response.json()["entries"]) > 0 else 0
  mmsi.append(temp)

print(mmsi)

import pandas as pd    

df = pd.DataFrame(mmsi)
df.to_csv('mmsi_iuu_20220803.csv', index=False)