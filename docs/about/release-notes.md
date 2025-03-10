## Version 0.3.11

- Added support for passing the string value of "all" to a commit to specify all admin users.

## Version 0.3.10

- Added support for new security rule types of SWG by allowing the `device` field to be either string or dictionary

## Version 0.3.9

- Added support for NAT rules

## Version 0.3.8

- Added support remote networks
- First time to leverage SASE APIs until Remote Network endpoints for SCM API are working properly

## Version 0.3.7

- Added support HIP objects

## Version 0.3.6

- Auto-paginiation when using the `list()` method
- Support for controlling the maximum amount of objects returned in a request (default: 2500, max: 5000)

## Version 0.3.5

- Added support performing advanced filtering capabilities

## Version 0.3.4

- Added support for External Dynamic Lists
- Added support for Auto Tag Actions (not yet supported by API)

## Version 0.3.3

- Added support for URL Categories

---

## Version 0.3.2

- Added support for performing commits
- Added support for pulling in job status

---

## Version 0.3.1

- Added support for Service Group objects

---

## Version 0.3.0

- Refactored Exceptions
- Refactored logging
- Updated tests
- Addressed issue with refresh_token of oauth client
- Added support for tag objects
- `fetch()` returns a Pydantic modeled object now
- `update()` supports passing of Pydantic modeled objects

---

## Version 0.2.2

- Dropped dependency version on crypto package.

### Updates:

* Drop dependency version on crypto package

---

## Version 0.2.1

- Added client-side filtering to address list method.
- Refactored address object management and enhanced error handling.
- Introduced `BadResponseError` for invalid API responses.
- Improved address and address group tests with better validation.
- Enhanced error handling across Address and Application modules.

## Version 0.2.0

- Added `fetch` method to various profile and object classes.
- Refactored update methods to use `data['id']` directly.
- Introduced `AntiSpywareProfileUpdateModel`.
- Improved error type extraction logic in client.
- Refactored Address models for separate base, create, update, and response logic.

## Version 0.1.17

- **Added `move` method**: Enable moving security rules within the rule base.

## Version 0.1.16

- **Updated `create` method**: Ensured missing dictionary keys are set with default values.

## Version 0.1.15

- **Updated pattern**: Supported periods (.) in security policy names.

## Version 0.1.14

- **Added Security Rules**: Introduced support for Security Rules configuration.

## Version 0.1.13

- **Added Decryption Profiles**: Introduced support for Decryption Profiles.

## Version 0.1.12

- **Added DNS Security Profiles**: Introduced support for DNS Security Profiles.

## Version 0.1.11

- **Added Vulnerability Protection Profiles**: Introduced support for Vulnerability Protection Profiles.

## Version 0.1.10

- **Bug Fix**: Supported empty API responses for PUT updates.

## Version 0.1.9

- **Wildfire Antivirus**: Added support for managing Wildfire Anti-Virus Security Profiles.

## Version 0.1.8

- **Pytests**: Added tests to support Anti Spyware Profiles.

## Version 0.1.7

- **Anti Spyware Profiles**: Enabled support for Anti Spyware Profiles.

## Version 0.1.6

- **Logging**: Changed default logging level to INFO.

## Version 0.1.5

- **Added Address Groups**: Enabled support for Address Groups.
- **Docs Update**: Updated the mkdocs site.

## Version 0.1.4

- **Added Services**: Enabled support for Services.
- **Docs Update**: Updated the mkdocs site.

## Version 0.1.3

- **Added Applications**: Enabled support for Applications.
- **Docs Update**: Revamped README and mkdocs site.

## Version 0.1.2

- **Refactoring Names**: Simplified naming conventions across the project.

## Version 0.1.1

- **Refactor**: Transitioned the project to an object-oriented structure.

## Version 0.1.0

- **Initial Release**: Developer version of `pan-scm-sdk`.

---

For more detailed information on each release, visit
the [GitHub repository](https://github.com/cdot65/pan-scm-sdk/releases) or check
the [commit history](https://github.com/cdot65/pan-scm-sdk/commits/main).