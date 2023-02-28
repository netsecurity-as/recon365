<center>
<h1>recon365</h1>
Gather information from an email address connected to Office 365
</center>

## Example outputs
### User from external tenant
```console
$ python3 recon365.py --token teams_jwt_token.txt --email bob@example.com
Full Name          Bob Smith 
Email Address      bob@example.com
Tenant Name        Example Company
User Type          Federated
Object ID          abcabc12-ab12-ab12-ab12-abcdabcd1234
Tenant ID          afafaf89-90fa-fafa-fa23-dfad8ada8a9a
Availability       Available
Device Type        Desktop
```

### User from your own tenant
```console
$ python3 recon365.py --token teams_jwt_token.txt --email alice@othercompany.com
Full Name          Alice Smith
Email Address      alice@othercompany.com
Tenant Name        Some Other Company
User Type          ADUser
Object ID          afafaf89-90fa-fafa-fa23-dfad8ada8a9a
```

### A regular Office 365 user
Note: currently the script checks if the user has skype and then show the output according to the fetched data. I havent had the opportunity to test on a user who has not created a Skype account. So this needs a more thorough testing

```console
$ python3 recon365.py -t token.txt -e joe@gmail.com
Full Name       Joe Smith 
Email Address   joe@gmail.com
Skype ID        live:joe.smith
User Type       SkypeConsumer
```

## How to find your JWT token
Visit https://teams.microsoft.com and fetch the JWT token from the Storage. Be aware that this token may expire after around 24 hours

![](images/fetch_jwt.png)

## Usage
```console
$ python3 recon365.py --help
usage: recon365.py [options]

options:
  -h, --help            show this help message and exit
  --token PATH, -t PATH
                        Path to file containing your Microsoft Teams JWT token
  --email EMAIL, -e EMAIL
                        Email address you'd like to fetch information for
  --raw, -r             Output raw data fetched from MS Teams API (it contains more info)
```

## References
- https://github.com/nyxgeek/o365recon
- https://badoption.eu/blog/2023/02/06/spoof_office_comments.html
- https://github.com/Gerenios/AADInternals