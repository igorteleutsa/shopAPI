
# E-commerce REST API

## Project Overview

This project is a Django-based REST API for an e-commerce platform. It supports the following features:

- **Products**: List, filter, add, update, delete products.
- **Categories**: List, add, update, delete categories.
- **Reservations**: Create, update, cancel reservations.
- **Sales**: Start and end sales for products.
- **Reports**: Generate a report of sold products.

## Technologies Used

- **Django**: Web framework used for development.
- **Django REST Framework**: Framework used for building the REST API.
- **PostgreSQL**: Database used in the project.
- **Docker**: Used for containerization.

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    ```

2. **Navigate to the project directory**:
    ```bash
    cd <project-directory>
    ```

3. **Copy the `.env.sample` file to `.env`** and fill in your database credentials and secret key:
    ```bash
    cp .env.sample .env
    ```

4. **Run the project using Docker Compose**:
    ```bash
    docker-compose up --build
    ```

5. **Apply migrations**:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

6. **Create a superuser** to access the Django admin:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

7. **Access the application**:
    - The API will be available at: `http://localhost:8000/api/`
    - Django Admin: `http://localhost:8000/admin/`
    - Swagger Documentation: `http://localhost:8000/swagger/`

## Running Tests

To run the tests for this project, use the following command:

```bash
docker-compose exec web python manage.py test
```

## RBAC (Role-Based Access Control)

This project uses RBAC through Django's permission system, allowing for scalable and changeable access control based on roles.

## API Documentation

The API is documented using Swagger. You can access the interactive API documentation at:

```
http://localhost:8000/swagger/
```

## Notes

- Ensure the database service is running before executing the migrations or running the development server.
- The project follows PEP8 guidelines and uses `black` for code formatting.
