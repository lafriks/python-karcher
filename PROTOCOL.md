# Karcher Home Robot protocol

## Servers

* Europe - https://eu-appaiot.3irobotix.net
* USA - https://us-appaiot.3irobotix.net
* China - https://cn-appaiot.3irobotix.net

## Constants

wifiSSIDPrefix = "iPlus"
projectType = "android_iot.karcher"
tenantId = "1528983614213726208"
version = "v1"
zone = "GBR"

### Products

* RCV3 - `1528986273083777024`
* RCV5 - `1540149850806333440`
* RCF5 - `1599715149861306368`

## Work mode

* Idle - 0, 35, 85, 29, 40, 14, 23
* Pause - 4, 31, 82, 27, 37, 9
* Cleaning - 1, 30, 81, 25, 36, 7
* Working - Cleaning || Pause
* GoHome - 5, 10, 11, 12, 21, 26, 32, 47, 38

## Encryption

AES-128-ECB
Key = hex(md5(tenantId))[8:24]

Example `0310abafaa3a2268`

## Default headers

* `User-Agent: Android_<tenantId>`
* `authorization: <user-auth>` - If authorized
* `id: <user-id>` - If authorized
* `tenantId: <tenantId>`
* `sign: <signature>`
* `ts: <unix-timestamp>`
* `nonce: <randstr-32>`

`randstr-32` - random string of 32 characters from set `123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`
`request-data` - for `GET` URL decoded values, for `POST` or `PUT` - JSON values without keys, only data

`signature` = md5(`user-auth`+`unix-timestamp`+`randstr-32`+`request-data`)

## Error response

Commonly in case of error API returns status code 200 with following JSON data:

* `code` - 0 for success, or other codes for errors
* `msg` - Error message

### Error codes

* `0` - Success
* `608` - Forbidden
* `609` - Unauthorized or authorization expired, please log in again
* `612` - Parameter validity verification failed
* `613` - Invalid token
* `620` - The username or password is incorrect
* `889` - Signature error (sign)
* `890` - Signature error (ts)
* `891` - Signature error (nonce)
* `892` - Signature error (genSign)

## Methods

### Get base URLs

The default general address delivery.

`GET /network-service/domains/list`

Parameters:

* `tenantId` - Tenant ID
* `productModeCode` - Project type
* `version` - Version

Response:

* `code` - Status code
* `result` - Result
  * `domain` - Encrypted domain JSON
  * `tenantId` - Tenant ID
  * `productModeCode` - Project type
  * `remarks` - Additional information

Domain JSON:

* `MQTT` - MQTT server address
* `MQTT_ga`
* `APP_api` - API server address
* `APP_cdn`
* `MAP_cdn`
* `DEV_api`
* `DEV_ota`
* `APP_log`
* `dev_log`
* `APP_api_CDN`
* `DEV_api_CDN`
* `DEV_ota_CDN`
* `image`
* `video`
* `update_package`
* `all`

Example request:

```http
GET https://eu-appaiot.3irobotix.net/network-service/domains/list?tenantId=1528983614213726208&productModeCode=android_iot.karcher&version=v1
Content-Type: application/x-www-form-urlencoded
Domain-Name: originalUrl
```

### Login

User authorization.

`POST /user-center/auth/login`

Request JSON:

* `tenantId` - Tenant ID
* `lang` - Language code
* `token` - Token (for token authorization)
* `userId` - User ID (for code authorization)
* `authcode` - Authorization code (for code authorzation)
* `username` - Encrypted username (email)
* `password` - Encrypted password
* `projectType` - Project type
* `versionCode` - Application version code ex `10004`
* `versionName` - Application version ex `1.0.4`
* `phoneBrand` - Encrypted phone brand and model with underscore separator ex `xiaomi_mi 9`
* `phoneSys` - Constant value `1`
* `noticeSetting` - notification settings
  * `andIpad` - registration ID (random string 19 characters in length)
  * `android` - registration ID (random string 19 characters in length)

Response JSON:

* `data`:
  * `AUTH` - Authorization token
  * `EMQ_TOKEN` - MQTT token
  * `TENANT_ID` - Tenant ID
  * `USERNAME` - Encrypted username
  * `CONNECTION_TYPE` - Connection type ex `user`
  * `PROJECT_TYPE` - Project type
  * `ROBOT_TYPE` - Robot type ex `user`
  * `LANG` - Language code
  * `COUNTRY_CITY` - JSON encoded location data
    * `continent` - Continent
    * `country` - Country
    * `city` - City
  * `BETA_FLAG` - Has beta access: `0` - no beta access
* `clientType` - Client type ex `PHONE`
* `id` - User ID

### Get user devices

Get list of all user devices.

`GET /smart-home-service/smartHome/user/getDeviceInfoByUserId/{userID}`

Request parameters:

* `userID` - user identifier

Response JSON:

* List of devices
  * `deviceId` - Device identifier
  * `sn` - Device serial number
  * `mac` - Device network MAC address
  * `nickname` - Device name
  * `versions` - List of firmware versions
    * `packageType`
    * `version` - Numeric version number
    * `version_name` - Version number
    * `ctrl_version` - Control version number
  * `status` - Status (0 - offline, 1 - online)
  * `isDefault` - Default device
  * `isSelected` - Device selected
  * `isShare` - Device shared
  * `onlineTime` - Unix time miliseconds when was online
  * `photoUrl` - URL of product image
  * `productId` - Product identifier
  * `productModeCode` - Product name
  * `roomId` - Current room identifier
  * `bindTime` - Bind time unix miliseconds
  * `shareList` - Share history
