# -*- coding: utf-8 -*-
"""MMSI_to_vessel_type.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XaNsflNJ552WJ_6HBplr4Kgm86dH4WzL
"""

# importing module
from pandas import *
 
# reading CSV file
data = read_csv("unique_mmsi_csv.csv")
 
# converting column data to list
mmsi = data['mmsi'].tolist()

# printing list data
print('mmsi:', mmsi)

import requests
count = 0
vessel_type = []
gear_type = []
flag = []
score = []

for x in mmsi:
  # API Request last mai dekh imo[0] hai usse apan imo ki list se uska mmsi search karenge, isko loop mai daalna hai for every element of the imo list
  response = requests.get(f"https://gateway.api.globalfishingwatch.org//v2/vessels/search?query="+str(x)+"&limit=10&datasets=public-global-support-vessels:latest,public-global-carrier-vessels:latest,public-global-fishing-vessels:latest&offset=0",
  headers={
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpZEtleSJ9.eyJkYXRhIjp7Im5hbWUiOiJpdXVfZmlzaGluZyIsInVzZXJJZCI6MTk4NDEsImFwcGxpY2F0aW9uTmFtZSI6Iml1dV9maXNoaW5nIiwiaWQiOjMyNSwidHlwZSI6InVzZXItYXBwbGljYXRpb24ifSwiaWF0IjoxNjY3NjUxMzk2LCJleHAiOjE5ODMwMTEzOTYsImF1ZCI6ImdmdyIsImlzcyI6ImdmdyJ9.En37YiQThXrQ36FPR1yeBeQnw2RVS6JggAL56HEO5eXOmV39R0xUAQWYYghxj8lcdx5vOlN-mzHR8H_ODjy6dMoyhiaccpD6NoJ3esUZ_V6Xjqvrt69Ld0aB_fVJ8Sqo1_tKVsUX5wxCYguW5Yxn2TE0Xxa5FVSVdh1O_N1AhIP7U428UGzKLHeK1ZmPlGxcdcQKHMH36luC8r1FBOVzvXiYq6pv7tV_KvLYUmT5_6Rq3iICvoQMXaujx6kYbFcdy0wuKoQu-lkrv_r21FXNtANfoKxOvdz0OKkNdcz1i1PGLSViv_uWn_5d_KlOzsMO9PdR1CWIfq72AMLX9E9GlpxU7hUJwv_SUmt7XtO17uZMs8Zuc2DqxkH6RYa2Dar2jNAxDfHIBTmNb6MgjqXEEcm0INoHBXE7iij6Rq5rfrPbWd1RM-Ey3dcMxMO5RSQ2YtSABrmYkmbpdV0gwyxS_cq0Poi0dqBua4kJl2nXzxvf18Cq9GUeqUgLd_7Jowkq"
  }
  )

  # poora response print ke liye
  # print(response.json())
  # siraf mmsi print karne ke liye, isko variable mai daalke list mai append kar denge
  print(count)
  count = count + 1
  if len(response.json()["entries"]) > 0:
    if response.json()["entries"][0]['vesselType']:
      temp = response.json()["entries"][0]['vesselType']
    else:
      temp = 'other'
    
    if response.json()["entries"][0]['flag']: 
      temp1 = response.json()["entries"][0]['flag']
    else:
      temp1 = 'other'  
    
    if response.json()["entries"][0]['score']:
      temp2 = response.json()["entries"][0]['score']
    else:
      temp2 = 0

    if response.json()["entries"][0]['geartype']: 
      temp3 = response.json()["entries"][0]['geartype']
    else:
      temp3 = 'other'
  else:
    temp = 'other'
    temp1 = 'other'
    temp2 = 0
    temp3 = 'other'
  
  vessel_type.append(temp)
  flag.append(temp1)
  score.append(temp2)
  gear_type.append(temp3)
  
  print("vessel type = ",temp," | flag = ",temp1," | score = ",temp2," | gear_type = ",temp3)

print(gear_type)

import pandas as pd    

df = pd.DataFrame(vessel_type)
df.to_csv('vessel_type.csv', index=False)

df1 = pd.DataFrame(flag)
df1.to_csv('flag.csv', index=False)

df2 = pd.DataFrame(score)
df2.to_csv('score.csv', index=False)

df3 = pd.DataFrame(gear_type)
df3.to_csv('gear_type.csv', index=False)

# API request for single mmsi (for testing the response)

import requests
print(mmsi[48])

response = requests.get(f"https://gateway.api.globalfishingwatch.org//v2/vessels/search?query="+str(mmsi[49])+"&limit=1&datasets=public-global-support-vessels:latest,public-global-carrier-vessels:latest,public-global-fishing-vessels:latest&offset=0",
headers={
  "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpZEtleSJ9.eyJkYXRhIjp7Im5hbWUiOiJpdXVfZmlzaGluZyIsInVzZXJJZCI6MTk4NDEsImFwcGxpY2F0aW9uTmFtZSI6Iml1dV9maXNoaW5nIiwiaWQiOjMyNSwidHlwZSI6InVzZXItYXBwbGljYXRpb24ifSwiaWF0IjoxNjY3NjUxMzk2LCJleHAiOjE5ODMwMTEzOTYsImF1ZCI6ImdmdyIsImlzcyI6ImdmdyJ9.En37YiQThXrQ36FPR1yeBeQnw2RVS6JggAL56HEO5eXOmV39R0xUAQWYYghxj8lcdx5vOlN-mzHR8H_ODjy6dMoyhiaccpD6NoJ3esUZ_V6Xjqvrt69Ld0aB_fVJ8Sqo1_tKVsUX5wxCYguW5Yxn2TE0Xxa5FVSVdh1O_N1AhIP7U428UGzKLHeK1ZmPlGxcdcQKHMH36luC8r1FBOVzvXiYq6pv7tV_KvLYUmT5_6Rq3iICvoQMXaujx6kYbFcdy0wuKoQu-lkrv_r21FXNtANfoKxOvdz0OKkNdcz1i1PGLSViv_uWn_5d_KlOzsMO9PdR1CWIfq72AMLX9E9GlpxU7hUJwv_SUmt7XtO17uZMs8Zuc2DqxkH6RYa2Dar2jNAxDfHIBTmNb6MgjqXEEcm0INoHBXE7iij6Rq5rfrPbWd1RM-Ey3dcMxMO5RSQ2YtSABrmYkmbpdV0gwyxS_cq0Poi0dqBua4kJl2nXzxvf18Cq9GUeqUgLd_7Jowkq"
}
)

# poora response print ke liye
print(response.json())
# siraf mmsi print karne ke liye, isko variable mai daalke list mai append kar denge
temp = response.json()["entries"][0]['vesselType'] if len(response.json()["entries"]) > 0 else 'other'
print(temp)