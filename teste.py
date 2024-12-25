from sqlalchemy import create_engine, inspect

# Configuração do banco
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)

# Inspecionar tabelas
inspector = inspect(engine)

# Listar tabelas do esquema 'test'
tables = inspector.get_table_names(schema="test")
print("Tabelas no esquema 'test':", tables)

# Detalhes de uma tabela específica
for table in tables:
    columns = inspector.get_columns(table_name=table, schema="test")
    print(f"\nTabela: {table}")
    for column in columns:
        print(f" - {column['name']} ({column['type']})")