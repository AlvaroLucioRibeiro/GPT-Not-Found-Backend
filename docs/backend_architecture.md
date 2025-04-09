# 📌 Backend Architecture - GPT-NOT-FOUND

## 📖 Overview
This document provides a detailed explanation of the **GPT-NOT-FOUND** backend architecture. It covers the directory structure, the purpose of each folder and file, and how the project is organized. The goal is to ensure clarity and maintainability for developers working on the project.

This backend is built using **FastAPI** and follows a modular structure to enhance scalability and maintainability. It includes robust testing, API routing, authentication, and database management.

---

## Index
- [Project Structure](#project-structure)
- [Folder & File Descriptions](#folder--file-descriptions)
  - [`.github`](#github)
  - [`docs`](#docs)
  - [`scripts`](#scripts)
  - [`src`](#src)
    - [`db`](#db)
    - [`modules`](#modules)
    - [`routes`](#routes)
    - [`tests`](#tests)
    - [`utils`](#utils)
- [Additional Configuration Files](#additional-configuration-files)


## Project Structure

The backend is structured as follows:

```mermaid
graph TD;
    subgraph GPT-NOT-FOUND
        C1[requirements.txt]
        C2[.gitignore]
        C3[vercel.json]

        subgraph .github
            subgraph workflows
                Test[Test.yml]
            end
        end

        subgraph scripts
            D1[create_and_activate_venv.sh]
            D2[send_email_notification.sh]
        end

        subgraph docs
            B1[backend_architecture.md]
            B2[backend_documentation.md]
        end

        subgraph src
            A1[main.py]
            A2[__init__.py]

            subgraph src/tests
                T3a[__init__.py]

                subgraph src/tests/db_tests
                    T1a[__init__.py]
                    T1b[db_base_test.py]

                    subgraph src/tests/db_tests/CRUD
                        T11[__init__.py]
                        T12[test_contracts.py]
                        T13[test_customers.py]
                        T14[test_events.py]
                        T15[test_invoices.py]
                        T16[test_orders.py]
                        T17[test_payments.py]
                        T18[test_products.py]
                    end
                end

                subgraph src/tests/routes
                    T51[__init__.py]
                    T52[test_route_customer_data.py]
                    T53[test_route_customers.py]
                    T54[test_route_events.py]
                    T55[test_route_invoices.py]
                    T56[test_route_order.py]
                    T57[test_route_login.py]
                    T58[test_route_payments.py]
                    T59[test_route_products.py]
                    T50[test_route_contracts.py]
                end

                subgraph src/tests/utils
                    T4[utils.py]
                end

                subgraph src/tests/utils_tests
                    T2a[utils_test.py]
                end
            end

            subgraph src/db
                DB1[db_base_classes.py]
                DB2[db_sql_connection.py]
                DB8[db_enums.py]

                subgraph src/db/CRUD
                    DB5[__init__.py]
                    DB3[create.py]
                    DB4[read.py]
                    DB6[delete.py]
                    DB7[update.py]
                end
            end

            subgraph src/modules
                M2[__init__.py]
                M1[modules_api.py]
            end

            subgraph src/routes
                R1[route_authentication.py]
                R2[route_customers_me.py]
                R3[route_customer_data.py]
                R4[route_events.py]
                R5[route_invoices.py]
                R6[route_order.py]
                R7[route_payments.py]
                R8[route_products.py]
                R9[route_contracts.py]
            end

            subgraph src/utils
                U3[__init__.py]
                U1[utils_token_auth.py]
                U2[utils_validation.py]
            end
        end
    end
```

## Folder & File Descriptions

### `.github`
This folder contains **GitHub Actions workflows** for CI/CD automation.

- **`workflows/Tests.yml`** → Defines automated test execution on GitHub Actions.

---

### `docs`
This folder stores documentation related to the backend.

- **`backend_architecture.md`** → Describes the project’s folder structure and purpose of each component.
- **`backend_documentation.md`** → Contains detailed API documentation and guidelines.

---

### `scripts`
This folder contains shell scripts used for automation.

- **`create_and_activate_venv.sh`** → Automates the creation and activation of a virtual environment for development.
- **`send_email_notification.sh`** → Send a email when the pipeline in guthub actions has been executed correctly

---

### `src`
The core of the backend application, where all logic is implemented.

#### `db`
Handles database connections and interactions.

- **`db_base_classes.py`** → Defines base classes for the database models.
- **`db_sql_connection.py`** → Manages the connection to the database.
- **`db_enums.py`** → All types of atributes in database
- **`CRUD/`** → Contains fundamental database operations:
  - **`create.py`** → Handles the creation of records.
  - **`delete.py`** → Handles delenting of records
  - **`read.py`** → Handles reading and fetching records.
  - **`update.py`** → Handles updating of records
  - **`__init__.py`** → Initializes the CRUD module.

---

#### `modules`
Contains modular functionalities that extend the backend.

- **`modules_api.py`** → Defines reusable API components and logic.
- **`__init__.py`** → Initializes the modules package.

---

#### `routes`
Defines all API endpoints for the application.

- **`route_authentication.py`** → Handles user authentication (login, JWT verification, etc.).
- **`route_customer_data.py`** → Handles getting data from customers in database
- **`route_customers_me.py`** → Handles customer-related API endpoints.
- **`route_events.py`** → Handles events-related API endpoints.
- **`route_invoices.py`** → Handles invoices-related API endpoints.
- **`route_order.py`** → Handles order-related API endpoints.
- **`route_payments.py`** → Handles payments-related API endpoints.
- **`route_products.py`** → Handles products-related API endpoints.
- **`route_contracts.py`** → Handles contracts-related API endpoints.

---

#### `tests`
Contains unit tests and integration tests to validate the system’s functionality.

- **`__init__.py`** → Initializes the test suite.
  
##### `db_tests`
Tests related to the database.

- **`__init__.py`** → Initializes the database test suite.
- **`db_base_test.py`** → Tests database operations.

###### `CRUD`

Tests related to CRUD operations in database

- **`test_contracts.py`** → Tests for CRUD operations in contracts table
- **`test_customers.py`** → Tests for CRUD operations in customers table
- **`test_events.py`** → Tests for CRUD operations in events table
- **`test_invoices.py`** → Tests for CRUD operations in invoices table
- **`test_orders.py`** → Tests for CRUD operations in orders table
- **`test_payments.py`** → Tests for CRUD operations in payments table
- **`test_products.py`** → Tests for CRUD operations in products table

##### `route`

Tests for endpoints of routes created.

- **`test_route_customer_data.py`** → Handles tests for getting data from customers in database
- **`test_route_customers.py`** → Handles tests for customer-related API endpoints.
- **`test_route_events.py`** → Handles tests for events-related API endpoints.
- **`test_route_invoices.py`** → Handles tests for invoices-related API endpoints.
- **`test_route_order.py`** → Handles tests for order-related API endpoints.
- **`test_route_login.py`** → Handles tests for authentication-related API endpoints.
- **`test_route_payments.py`** → Handles tests for payments-related API endpoints.
- **`test_route_products.py`** → Handles tests for products-related API endpoints.
- **`test_route_contracts.py`** → Handles tests for contracts-related API endpoints.

##### `utils`

Utils for creating tests.

- **`utlis.py`** → Helper functions for tests

##### `utils_tests`
Tests for utility functions.

- **`utils_test.py`** → Validates helper functions used throughout the project.

---

#### `utils`
Contains helper functions and utilities for authentication and validation.

- **`utils_token_auth.py`** → Handles JWT authentication and token management.
- **`utils_validation.py`** → Contains input validation functions.
- **`__init__.py`** → Initializes the utilities package.

---

## Additional Configuration Files

These files are located in the root directory of the project.

- **`requirements.txt`** → Lists all dependencies required for the project.
- **`.gitignore`** → Specifies files and folders to be ignored by Git.
- **`vercel.json`** → Configuration file for deploying the backend on Vercel.

---