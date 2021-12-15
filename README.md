Bitcoin SV | Next.js | API SPV Channels | Ethereum Streamed | CodeSandBox
===========

What is Bitcoin SV?
-------------------

[Bitcoin SV (Satoshi Vision)](https://bitcoinsv.io/) is the original Bitcoin.  It restores the original Bitcoin 
protocol, will keep it stable, and allow it to massively scale.  Bitcoin SV will maintain the vision set out by Satoshi 
Nakamoto’s white paper in 2008.  This Github repository provides open-source software to enable use of Bitcoin SV.

License
-------

Bitcoin SV is released under the terms of the Open BSV license. See [LICENSE](LICENSE) for more information.

Security
--------
Security is core to our values, and we value the input of security researchers acting in good faith to help us maintain 
high standards of security and privacy for our users and the Bitcoin SV blockchain.

To encourage ethical and responsible research into security vulnerabilities, the Bitcoin SV team, with support from 
Coingeek Mining, has instituted a [Responsible Disclosure Policy](doc/rdp.md).

Development Process
-------------------

This Github repository contains the source code of releases.

At this early stage in Bitcoin SV's development, we are not accepting contributions to the project. We expect this to 
change in the future.

Contacting the Bitcoin SV Team
------------------------------

If you want to report a non-confidential issue with Bitcoin SV, please use the 
[GitHub issue system](https://github.com/bitcoin-sv/bitcoin-sv/issues).

If you want to report a security vulnerability, please review the [Responsible Disclosure Policy](doc/rdp.md) and send
e-mail to <security@bitcoinsv.io>.

For any other questions or issues, please send e-mail to <support@bitcoinsv.io>.

# SPV Channels CE

Readme version 1.1.1.

| Contents | Version |
|-|-|
| SPV Channels Community Edition | 1.1.0 |

This repository contains SPV Channels CE, which is an implementation of the [BRFC specification](https://github.com/bitcoin-sv-specs/brfc-spvchannels) for SPV channels.
In addition to a server side implementation, it also contains the JavaScript client libraries for interacting with the server. See [Client libraries readme](client/javascript/readme.md) for more details about the client side libraries. 

SPV Channels provides a mechanism via which counterparties can communicate in a secure manner even in circumstances where one of the parties is temporarily offline.

## Swagger UI

The REST API can be reviewed in [Swagger UI](https://bitcoin-sv.github.io/spvchannels-reference/).

# Deploying SPV Channels CE API Server as docker containers on Linux

## Pre Requirements:
A SSL server certificate is required for installation. Obtain the certificate from your IT support team. There are are also services that issue free SSL certificates such as `letsencrypt.org`.  The certificate must be issued for the host with a fully qualified domain name. To use the server side certificate, you need to export it (including the corresponding private key) in PFX file format (*.pfx).

API Clients must trust the Certification Authority (CA) that issued the server side SSL certificate.

## Initial setup

The distribution is shared and run using Docker.

1. Open the terminal.

2. Create a directory where the spvchannels docker images, config and database will be stored (e.g. spvchannels) and navigate to it:

    ```
    mkdir spvchannels
    cd spvchannels
    ```    
   
3. Download the distribution of SPV Channels Server into the directory created in the previous step and extract the contents.

4. Check that the following files are present:

     - `docker-compose.yml`
     - `.env`
     
5. Create a `config` folder and copy the SSL server certificate file (<certificate_file_name>.pfx) into it. This server certificate is required to setup TLS (SSL).

6. Before running the SPV Channels API Server containers (spvchannels-db and spvchannels), replace some values in the `.env` file.

| Parameter | Description |
| --------- | ----------- |
|CERTIFICATEFILENAME|File name of the SSL server certificate (e.g. *<certificate_file_name.pfx>*) copied in step 5.|
|CERTIFICATESPASSWORD|Password of the *.pfx file copied in step 5.|
   > **Note:** The remaining setting are explaned in the section [Settings](#Settings).

## Running application
1. After the `.env` is set up, launch the spvchannels-db and spvchannels containers using the command:

    ```
    docker-compose up –d
    ```

The docker images as specified by the `docker-compose.yml` file, are automatically pulled from Docker Hub. 

2. Verify that all the SPV Channels Server containers are running using:

    ```
    docker ps
    ```
    The list should include `bitcoinsv/spvchannels-db` and `bitcoinsv/spvchannels`.
   
3. If everything is running you can continue to section [Account manager](#Account-manager:) to create an account.

> **Note:** If you were provided with an account id and its credentials then you can skip Setting up an account and proceed to [REST interface](#REST-interface)
## Setting up an account
To be able to call SPV Channels Server API, an account must be added into the database using the following command:

   ```
   docker exec spvchannels ./SPVChannels.API.Rest -createaccount [accountname] [username] [password]
   ```

Parameter description:

| Parameter | Description |
| ----------- | ----------- |
| [accountname] | name of the account, any whitespaces in accountname must be replaced with '_' |
| [username] | username of the account |
| [password] | password of the username |

   > **Note:** This command can also be used to add new users to an existing account (e.g. running `docker exec spvchannels ./SPVChannels.API.Rest -createaccount Accountname User1 OtherP@ssword` will return the account-id of Accountname).
## Setting up mobile push notifications
To enable mobile push notifications from SPV Channels, a Firebase service account key is required. Copy the *.json file containing the Firebase service account key into the config folder and set FIREBASECREDENTIALSFILENAME in the `.env` file.

>To get a Firebase service account *.json file, log in to your Firebase console and from Project Setting -> Service account -> Click on generate new private key. This will generate a *.json file with your Firebase service account key.

## REST interface

The reference implementation exposes different **REST APIs**:

* an API for managing channels
* an API for managing messages

This interfaces can be accessed on `https://<servername>:<port>/api/v1`. A Swagger page with the interface description can be accessed at `https://<servername>:<port>/swagger/index.html`
> **Note:** `<servername>` should be replaced with the name of the server where docker is running. `<port>` is set to 5010 by default in the `.env` file.
## Settings
| Parameter | Data type (allowed value) | Description |
| ----------- | ----------- | ----------- |
| NPGSQLLOGMANAGER | `<bool>` (`True|False`) | Enables additional database logging. Logs are in spvchannels-db container and can be accessed with the command (docker logs spvchannels-db). By default it's set to `False`. |
| HTTPSPORT | `<number>` | Port number on which SPV Channels API is running. By default it's set to `5010`. |
| CERTIFICATEFILENAME | `<text>` | File name of the SSL server certificate (e.g. *<certificate_file_name.pfx>*) |
| CERTIFICATESPASSWORD | `<text>` | Password of the *.pfx file |
| NOTIFICATIONTEXTNEWMESSAGE | `<text>` | Notification text upon arrival of a new message. By default it's set to `New message arrived`. |
| MAXMESSAGECONTENTLENGTH | `<number>` | Maximum size of any single message in bytes. By default it's set to its maximum size `65536`. |
| CHUNKEDBUFFERSIZE | `<number>` | If a message is sent in chunks, this sets the size of a chunk. By default it's set to `1024`. |
| TOKENSIZE | `<number>` | Length of bearer token. By default it's set to `64`. |
| CACHESIZE | `<number>` | Number of records in memorycache. By default it's set to `1048576`. |
| CACHESLIDINGEXPIRATIONTIME | `<number>` | Time in which a record is removed from memorycache if it is not accessed. By default it's set to `60` seconds. |
| CACHEABSOLUTEEXPIRATIONTIME | `<number>` | Time in which a record is removed from memorycache. By default it's set to `600` secunds. |
| FIREBASECREDENTIALSFILENAME | `<text>` | Fully qualified file name of the Firebase service account key. This setting is only required if you wish to enable mobile push notifications. See [Setting up mobile push notifications](#Setting-up-mobile-push-notifications)

## Terminating application

1. Open the terminal and navigate to spvchannels folder:

    ```
    cd spvchannels
    ```

2. To shutdown SPV Channels Server containers use the following command:

    ```
    docker-compose down
    ```

# This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `pages/index.js`. The page auto-updates as you edit the file.

[API routes](https://nextjs.org/docs/api-routes/introduction) can be accessed on [http://localhost:3000/api/hello](http://localhost:3000/api/hello). This endpoint can be edited in `pages/api/hello.js`.

The `pages/api` directory is mapped to `/api/*`. Files in this directory are treated as [API routes](https://nextjs.org/docs/api-routes/introduction) instead of React pages.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Codesandbox

The easiest way to deploy your Next.js app is to use the [codesandbox](https://codesandbox.io/) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.<p></p>

<p>© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
