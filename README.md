<center>
<h1>recon365</h1>
Gather information from an email address connected to AzureAD or Office 365
<p align="center">
  <a href="#example-outputs">Example outputs</a> •
  <a href="#how-to-find-your-jwt-token">How to find your JWT token</a> •
  <a href="#usage">Usage</a> •
  <a href="#references">References</a>
</p>
</center>

## Example outputs
### Get info on on an email address in Azure AD
```console
$ python3 recon365.py --jwt token.txt --target bob.smith@company.no
[+] bob.smith@company.com 
 | tenantId          : 65443347-7d65-4339-b113-4cc43a0d7111
 | isShortProfile    : False
 | accountEnabled    : True
 | featureSettings   : {'coExistenceMode': 'TeamsOnly'}
 | userPrincipalName : bob.smith@company.com
 | givenName         : bob.smith@company.no
 | surname           :
 | email             : bob.smith@comapny.com
 | tenantName        : Company AS
 | displayName       : Bob Smith 
 | type              : Federated
 | mri               : 8:orgid:edb2cd41-315a-4a7a-8f24-690c234503fe
 | objectId          : edb2cd74-125a-4a7a-8f24-698c33d004gh
 | availability      : Offline
 | devicieType       : Mobile
```

### User with an Microsfot 356 account

```console
$ python3 recon365.py --jwt token.txt -t info@anothercompany.no
[+] info@anothercompany.no
 | skypeId           : alice-5b
 | city              : Oslo
 | state             : Oslo
 | country           : Norway
 | avatarUrl         : https://api.skype.com/users/alice-5b/profile/avatar
 | isShortProfile    : False
 | accountEnabled    : True
 | userPrincipalName : info@anothercompany.no
 | email             : info@anothercompany.no
 | displayName       : Alice Smith 
 | type              : SkypeConsumer
 | mri               : 8:alice-5b
 | availability      : PresenceUnknown
 | devicieType       : None
```

### Get info on a domain
```console
$ python3 recon365.py --target finalcompany.no
[+] finalcompany.no
 | State                   : 3
 | UserState               : 2
 | Login                   : finalcompany.no
 | NameSpaceType           : Federated
 | DomainName              : finalcompany.no
 | FederationGlobalVersion : -1
 | AuthURL                 : https://ok.finalcompany.no/adfs/ls/?username=finalcompany.no&wa=wsignin1.0&wtrealm=urn%3afederation%3aMicrosoftOnline&wctx=
 | FederationBrandName     : Final Company
 | CloudInstanceName       : microsoftonline.com
 | CloudInstanceIssuerUri  : urn:federation:MicrosoftOnline
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
  -j PATH, --jwt PATH   Path to file containing your Microsoft Teams JWT token
  -t TARGET, --target TARGET
                        Email address or domain you'd like to fetch information for
  -l FILE, --list FILE  File containing email addresses or domains you'd like to fethc information for
```

## References
- https://github.com/nyxgeek/o365recon
- https://badoption.eu/blog/2023/02/06/spoof_office_comments.html
- https://github.com/Gerenios/AADInternals
