# Inventory Management Web Application

A full-stack inventory management system designed to streamline inventory tracking and management processes.

## Features

- **User Authentication**: Secure login system with role-based access control.
- **Inventory Tracking**: Add, update, and delete inventory items with real-time data synchronization.
- **Reporting**: Generate reports on inventory levels, sales, and other key metrics.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: React (JavaScript)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Deployment**: Docker

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/watson-clara/InventoryAppPublic.git
cd InventoryAppPublic
```

### 2. Set up the backend

- Navigate to the `backend` directory:

  ```bash
  cd backend
  ```

- Create a virtual environment and activate it:

  ```bash
  python3 -m venv env
  source env/bin/activate  # On Windows use `env\Scripts\activate`
  ```

- Install the required packages:

  ```bash
  pip install -r requirements.txt
  ```

- Set up the PostgreSQL database:

  ```bash
  psql -U your_username -d inventory_db -f schema.sql
  ```

  Ensure that `SQLALCHEMY_DATABASE_URI` in `config.py` is correctly set:

  ```python
  SQLALCHEMY_DATABASE_URI = 'postgresql://your_username:your_password@localhost:5432/inventory_db'
  ```

- Apply database migrations:

  ```bash
  flask db init
  flask db migrate
  flask db upgrade
  ```

- Run the backend server:

  ```bash
  flask run
  ```

### 3. Set up the frontend

- Navigate to the `frontend` directory:

  ```bash
  cd ../frontend
  ```

- Install the dependencies:

  ```bash
  npm install
  ```

- Start the frontend development server:

  ```bash
  npm start
  ```

## Usage

Once both the backend and frontend servers are running, you can access the application by navigating to `http://localhost:3000` in your web browser.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

