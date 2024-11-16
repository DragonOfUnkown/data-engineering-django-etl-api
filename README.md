# DjangoProjectNeo

Django-based project showcasing a client-transaction management system with advanced features like materialized views and data APIs.

---

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Setup Instructions](#setup-instructions)
4. [Usage](#usage)
5. [Testing](#testing)
6. [Expected Results](#expected-results)
7. [Troubleshooting](#troubleshooting)

---

## Features

- Manage Clients and their Transactions.
- Automatically calculate aggregated client transaction summaries using PostgreSQL Materialized Views.
- Admin dashboard to view and refresh materialized views.
- REST API to fetch client transaction data.
- ETL process for loading data from files into the database.

---

## Technologies Used

- **Python**:  3.11.9
- **Django**: 5.1.3
- **PostgreSQL**: 17.1
- **Docker**: For containerized setup

---

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/DragonOfUnkown/data-engineering-django-etl-api.git
cd djangoProjectNeo
```
### Step 2: Set Up Environment Variables
Modify the docker-compose.yml file to configure the PostgreSQL database environment. Locate the db service and update it with the following configuration:
```bash
db:
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: password
    POSTGRES_DB: neo_project_database
```

### Step 3: Start Docker Containers
Run the following commands:
```bash
docker-compose down -v  # Cleanup any old containers or volumes
docker-compose up --build
```
This will start the application and database containers.
## Usage
### Step 4: Make Migrations
Generate and apply database migrations:
```bash
docker-compose exec app python manage.py makemigrations
docker-compose exec app python manage.py migrate
```
### Step 5: Create a Superuser
Create a Django admin superuser:

```bash
docker-compose exec app python manage.py createsuperuser
```
Follow the prompts to set up the admin credentials.

### Step 6: Load Initial Data
Run the custom load_data command to populate the database:

```bash
docker-compose exec app python manage.py load_data
```
### Step 7: Access the Admin Panel
Navigate to the admin panel:

```bash
http://localhost:5000/admin/
```
Log in using the superuser credentials.

## Testing
### Step 8: Verify Materialized View
Access the MaterializedView model in the admin panel to refresh and monitor materialized views.
Alternatively, refresh manually in PostgreSQL:
```bash
docker-compose exec db psql -U postgres -d neo_project_database
```
Then, run:

```bash
REFRESH MATERIALIZED VIEW client_transaction_summary;
SELECT * FROM client_transaction_summary;
```
### Step 9: Use the REST API
You can test the API using Postman or curl:
```bash

GET http://localhost:5000/api/transactions/<client_id>/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```

see the pictures in the folder pictures to see screenshots of running api testing with postman and to view the admin pannel.
## Expected Results

### Admin Dashboard
- **Client**: Manage client data.
- **Transaction**: Manage transactions associated with clients.
- **MaterializedView**: Refresh and monitor materialized views.

---

### REST API
For a client with transactions, the API will return aggregated transaction data.

**Example Response**:
```json
{
  "client_id": 1,
  "total_transactions": 2,
  "total_spent": 500.00,
  "total_gained": 300.00
}
```
# Materialized View

The `client_transaction_summary` materialized view aggregates transaction data.

### Query

```sql
SELECT * FROM client_transaction_summary;
```
Expected Output

```table

 client_id | total_transactions | total_spent | total_gained
-----------+--------------------+-------------+--------------
         1 |                  2 |      500.00 |      300.00
         2 |                  1 |     1000.00 |         0.00
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running and accessible.
- Verify database credentials and connection settings in `docker-compose.yml`.

### Admin Panel Access
- Confirm the superuser creation was successful.
- If the application does not load, check container logs using:

```bash
docker logs <container_id>
```


