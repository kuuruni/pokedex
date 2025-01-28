CREATE TABLE IF NOT EXISTS types (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS pokemon (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  hp INT NOT NULL,
  attack INT NOT NULL,
  defense INT NOT NULL,
  sp_atk INT NOT NULL,
  sp_def INT NOT NULL,
  speed INT NOT NULL,
  picture VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS pokemon_types (
  id SERIAL PRIMARY KEY,
  pokemon_id INT NOT NULL,
  type_id INT NOT NULL,
  FOREIGN KEY (pokemon_id) REFERENCES pokemon(id),
  FOREIGN KEY (type_id) REFERENCES types(id)
);