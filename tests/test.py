import requests
import pandas as pd

base_url = 'http://localhost:5000/'

login_url = f'{base_url}/login'
credentials = {"username":"username","password":"password"}
response = requests.post(login_url,json=credentials)
print(response.json())
token = response.json().get('access_token')
input()

upload_data = f'{base_url}/upload-data'
csv_path = r'ROUTE_TO_YOUR_FILE.csv'
files = {'csv_file': (open(csv_path, 'rb'))}
headers = {'Authorization': f'Bearer {token}'}
params = {'enable_max_rows':'yes'}
response = requests.post(upload_data, files=files, headers=headers, params=params)
print(response.json())
input()

#For multiple csv
#upload_data = f'{base_url}/upload-data'
#csv_path = r'ROUTE_TO_YOUR_FILE.csv'
#csv_files = glob.glob(os.path.join(csv_path, '*.csv'))

#for i in csv_files:
    #files = {'csv_file': (open(i, 'rb'))}
    #headers = {'Authorization': f'Bearer {token}'}
    #params = {'enable_max_rows':'yes'}
    #response = requests.post(upload_data, files=files, headers=headers, params=params)
    #print(response.json())
    #input()

hired_by_q_url = f'{base_url}/hired_employees_2021_q'
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(hired_by_q_url, headers=headers)
data = response.json()
df = pd.DataFrame(data['data'])
print(df)
input()

hired_by_dept_2021 = f'{base_url}/hired_by_dept_2021'
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(hired_by_dept_2021, headers=headers)
data = response.json()
df = pd.DataFrame(data['data'])
print(df)
