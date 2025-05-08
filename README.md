## Description

This is a simple API for managing insurance policies. It provides endpoints to **list**, **create**, **delete**, and **update** policy records.

---

## Running the Application

1. **Start the application:**
   ```sh
   docker compose up
   ```

2. **Apply the database migrations:**
   ```sh
   docker-compose run web python manage.py migrate
   ```

3. **Run the tests:**
   ```sh
   docker-compose exec web bash
   python manage.py test api
   ```

---

## API Endpoints

You can interact with the API using the following endpoints:

### Create a Policy

**Request:**
```
POST http://localhost:8000/api/policies/
```

**Body:**
```json
{
  "customer_name": "John Doe",
  "policy_type": "life",
  "expiry_date": "2025-12-31"
}
```

---

### List All Policies

**Request:**
```
GET http://localhost:8000/api/policies/
```

---

### Delete a Policy

**Request:**
```
DELETE http://localhost:8000/api/policies/<POLICY_ID>/
```

---

### Update a Policy

**Request:**
```
PUT http://localhost:8000/api/policies/<POLICY_ID>/
```

**Body:**
```json
{
  "customer_name": "John Doe",
  "policy_type": "car",
  "expiry_date": "2026-12-31"
}
```

---

> **Note:** The `expiry_date` is validated to ensure it is not in the past.