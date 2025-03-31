# CrypTomorrow

A cryptocurrency price tracking and analysis application.

## Prerequisites

- Docker Desktop installed on your system
- Git (for cloning the repository)

## Setup Instructions

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CrypTomorrow.git
   cd CrypTomorrow
   ```

2. Start the application:
   ```bash
   docker compose up --build
   ```

   This will:
   - Build the Docker image for the Python application
   - Start the PostgreSQL with TimescaleDB container
   - Initialize the database schema
   - Start the application container

3. To stop the application:
   ```bash
   docker compose down
   ```

   To stop and remove all data:
   ```bash
   docker compose down -v
   ```

## Project Structure

```
CrypTomorrow/
├── crypto_backend.py/
│   └── market_prices_collection/
│       ├── __init__.py
│       ├── store.py
│       └── db_conn.py
├── Dockerfile
├── docker-compose.yml
├── init_db.py
└── requirements.txt
```

## Features

- Real-time cryptocurrency price tracking
- Historical price data storage
- Data analysis and visualization
- RESTful API endpoints

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.