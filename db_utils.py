import mysql.connector
import os
from dotenv import load_dotenv
import streamlit as st

# Cargar variables de entorno solo una vez
load_dotenv()

def get_connection():
    """
    Establece una conexión con la base de datos utilizando las credenciales del archivo .env
    
    Returns:
        Connection: Objeto de conexión a la base de datos MySQL
        
    Raises:
        ValueError: Si faltan variables de entorno necesarias
        mysql.connector.Error: Si hay un error al conectar con la base de datos
    """
    # Verificar que todas las variables de entorno necesarias estén definidas
    required_env_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Faltan variables de entorno necesarias: {', '.join(missing_vars)}")
    
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    except mysql.connector.Error as err:
        raise Exception(f"Error al conectar a la base de datos: {err}")

def get_tables():
    """
    Recupera la lista de tablas disponibles en la base de datos.
    
    Returns:
        list: Lista de nombres de tablas en la base de datos
        
    Raises:
        Exception: Si hay un error al consultar las tablas
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        return tables
    except Exception as e:
        raise Exception(f"Error al obtener las tablas: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def get_table_structure(table_name):
    """
    Retrieves the structure of a specified table from the database.

    Args:
        table_name (str): The name of the table whose structure is to be retrieved.

    Returns:
        list[dict]: A list of dictionaries where each dictionary represents a column in the table.
                    Each dictionary contains the following keys:
                    - COLUMN_NAME: The name of the column.
                    - COLUMN_TYPE: The data type of the column.
                    - IS_NULLABLE: Indicates whether the column can contain NULL values.
                    - COLUMN_KEY: Indicates whether the column is a key (e.g., primary key).
                    - COLUMN_DEFAULT: The default value of the column.
                    - EXTRA: Any additional information about the column (e.g., auto_increment).
                    - COLUMN_COMMENT: Comments associated with the column.
                    
    Raises:
        ValueError: Si el nombre de la tabla está vacío
        Exception: Si hay un error al consultar la estructura de la tabla
    """
    if not table_name:
        raise ValueError("El nombre de la tabla no puede estar vacío")
    
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                COLUMN_NAME,
                COLUMN_TYPE,
                IS_NULLABLE,
                COLUMN_KEY,
                COLUMN_DEFAULT,
                EXTRA,
                COLUMN_COMMENT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            ORDER BY ORDINAL_POSITION
        """
        cursor.execute(query, (os.getenv("DB_NAME"), table_name))
        structure = cursor.fetchall()
        return structure
    except Exception as e:
        raise Exception(f"Error al obtener la estructura de la tabla '{table_name}': {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_table_full_info(table_name):
    """
    Obtiene información completa de una tabla incluyendo estructura, claves foráneas, 
    motor de almacenamiento y otros metadatos.
    
    Args:
        table_name (str): Nombre de la tabla a consultar
        
    Returns:
        dict: Diccionario con toda la información de la tabla
    """
    if not table_name:
        raise ValueError("El nombre de la tabla no puede estar vacío")
    
    conn = None
    result = {
        'columns': [],
        'primary_keys': [],
        'foreign_keys': [],
        'indexes': [],
        'metadata': {}
    }
    
    try:
        conn = get_connection()
        
        # Obtener estructura de columnas
        result['columns'] = get_table_structure(table_name)
        
        # Obtener metadatos de la tabla
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                TABLE_NAME,
                ENGINE,
                VERSION,
                ROW_FORMAT,
                TABLE_ROWS,
                AVG_ROW_LENGTH,
                DATA_LENGTH,
                MAX_DATA_LENGTH,
                INDEX_LENGTH,
                AUTO_INCREMENT,
                CREATE_TIME,
                UPDATE_TIME,
                TABLE_COLLATION,
                TABLE_COMMENT
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        """
        cursor.execute(query, (os.getenv("DB_NAME"), table_name))
        metadata = cursor.fetchone()
        result['metadata'] = metadata if metadata else {}
        
        # Obtener información de claves primarias
        query = """
            SELECT 
                COLUMN_NAME 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND CONSTRAINT_NAME = 'PRIMARY'
            ORDER BY ORDINAL_POSITION
        """
        cursor.execute(query, (os.getenv("DB_NAME"), table_name))
        result['primary_keys'] = [row['COLUMN_NAME'] for row in cursor.fetchall()]
        
        # Obtener información de claves foráneas
        query = """
            SELECT 
                k.CONSTRAINT_NAME,
                k.COLUMN_NAME,
                k.REFERENCED_TABLE_NAME,
                k.REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE k
            JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS c ON 
                k.CONSTRAINT_NAME = c.CONSTRAINT_NAME AND 
                k.TABLE_SCHEMA = c.TABLE_SCHEMA AND 
                k.TABLE_NAME = c.TABLE_NAME
            WHERE 
                k.TABLE_SCHEMA = %s AND 
                k.TABLE_NAME = %s AND 
                c.CONSTRAINT_TYPE = 'FOREIGN KEY'
        """
        cursor.execute(query, (os.getenv("DB_NAME"), table_name))
        result['foreign_keys'] = cursor.fetchall()
        
        # Obtener índices
        query = """
            SELECT 
                INDEX_NAME,
                NON_UNIQUE,
                GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) AS columns_list
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            GROUP BY INDEX_NAME, NON_UNIQUE
        """
        cursor.execute(query, (os.getenv("DB_NAME"), table_name))
        result['indexes'] = cursor.fetchall()
        
        # Obtener el script CREATE TABLE
        cursor = conn.cursor()
        cursor.execute(f"SHOW CREATE TABLE {table_name}")
        create_table = cursor.fetchone()
        if create_table and len(create_table) > 1:
            result['create_script'] = create_table[1]
        
        return result
        
    except Exception as e:
        raise Exception(f"Error al obtener información completa de la tabla '{table_name}': {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
