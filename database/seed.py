import requests, psycopg
import os, re

db_host = os.getenv('POSTGRES_HOST') or "localhost"
db_port = os.getenv('POSTGRES_PORT') or 5432
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')

conn_info = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

def scrape_pokedex():
    url = 'https://pokemondb.net/pokedex/all'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    # find table element
    start_index = response.text.find('<table id="pokedex" class="data-table sticky-header block-wide">')
    end_index = response.text.find('</table>', start_index) + len('</table>')
    table_html = response.text[start_index:end_index]

    # data column
    start_index = table_html.find('<thead>')
    end_index = table_html.find('</thead>') + len('</thead>')
    columns = re.findall(r'<th.*?><div.*?>(.+?)</div></th>', table_html[start_index:end_index])
    columns = [re.sub(r'<.*?>', '', col).strip().lower().replace(". ", "_") for col in columns]
    
    # data rows
    start_index = table_html.find('<tbody>')
    end_index = table_html.find('</tbody>') + len('</tbody>')
    data_rows = []
    
    for row in table_html[start_index:end_index].split('</tr>'):
        row_data = {
            columns[i]: re.sub(r'<.*?>', '', col).strip()
            for i, col in enumerate(row.split('</td>')[:-1])
        }
        # skip empty rows
        if not row_data:
            continue
        row_data["type"] = row_data.pop("type").lower().split(" ")
        picture = re.search(r'<img.*?src="(.+?)"', row)
        row_data['picture'] = picture.group(1)
        data_rows.append(row_data)

    return data_rows

def seed():
    conn = psycopg.connect(conn_info)
    cursor = conn.cursor()
    
    pokedex = scrape_pokedex()
    poke_types = set().union(*[pokemon['type'] for pokemon in pokedex])
    poke_types = dict(zip(poke_types, range(1, len(poke_types) + 1)))
    
    cursor.execute("BEGIN TRANSACTION;")
    cursor.execute("DELETE FROM pokemon;")
    cursor.execute("DELETE FROM types;")
    cursor.execute("DELETE FROM pokemon_types;")

    for poke_type, id in poke_types.items():
        cursor.execute("""
            INSERT INTO types 
              (id, name)
            VALUES 
              (%s, %s);
        """, (id, poke_type))

    for pokemon in pokedex:
        result = cursor.execute("""
            INSERT INTO pokemon 
              (name, hp, attack, defense, sp_atk, sp_def, speed, picture)
            VALUES 
              (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            pokemon['name'],
            pokemon['hp'],
            pokemon['attack'],
            pokemon['defense'],
            pokemon['sp_atk'],
            pokemon['sp_def'],
            pokemon['speed'],
            pokemon['picture']
        ))

        [poke_id] = result.fetchone()
        for poke_type in pokemon['type']:
            cursor.execute("""
                INSERT INTO pokemon_types 
                  (pokemon_id, type_id)
                VALUES 
                  (%s, %s);
            """, (poke_id, poke_types[poke_type]))
            
    cursor.execute("COMMIT;")
        
if __name__ == '__main__':
    seed()