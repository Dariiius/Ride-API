# Ride-API

Ride-API is a RESTful API built using Django REST Framework (DRF) for managing ride-related data. This project serves as a demonstration of backend development skills for the Wingz Django Backend Developer Assessment.

### Technologies Used
- Django REST Framework (3.15.2)
- PostgreSQL (17.4.1)
- JWT Authentication (Simple JWT)

### Prerequisites
Ensure you have the following installed:
- Python 3.13.2
- PostgreSQL 17.4.1
- Virtual environment (refer to Setup #2 in the Setup Instructions below)

## Setup Instructions
#### 1. Clone the repository:
```sh
git clone https://github.com/Dariiius/Ride-API.git
```

#### 2. Verify required tools:
- Python
```sh
# Windows
python --version 

# macOS/Linux
python3 --version
```

- PostgreSQL
```sh
psql --version
```

#### 3. Create and activate the virtual environment:
- Windows (VS Code)
	1. Ctrl+Shift+P > Python: Create Environment > Venv > Choose installed python version
	2. Ctrl+Shift+P > Python: Select Interpreter > Choose the newly created virtual environment

- Windows
```sh
python -m venv .venv
.venv\Scripts\activate
```

- MacOS/Linux 
```sh
	- sudo apt-get install python3-venv # Applicable for Linux only
	- python3 -m venv .venv
	- source .venv/bin/activate
```

#### 3. Create database with PostgreSQL
```sh
psql -U your_username -d postgres
CREATE DATABASE ride_db;
```

If you're using Windows, click [here](https://medium.com/@zum.hatice/how-to-create-a-postgresql-db-and-connect-in-windows-b26eaa48c7fb) to view the installation instructions.  
Note: You can create the database using the pgAdmin tool, which is installed along with PostgreSQL.

#### 4. Install requirements:
```sh
pip install -r requirements.txt
```

#### 5. Create a .env file in the project's root directory (at the same level as manage.py) and paste the following content:
```sh
DB_NAME=ride_db
DB_USER=your_user # Update with your database user
DB_PASSWORD=your_password # Update with your database password
DB_HOST=localhost
DB_PORT=5432 # Update this if you are not using the default port
```

#### 5. Apply migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```

#### 6. Create Super User (Django Admin)
```sh
python manage.py createsuperuser
```

#### 7. Run the server
```sh
# Windows
python manage.py runserver 8080

# macOS/Linux
python3 manage.py runserver 8080
```

---

### Accessing Django Admin and Swagger-UI
- To access the **Django Admin panel**, open your browser and go to: http://127.0.0.1:8080/admin/.
- To view the **API documentation (Swagger-UI)**, navigate to: http://127.0.0.1:8080/api/schema/swagger-ui/.
- If you're using **Postman** for CRUD operations, download the collection and environment [here](https://drive.google.com/file/d/1l5K1UrN-8nFe62Y1IndV7PGR2MczuEed/view?usp=sharing).


### Additional Notes
#### Challenges faced during implementation:
1. Determining how to calculate the distance from the origin location to the pickup location. I ultimately chose the Haversine Formula, specifically the "Spherical Law of Cosines," which computes the straight-line distance between two points. I opted for this approach because the requirements did not explicitly specify that the distance must follow the road network, and it also improves performance by allowing calculations to be performed at the database level.
2. Writing a raw SQL query to count the number of trips that exceeded one hour per driver and sort the results by date.

#### Ride list API screenshots (Django Debug Bar)
*Note: Three queries were identified because there are only two ride records in the database, and the second and third queries are similar for each ride entry.*

[Screenshot #1](https://drive.google.com/file/d/1owhyS0lkGasUEGDR6ozbHRym2SALlror/view?usp=sharing) | [Screenshot #2](https://drive.google.com/file/d/1gZleE9gDJKIfbPAW9WCsb8Q2Tjzmxxn_/view?usp=sharing)


#### Raw SQL statement to retrieve the count of trips lasting more than one hour from pickup to drop-off:
```sql
WITH ride_durations AS (
    SELECT 
        re.ride_id,
        MAX(CASE WHEN re.description = 'Status changed to dropoff' THEN re.created_at END) AS dropoff_time,
        MAX(CASE WHEN re.description = 'Status changed to pickup' THEN re.created_at END) AS pickup_time
    FROM app_ride_event_rideevent re
    WHERE re.description IN ('Status changed to pickup', 'Status changed to dropoff')
    GROUP BY re.ride_id
)
SELECT 
    TO_CHAR(r.pickup_time, 'YYYY-MM') AS "Month",
    CONCAT(INITCAP(u.first_name), ' ', LEFT(INITCAP(u.last_name), 1)) AS "Driver",
    COUNT(*) AS "Count of Trips > 1 hr"
FROM ride_durations rd
INNER JOIN app_ride_ride r ON rd.ride_id = r.id
INNER JOIN app_user_user u ON r.driver_id = u.id
WHERE rd.dropoff_time IS NOT NULL 
AND rd.pickup_time IS NOT NULL
AND (rd.dropoff_time - rd.pickup_time) > INTERVAL '1 hour'
GROUP BY "Month", "Driver"
ORDER BY "Month";
```