# Django To-Do List Application

This is a simple to-do list application built with Django, following Test-Driven Development principles.

## Features

*   Create and manage personal to-do lists.
*   Add items to lists.
*   View lists.

## Installation

### Development Environment

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd django-tdd
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations:**
    ```bash
    python src/manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python src/manage.py runserver
    ```
    The application will be accessible at `http://localhost:8000/`.

### Production Environment

The production environment is set up using Docker and Ansible.

1.  **Build the Docker image:**
    ```bash
    docker build -t django-todo-app .
    ```

2.  **Deploy with Ansible:**
    *   Ensure you have Ansible installed and configured.
    *   Modify the `infra/deploy-playbook.yaml` and `infra/env.j2` files with your server details and environment variables.
    *   Run the Ansible playbook:
        ```bash
        ansible-playbook infra/deploy-playbook.yaml -i <inventory_file> -e env=<environment_name>
        ```
        Replace `<inventory_file>` with your Ansible inventory file and `<environment_name>` with your environment name (e.g., production, staging).

    **Note:**  Refer to the `infra/deploy-playbook.yaml` for detailed deployment steps and configuration.

## Running Tests

To run tests:

```bash
python src/manage.py test lists
python src/manage.py test functional_tests
```

## Contributing

[Add contribution guidelines here if applicable]

## License

[Add license information here if applicable]