# REST API example application

This is a barebones example of an RESTful api made in python for uploading csv data to a SQL database.
Can be used for multiple or simple upload and can upload more than 1000 rows.

The entire application is contained within `main.py`.
`test.py` is made for testing and example-wise only.

Remember to run `requirements.txt` first for library updating.

# Properties

- Upload CSV data
- Process and store data into SQL tables
- Query and get data in JSON format

# Requirements

- Python 3.x

# Run the app

1. Clone the repo locally.
2. Run `requirements.txt`

`bash` 

    pip install -r requirements.txt

4. Run main.py

The app will be hosted over http://localhost:5000

# Examples

The API has a validation module which queries the SQL database in order to get validation for allowed users remember to first
create said table and/or modify the access rules you preffer.

`bash`

    curl -X POST -d "username=username&password=password" http://localhost:5000/login

Once the token is recieved remember to include it in every request until session ends

Remember you can disable 1000 rows limiter with parameter "enable_max_rows=yes"

`bash`

    curl -H "Authorization: Bearer <TOKEN>" -X POST -d "enable_max_rows=yes" -F "csv_file=@myfile.csv" http://localhost:5000/upload-data

And finally you can query the data previously worked out in the SQL database

`bash`

    curl -H "Authorization: Bearer <TOKEN>" -X GET -F "csv_file=@myfile.csv" http://localhost:5000/upload-data

# Contribute

Contributions are welcome! Remember to follow the usual steps:

1. Create a fork
2. Clone the fork locally
3. Modify and test
4. Send Pull Request to this repo
