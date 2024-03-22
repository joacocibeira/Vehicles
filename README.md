# Vehicles 1.0.1

The Vehicles App is a web-based application designed to help users monitor and manage the movement of vehicles entering and exiting private facilities
## Installation

1. Clone the GitHub repository

```bash
   git clone https://github.com/joacocibeira/Vehicles
```
2. Rename the .env_sample file to .env and edit the variables

3. Run the following command to enter the Django shell:
   
    ```bash
    python manage.py shell
    ```

4. Once you're in the Django shell, execute the following Python commands to generate a new secret key:
   
    ```python
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    ```

5. Copy this key in your .env file to have a secure private key

3. Build and compose the image with Docker

```bash
   docker-compose up -d --build
```

## Features
- CRUD operations for vehicle management.
- Data validation for vehicle entries.
- Docker support for easy setup and deployment.


## Dependencies

- Docker