# Pokédex API

An API serving all Pokémon types, scraped from [Pokémon Database](https://pokemondb.net/pokedex/all). Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [psycopg](https://www.psycopg.org/)

## Prerequisites

1. Copy `.env.example` to `.env` and fill in your environment variables.
2. Create and activate your virtual environment:
  ```sh
  python -m venv <your-env>
  source <your-env>/bin/activate  # On Windows use `<your-env>\Scripts\activate`
  ```
3. Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
4. Migrate the database tables:
  ```sh
  python database/migration.py
  ```
5. Seed the database:
  ```sh
  python database/seed.py
  ```
6. Start the FastAPI server:
  - For development:
    ```sh
    fastapi dev main.py
    ```
  - For production:
    ```sh
    fastapi run main.py
    ```