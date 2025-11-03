from sqlalchemy import event
from sqlalchemy.orm import Session

@event.listens_for(Session, "after_commit")
def export_tables_after_commit(session):
    # Ici la base est à jour : les INSERT/UPDATE/DELETE sont déjà validés
    import pandas as pd
    import os
    from sqlalchemy import inspect

    engine = session.get_bind()
    inspector = inspect(engine)

    export_path = "/data"  # ou le dossier monté depuis ton conteneur DB
    os.makedirs(export_path, exist_ok=True)

    for table_name in inspector.get_table_names():
        df = pd.read_sql_table(table_name, engine)
        df.to_csv(os.path.join(export_path, f"{table_name}.csv"), index=False)
    
    print("✅ Base exportée après commit")
