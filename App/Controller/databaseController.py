import cx_Oracle
import json
import os
from dotenv import load_dotenv
import time
from pathlib import Path

load_dotenv('.env')

class DatabaseController:
    def __init__(self):
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.service_name = os.getenv('DB_SERVICE_NAME')
        self.connection = None
        self.rules_data_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'rules.JSON')
        self.database_management_path = os.path.join(os.path.dirname(__file__), '..', 'Files', 'databaseManagement.JSON')
        self.schema_table_data = self._load_database_management_data() 
        self.rules_by_table = self._load_rules_from_file()
        self.last_used_time = None
        self.session_timeout_seconds = 60
        self.local_username = None
        self.local_password = None
        self.local_host = None
        self.local_port = None
        self.local_service_name = None

    def set_credentials(self, username, password, host, port, service_name):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.service_name = service_name

    def connect(self):
        if not self.connection:
            try:
                if not all([self.username, self.password, self.host, self.port, self.service_name]):
                    raise Exception("Faltan parámetros de conexión. Verifica que todos los valores estén presentes.")
                self.local_username = self.username
                self.local_password = self.password
                self.local_host = self.host
                self.local_port = self.port
                self.local_service_name = self.service_name
                
                dsn_tns = cx_Oracle.makedsn(self.host, self.port, service_name=self.service_name)
                self.connection = cx_Oracle.connect(self.username, self.password, dsn_tns)
                
                
                self.last_used_time = time.time()
            except cx_Oracle.DatabaseError as e:
                raise Exception(f"Error al conectar: {str(e)}")

    def get_connection(self):
        self._check_session_timeout()
        if not self.connection:
            self.connect()
        return self.connection

    def _load_database_management_data(self):
        if os.path.exists(self.database_management_path):
            with open(self.database_management_path, 'r') as file:
                return json.load(file)
        return {}

    def save_database_management_data(self):
        with open(self.database_management_path, 'w') as file:
            json.dump(self.schema_table_data, file, indent=4)

    def _check_session_timeout(self):
        if self.last_used_time and (time.time() - self.last_used_time > self.session_timeout_seconds):
            self.close_connection()

    def is_connected(self):
        return self.connection is not None

    def execute_query(self, query):
        if not self.connection:
            raise Exception("No se ha establecido una conexión con la base de datos.")
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            self.last_used_time = time.time()
            return data
        except cx_Oracle.DatabaseError as e:
            raise Exception(f"Error al ejecutar la consulta: {str(e)}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.last_used_time = None

    def get_databases(self):
        return list(self.schema_table_data.keys())

    def get_tables(self, database_name):
        return self.schema_table_data.get(database_name, {}).keys()

    def get_all_tables(self):
        all_tables = []
        for db_name, table_list in self.schema_table_data.items():
            all_tables.extend([table for table in table_list])
        return all_tables

    def get_table_data(self, database_name, table_name):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            # Asegúrate de obtener la lista de columnas como una cadena separada por comas
            columns_to_display = self.get_columns_to_display(table_name)
            query = f"SELECT {columns_to_display} FROM {database_name}.{table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [col[0] for col in cursor.description]

            cursor.close()

            return rows, column_names
        except cx_Oracle.DatabaseError as e:
            raise Exception(f"Error al cargar datos: {str(e)}")


    def get_columns_to_display(self, table_name):
        for schema, tables in self.schema_table_data.items():
            if table_name in tables:
                table_info = tables[table_name]
                
                # Si table_info es un diccionario, maneja "clave" y "campos" normalmente
                if isinstance(table_info, dict):
                    columns = [f'"{table_info["clave"]}"'] if "clave" in table_info and table_info["clave"] not in table_info["campos"] else []
                    columns += [f'"{col}"' for col in table_info.get("campos", [])]
                    return ", ".join(columns)
                
                # Si table_info es una lista, simplemente retorna los campos de la lista
                elif isinstance(table_info, list):
                    return ", ".join([f'"{col}"' for col in table_info])
                
                else:
                    raise TypeError(f"Formato inesperado para 'table_info' en la tabla '{table_name}'")
        
        return "*"



    def get_parameterOptionsWithDescription(self, table_name):
        return self.rules_by_table.get(table_name.lower(), [])

    def _load_rules_from_file(self):
        if os.path.exists(self.rules_data_path):
            with open(self.rules_data_path, 'r') as file:
                data = json.load(file)
                return data.get('table_rules', {})
        return {}

    def _save_rules_to_file(self):
        with open(self.rules_data_path, 'w') as file:
            json.dump({"table_rules": self.rules_by_table}, file, indent=4)

    def add_rule_to_table(self, table_name, rule):
        table_name = table_name.lower()
        if table_name in self.rules_by_table:
            if rule not in self.rules_by_table[table_name]:
                self.rules_by_table[table_name].append(rule)
        else:
            self.rules_by_table[table_name] = [rule]
        self._save_rules_to_file()

    def remove_rule_from_table(self, table_name, rule):
        table_name = table_name.lower()
        if table_name in self.rules_by_table and rule in self.rules_by_table[table_name]:
            self.rules_by_table[table_name].remove(rule)
            self._save_rules_to_file()

    def get_database_by_table(self, table_name):
        for db_name, tables in self.schema_table_data.items():
            if table_name in tables:
                return db_name

        raise ValueError(f"No se encontró una base de datos para la tabla '{table_name}'")

    def generate_sql_script(self, db_name, table_name, original_df, modified_df, save_path, column_name=None):
        print(f"Column name: {column_name} desde dbController")
        try:
            # Obtener el esquema al que pertenece la tabla usando get_schema_by_table
            schema_name = self.get_schema_by_table(table_name)
            
            # Obtener información de la tabla
            table_info = self.schema_table_data[schema_name].get(table_name)
            if not table_info:
                print(f"Error: La tabla '{table_name}' no existe en el esquema '{schema_name}'.")
                return None

            # Obtener la clave primaria de la tabla
            primary_key = table_info.get("clave")
            if not primary_key:
                print(f"Error: No se encontró clave primaria para la tabla '{table_name}' en el esquema '{schema_name}'.")
                return None

            # Generar el script SQL con el esquema
            script = f"USE {schema_name};\n"

            for index, row in modified_df.iterrows():
                # Verificar si hay un cambio en la columna especificada (column_name)
                if column_name is not None:
                    original_value = original_df.iloc[index][column_name]
                    modified_value = row[column_name]

                    # Solo generar el UPDATE si el valor original no es None, "None", null, o vacío, y hay un cambio
                    if original_value not in [None, "None", "null", "", "ND"]:
                        if original_value != modified_value:
                            set_clause = f"{column_name}='{modified_value}'"
                            where_clause = f"{primary_key}='{original_df.iloc[index][primary_key]}' AND {column_name}='{original_value}'"
                            script += f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};\n"

                else:
                    # Si no se especifica column_name, recorre todas las columnas para detectar cambios
                    changes = []
                    where_conditions = [f"{primary_key}='{original_df.iloc[index][primary_key]}'"]
                    for col in original_df.columns:
                        original_value = original_df.iloc[index][col]
                        modified_value = row[col]
                        
                        # Solo incluir en el SET y WHERE si el valor original no es None, "None", null, o vacío, y ha cambiado
                        if original_value not in [None, "None", "null", "", "ND"] and original_value != modified_value:
                            changes.append(f"{col}='{modified_value}'")
                            where_conditions.append(f"{col}='{original_value}'")

                    # Solo generar el script si hay cambios
                    if changes:
                        set_clause = ", ".join(changes)
                        where_clause = " AND ".join(where_conditions)
                        script += f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};\n"

            # Guardar el script en el archivo especificado
            sql_file_name = f"{table_name}_Depurado.sql"
            full_file_path = os.path.join(os.path.dirname(save_path), sql_file_name)
            print(f"Intentando guardar el archivo SQL en: {full_file_path}")
            file_path = self.save_sql_to_selected_path(full_file_path, script)
            print(f"Ruta del archivo SQL guardado: {file_path}")
            return file_path

        except Exception as e:
            print(f"Error en generate_sql_script: {str(e)}")
            return None


    def save_sql_to_selected_path(self, file_path, script_content):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(script_content)

            return file_path
        except Exception as e:
            raise Exception(f"Error al guardar el archivo SQL: {str(e)}")

    
    def set_local_credentials(self, username, password, host, port, service_name):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.service_name = service_name
        
    
    def get_all_columns_for_table(self, schema_name, table_name, credentials=None):
        
        try:
            connection = self.get_connection()  # 
            cursor = connection.cursor()

            query = """
                SELECT COLUMN_NAME 
                FROM ALL_TAB_COLUMNS 
                WHERE TABLE_NAME = :table_name 
                AND OWNER = :schema_name
            """
            
            cursor.execute(query, table_name=table_name.upper(), schema_name=schema_name.upper())
            columns = [row[0] for row in cursor.fetchall()]

            cursor.close()

            return columns
        except cx_Oracle.DatabaseError as e:
            raise Exception(f"Error al obtener columnas: {str(e)}")
        
    def get_schema_by_table(self, table_name):
        """
        Obtiene el nombre del esquema basado en el nombre de la tabla.
        """
        for schema_name, tables in self.schema_table_data.items():
            if table_name in tables:
                return schema_name
        raise ValueError(f"No se encontró un esquema para la tabla '{table_name}'")

    def update_table_key(self, schema_name, table_name, new_key):
        """Actualiza la clave de la tabla en el archivo databaseManagement.JSON."""
        if schema_name in self.schema_table_data and table_name in self.schema_table_data[schema_name]:
            # Actualiza la clave de la tabla en el diccionario
            self.schema_table_data[schema_name][table_name]["clave"] = new_key
            # Guarda los cambios en el archivo JSON
            self.save_database_management_data()