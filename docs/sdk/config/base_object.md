# Base Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [Base Object Attributes](#base-object-attributes)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
    - [Creating Objects](#creating-objects)
    - [Retrieving Objects](#retrieving-objects)
    - [Updating Objects](#updating-objects)
    - [Listing Objects](#listing-objects)
    - [Deleting Objects](#deleting-objects)
7. [Managing Configuration Changes](#managing-configuration-changes)
    - [Performing Commits](#performing-commits)
    - [Monitoring Jobs](#monitoring-jobs)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Full Script Examples](#full-script-examples)
11. [Related Models](#related-models)

## Overview

The `BaseObject` class serves as the foundation for all configuration objects in Palo Alto Networks' Strata Cloud
Manager.
This class provides standardized CRUD operations (Create, Read, Update, Delete) and job management functionality that is
inherited by all configuration object types.

## Core Methods

| Method             | Description                   | Parameters                                           | Return Type             |
|--------------------|-------------------------------|------------------------------------------------------|-------------------------|
| `create()`         | Creates new object            | `data: Dict[str, Any]`                               | `Dict[str, Any]`        |
| `get()`            | Retrieves object by ID        | `object_id: str`                                     | `Dict[str, Any]`        |
| `update()`         | Updates existing object       | `data: Dict[str, Any]`                               | `Dict[str, Any]`        |
| `delete()`         | Deletes object                | `object_id: str`                                     | `None`                  |
| `list()`           | Lists objects with filtering  | `**filters`                                          | `List[Dict[str, Any]]`  |
| `list_jobs()`      | Lists jobs with pagination    | `limit: int`, `offset: int`, `parent_id: str`        | `JobListResponse`       |
| `get_job_status()` | Gets job status               | `job_id: str`                                        | `JobStatusResponse`     |
| `commit()`         | Commits configuration changes | `folders: List[str]`, `description: str`, `**kwargs` | `CandidatePushResponse` |

## Base Object Attributes

| Attribute    | Type | Required | Description                             |
|--------------|------|----------|-----------------------------------------|
| `ENDPOINT`   | str  | Yes      | API endpoint path for object operations |
| `api_client` | Scm  | Yes      | Instance of SCM API client              |

## Exceptions

| Exception                    | HTTP Code | Description                   |
|------------------------------|-----------|-------------------------------|
| `InvalidObjectError`         | 400       | Invalid object data or format |
| `MissingQueryParameterError` | 400       | Missing required parameters   |
| `NotFoundError`              | 404       | Object not found              |
| `AuthenticationError`        | 401       | Authentication failed         |
| `AuthorizationError`         | 403       | Permission denied             |
| `ConflictError`              | 409       | Object conflict               |
| `ServerError`                | 500       | Internal server error         |

## Basic Configuration

<div class="termy">

<!-- termynal -->

```python
from scm.client import Scm
from scm.config.objects import BaseObject

# Initialize client
client = Scm(
    client_id="your_client_id",
    client_secret="your_client_secret",
    tsg_id="your_tsg_id"
)


# Create custom object class
class CustomObject(BaseObject):
    ENDPOINT = "/config/objects/v1/custom"


# Initialize object
custom_obj = CustomObject(client)
```

</div>

## Usage Examples

### Creating Objects

<div class="termy">

<!-- termynal -->

```python
# Prepare object data
object_data = {
    "name": "test-object",
    "description": "Test object creation",
    "folder": "Texas"
}

# Create new object
try:
    new_object = custom_obj.create(object_data)
    print(f"Created object with ID: {new_object['id']}")
except InvalidObjectError as e:
    print(f"Invalid object data: {e.message}")
```

</div>

### Retrieving Objects

<div class="termy">

<!-- termynal -->

```python
# Get object by ID
try:
    object_id = "123e4567-e89b-12d3-a456-426655440000"
    retrieved_object = custom_obj.get(object_id)
    print(f"Retrieved object: {retrieved_object['name']}")
except NotFoundError as e:
    print(f"Object not found: {e.message}")
```

</div>

### Updating Objects

<div class="termy">

<!-- termynal -->

```python
# Update object data
update_data = {
    "id": "123e4567-e89b-12d3-a456-426655440000",
    "name": "updated-object",
    "description": "Updated description",
    "folder": "Texas"
}

# Perform update
try:
    updated_object = custom_obj.update(update_data)
    print(f"Updated object: {updated_object['name']}")
except InvalidObjectError as e:
    print(f"Invalid update data: {e.message}")
```

</div>

### Listing Objects

<div class="termy">

<!-- termynal -->

```python
# Define filter parameters
list_params = {
    "folder": "Texas",
    "limit": 100,
    "offset": 0
}

# List objects with filters
try:
    objects = custom_obj.list(**list_params)
    for obj in objects:
        print(f"Name: {obj['name']}")
except InvalidObjectError as e:
    print(f"Invalid filter parameters: {e.message}")
```

</div>

### Deleting Objects

<div class="termy">

<!-- termynal -->

```python
# Delete object by ID
try:
    object_id = "123e4567-e89b-12d3-a456-426655440000"
    custom_obj.delete(object_id)
    print("Object deleted successfully")
except NotFoundError as e:
    print(f"Object not found: {e.message}")
```

</div>

## Managing Configuration Changes

### Performing Commits

<div class="termy">

<!-- termynal -->

```python
# Prepare commit parameters
commit_params = {
    "folders": ["Texas"],
    "description": "Configuration update",
    "sync": True,
    "timeout": 300  # 5 minute timeout
}

# Commit changes
try:
    result = custom_obj.commit(**commit_params)
    print(f"Commit job ID: {result.job_id}")
except InvalidObjectError as e:
    print(f"Invalid commit parameters: {e.message}")
```

</div>

### Monitoring Jobs

<div class="termy">

<!-- termynal -->

```python
# Get status of specific job
try:
    job_status = custom_obj.get_job_status(result.job_id)
    print(f"Job status: {job_status.data[0].status_str}")

    # List recent jobs
    recent_jobs = custom_obj.list_jobs(limit=10)
    for job in recent_jobs.data:
        print(f"Job {job.id}: {job.type_str} - {job.status_str}")
except InvalidObjectError as e:
    print(f"Error checking job status: {e.message}")
```

</div>

## Error Handling

<div class="termy">

<!-- termynal -->

```python
from scm.exceptions import (
    InvalidObjectError,
    NotFoundError,
    AuthenticationError,
    ServerError
)

try:
    # Attempt operation
    result = custom_obj.create({
        "name": "test-object",
        "folder": "Texas"
    })

    # Commit changes
    commit_result = custom_obj.commit(
        folders=["Texas"],
        description="Added test object",
        sync=True
    )

    # Check job status
    status = custom_obj.get_job_status(commit_result.job_id)

except InvalidObjectError as e:
    print(f"Invalid object data: {e.message}")
except NotFoundError as e:
    print(f"Object not found: {e.message}")
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
except ServerError as e:
    print(f"Server error: {e.message}")
```

</div>

## Best Practices

1. **Object Initialization**
    - Define ENDPOINT in all subclasses
    - Validate api_client type
    - Use proper error handling
    - Initialize logging appropriately

2. **CRUD Operations**
    - Validate input data before operations
    - Handle response data consistently
    - Implement proper error handling
    - Use appropriate timeouts

3. **Job Management**
    - Monitor commit job status
    - Handle job failures appropriately
    - Use sync mode judiciously
    - Implement proper timeout handling

4. **Error Handling**
    - Catch specific exceptions first
    - Log error details
    - Provide meaningful error messages
    - Implement proper retry logic

5. **Performance**
    - Reuse object instances
    - Use appropriate pagination
    - Batch operations when possible
    - Cache frequently accessed data

## Full Script Examples

Refer to the [examples](https://github.com/cdot65/pan-scm-sdk/tree/main/examples) directory.

## Related Models

- [JobStatusResponse](../models/operations/jobs.md)
- [JobListResponse](../models/operations/jobs.md)
- [CandidatePushResponseModel](../models/operations/candidate_push.md)