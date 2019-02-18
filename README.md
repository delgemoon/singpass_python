# singpass_python

## singpass_python Demo App Setup

### 1.1 Install python and virtual env

In order for the demo application to run locally, you will need to install python 3.7, pip, and virtualenv.

Follow the instructions given by the links below depending on your OS.

- [Install Node and NPM for Windows](http://blog.teamtreehouse.com/install-node-js-npm-windows)
- [Install Node and NPM for Linux](http://blog.teamtreehouse.com/install-node-js-npm-linux)
- [nstall Node and NPM for Mac](http://blog.teamtreehouse.com/install-node-js-npm-mac)

### 1.2 Start the Application

**For Linux/MacOS**

Execute the following command to start the application:
```
  ./start.sh
```


**Access the Application on Your Browser**
You should be able to access the sample application via the following URL:

```
http://localhost:3001
```

---
## Login with SingPass

Use this test ID and password to login to SingPass:

NRIC: ``S9812381D``
Password: ``MyInfo2o15``

Other users can be found here
https://www.ndi-api.gov.sg/assets/lib/trusted-data/myinfo/downloads/myinfo-test-profiles.xlsx

A dashboard will appear, You need to copy the access request link to give
to those who you want to collect information. After they give their consent, you can 
see their info on your dashboard.

---
## Enable PKI Digital Signature

<span style="color:red">
<strong>Note:</strong> <br>
As of version 2.2.0 of our API specifications, the URLs of the APIs have changed.
Please note the different configurations accordingly.
</span>


### v2.2 APIs (LATEST)

**For Linux/MacOS**

Edit the ``start.sh``. Look for ``SANDBOX ENVIRONMENT``, Comment out these configurations,
```
# SANDBOX ENVIRONMENT (no PKI digital signature)
# export AUTH_LEVEL=L0
# export MYINFO_API_AUTHORISE='https://sandbox.api.myinfo.gov.sg/com/v2/authorise'
# export MYINFO_API_TOKEN='https://sandbox.api.myinfo.gov.sg/com/v2/token'
# export MYINFO_API_PERSON='https://sandbox.api.myinfo.gov.sg/com/v2/person'
```

Look for ``TEST ENVIRONMENT``, uncomment these configurations,
```
# TEST ENVIRONMENT (with PKI digital signature)
export AUTH_LEVEL=L2
export MYINFO_API_AUTHORISE='https://test.api.myinfo.gov.sg/com/v2/authorise'
export MYINFO_API_TOKEN='https://test.api.myinfo.gov.sg/com/v2/token'
export MYINFO_API_PERSON='https://test.api.myinfo.gov.sg/com/v2/person'
```
Execute the following command to start the application:
```
  ./start.sh
```

