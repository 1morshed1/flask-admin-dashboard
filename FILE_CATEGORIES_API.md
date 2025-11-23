# File Categories API Documentation

This document describes the REST API endpoints for managing file categories in the Flask Admin Dashboard.

## Base URL

All endpoints are prefixed with `/api/file-categories`

## Authentication

All endpoints require JWT authentication. Include the JWT token in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

## Authorization

- **GET** endpoints: Require authentication (any authenticated user)
- **POST, PUT, DELETE** endpoints: Require admin or superadmin role

---

## Endpoints

### 1. List File Categories

Get a paginated list of file categories with optional filtering, searching, and sorting.

**Endpoint:** `GET /api/file-categories`

**Authentication:** Required (JWT)

**Authorization:** Any authenticated user

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number (minimum: 1) |
| `per_page` | integer | No | 20 | Items per page (minimum: 1, maximum: 100) |
| `search` | string | No | - | Search term (searches in code, name, and description) |
| `status` | string | No | - | Filter by status: `active` or `inactive` |
| `sort` | string | No | `code` | Field to sort by (e.g., `code`, `name`, `created_date`, `last_updated`) |
| `order` | string | No | `asc` | Sort order: `asc` or `desc` |

**Example Request:**

```bash
GET /api/file-categories?page=1&per_page=20&status=active&sort=code&order=asc
```

**Example Response (200 OK):**

```json
{
  "file_categories": [
    {
      "id": "abc123",
      "code": "1099",
      "name": "1099",
      "description": "File category for 1099",
      "status": "active",
      "created_date": "2024-01-15T10:30:00",
      "last_updated": "2024-01-15T10:30:00",
      "user_count": 5
    },
    {
      "id": "def456",
      "code": "CHECKS",
      "name": "Checks",
      "description": "File category for Checks",
      "status": "active",
      "created_date": "2024-01-15T10:31:00",
      "last_updated": "2024-01-15T10:31:00",
      "user_count": 3
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 10,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

**Error Responses:**

- `401 Unauthorized`: Missing or invalid JWT token
- `400 Bad Request`: Invalid query parameters

---

### 2. Get File Category by ID

Get a specific file category by its ID.

**Endpoint:** `GET /api/file-categories/<category_id>`

**Authentication:** Required (JWT)

**Authorization:** Any authenticated user

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category_id` | string | Yes | The unique identifier of the file category |

**Example Request:**

```bash
GET /api/file-categories/abc123
```

**Example Response (200 OK):**

```json
{
  "id": "abc123",
  "code": "1099",
  "name": "1099",
  "description": "File category for 1099",
  "status": "active",
  "created_date": "2024-01-15T10:30:00",
  "last_updated": "2024-01-15T10:30:00",
  "user_count": 5
}
```

**Error Responses:**

- `401 Unauthorized`: Missing or invalid JWT token
- `404 Not Found`: File category not found

```json
{
  "error": {
    "code": "CATEGORY_NOT_FOUND",
    "message": "File category with id abc123 not found"
  }
}
```

---

### 3. Create File Category

Create a new file category.

**Endpoint:** `POST /api/file-categories`

**Authentication:** Required (JWT)

**Authorization:** Admin or Superadmin only

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | Yes | Unique code for the category (1-50 characters). Will be converted to uppercase automatically. |
| `name` | string | No | Display name for the category (max 100 characters). If not provided, defaults to the code. |
| `description` | string | No | Description of the category |
| `status` | string | No | Status: `active` or `inactive` (default: `active`) |

**Example Request:**

```json
{
  "code": "NEW_CATEGORY",
  "name": "New Category",
  "description": "Description for the new category",
  "status": "active"
}
```

**Example Response (201 Created):**

```json
{
  "message": "File category created successfully",
  "file_category": {
    "id": "xyz789",
    "code": "NEW_CATEGORY",
    "name": "New Category",
    "description": "Description for the new category",
    "status": "active",
    "created_date": "2024-01-15T11:00:00",
    "last_updated": "2024-01-15T11:00:00",
    "user_count": 0
  }
}
```

**Error Responses:**

- `400 Bad Request`: Invalid request body or validation error

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": ["code"],
        "message": "String should have at least 1 character",
        "type": "string_too_short"
      }
    ]
  }
}
```

- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Insufficient permissions (not admin/superadmin)

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Admin access required"
  }
}
```

- `409 Conflict`: Category code already exists

```json
{
  "error": {
    "code": "CATEGORY_EXISTS",
    "message": "A file category with this code already exists"
  }
}
```

---

### 4. Update File Category

Update an existing file category. All fields are optional, but at least one field must be provided.

**Endpoint:** `PUT /api/file-categories/<category_id>`

**Authentication:** Required (JWT)

**Authorization:** Admin or Superadmin only

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category_id` | string | Yes | The unique identifier of the file category |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `code` | string | No | Unique code for the category (1-50 characters). Will be converted to uppercase automatically. |
| `name` | string | No | Display name for the category (max 100 characters) |
| `description` | string | No | Description of the category |
| `status` | string | No | Status: `active` or `inactive` |

**Note:** At least one field must be provided in the request body.

**Example Request:**

```json
{
  "name": "Updated Category Name",
  "description": "Updated description",
  "status": "inactive"
}
```

**Example Response (200 OK):**

```json
{
  "message": "File category updated successfully",
  "file_category": {
    "id": "abc123",
    "code": "1099",
    "name": "Updated Category Name",
    "description": "Updated description",
    "status": "inactive",
    "created_date": "2024-01-15T10:30:00",
    "last_updated": "2024-01-15T12:00:00",
    "user_count": 5
  }
}
```

**Error Responses:**

- `400 Bad Request`: Invalid request body, validation error, or no fields provided

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "At least one field must be provided for update"
  }
}
```

- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Insufficient permissions (not admin/superadmin)
- `404 Not Found`: File category not found
- `409 Conflict`: Category code already exists (when updating code)

```json
{
  "error": {
    "code": "CATEGORY_EXISTS",
    "message": "A file category with this code already exists"
  }
}
```

---

### 5. Delete File Category

Delete a file category. The category cannot be deleted if it is assigned to any users.

**Endpoint:** `DELETE /api/file-categories/<category_id>`

**Authentication:** Required (JWT)

**Authorization:** Admin or Superadmin only

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category_id` | string | Yes | The unique identifier of the file category |

**Example Request:**

```bash
DELETE /api/file-categories/abc123
```

**Example Response (200 OK):**

```json
{
  "message": "File category deleted successfully"
}
```

**Error Responses:**

- `400 Bad Request`: Category is assigned to users

```json
{
  "error": {
    "code": "CATEGORY_IN_USE",
    "message": "Cannot delete file category. It is assigned to 5 user(s). Please unassign it from all users first."
  }
}
```

- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Insufficient permissions (not admin/superadmin)
- `404 Not Found`: File category not found

```json
{
  "error": {
    "code": "CATEGORY_NOT_FOUND",
    "message": "File category with id abc123 not found"
  }
}
```

---

## Data Models

### File Category Object

```json
{
  "id": "string",                    // Unique identifier (Firestore document ID)
  "code": "string",                  // Unique category code (uppercase)
  "name": "string",                  // Display name (optional)
  "description": "string",           // Description (optional)
  "status": "active" | "inactive",  // Status
  "created_date": "ISO8601",         // Creation timestamp
  "last_updated": "ISO8601",         // Last update timestamp
  "user_count": 0                    // Number of users assigned to this category
}
```

### Pagination Object

```json
{
  "page": 1,           // Current page number
  "per_page": 20,      // Items per page
  "total": 100,        // Total number of items
  "pages": 5,          // Total number of pages
  "has_next": true,    // Whether there is a next page
  "has_prev": false    // Whether there is a previous page
}
```

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": []  // Optional: Array of validation error details
  }
}
```

### Common Error Codes

- `VALIDATION_ERROR`: Request validation failed
- `FORBIDDEN`: Insufficient permissions
- `CATEGORY_NOT_FOUND`: File category not found
- `CATEGORY_EXISTS`: Category code already exists
- `CATEGORY_IN_USE`: Category cannot be deleted because it's assigned to users

---

## Usage Examples

### Example 1: Create a File Category

```bash
curl -X POST https://api.example.com/api/file-categories \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "TRAVEL_REPORTS",
    "name": "Travel Reports",
    "description": "Category for travel-related documents",
    "status": "active"
  }'
```

### Example 2: List Active Categories with Search

```bash
curl -X GET "https://api.example.com/api/file-categories?status=active&search=report&sort=name&order=asc" \
  -H "Authorization: Bearer <your_jwt_token>"
```

### Example 3: Update Category Status

```bash
curl -X PUT https://api.example.com/api/file-categories/abc123 \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "inactive"
  }'
```

### Example 4: Delete a Category

```bash
curl -X DELETE https://api.example.com/api/file-categories/abc123 \
  -H "Authorization: Bearer <your_jwt_token>"
```

---

## Notes

1. **Code Uniqueness**: Category codes must be unique. Codes are automatically converted to uppercase.

2. **Deletion Protection**: Categories cannot be deleted if they are assigned to any users. You must first unassign the category from all users before deletion.

3. **Activity Logging**: All create, update, and delete operations are logged in the activity log system.

4. **User Count**: The `user_count` field shows how many users are currently assigned to the category. This is calculated dynamically.

5. **Pagination**: The default page size is 20 items. Maximum page size is 100 items.

6. **Search**: The search functionality searches across `code`, `name`, and `description` fields (case-insensitive).

7. **Sorting**: You can sort by any field in the category object. Common sort fields include `code`, `name`, `created_date`, `last_updated`, and `user_count`.

---

## Integration with User Management

File categories can be assigned to users when creating or updating users. See the [Users API Documentation](README.md#users-api) for details on how to assign categories using the `file_category_ids` field.

Example user creation with file categories:

```json
{
  "email": "user@example.com",
  "password": "password123",
  "file_category_ids": ["category_id_1", "category_id_2"]
}
```

