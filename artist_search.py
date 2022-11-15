import sqlalchemy
import pandas as pd

def artist_objects(connection_string, artist, results_per_page=10, page_number=0):
    offset = results_per_page * page_number # zero based page counting
    artist_wildcard = f'%{artist.lower()}%'
    
    query = f"""
    SELECT *
    FROM mia
    WHERE artist ILIKE %s
    ORDER BY index
    OFFSET %s LIMIT %s"""

    engine = sqlalchemy.create_engine(connection_string)
    conn = engine.connect()
    
    response = conn.execute(query, artist_wildcard, offset, results_per_page)
    
    columns = response.keys()
    objects = response.fetchall()
    
    return pd.DataFrame(objects, columns=columns)

def artist_count(connection_string, artist, results_per_page=10, page_number=0):
    offset = results_per_page * page_number # zero based page counting
    artist_wildcard = f'%{artist.lower()}%'
    
    query = f"""
    SELECT COUNT(*)
    FROM mia
    WHERE artist ILIKE %s
    """
    
    engine = sqlalchemy.create_engine(connection_string)
    conn = engine.connect()
    
    response = conn.execute(query, artist_wildcard)
    
    total = response.fetchone()[0]
    
    high = min(offset + results_per_page - 1, total)
    
    return {"low": offset, "high": high, "total": total}

