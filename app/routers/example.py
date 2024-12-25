from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.config.database import get_db
from app.models.example import ExampleTable
from datetime import datetime

router = APIRouter()

@router.get("/examples")
def get_examples(
    db: Session = Depends(get_db),
    id: int = None,
    start_date: str = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    end_date: str = Query(None, description="Data final no formato YYYY-MM-DD"),
    limit: int = Query(10, description="Número máximo de registros por página"),
    offset: int = Query(0, description="Deslocamento para paginação")
):
    """
    Retorna todos os registros ou aplica filtros com paginação:
    - **id**: Filtro opcional pelo ID.
    - **start_date**: Filtro opcional para registros criados após esta data (YYYY-MM-DD).
    - **end_date**: Filtro opcional para registros criados antes desta data (YYYY-MM-DD).
    - **limit**: Número máximo de registros por página.
    - **offset**: Deslocamento para paginação.
    """
    query = db.query(ExampleTable)

    # Filtro por ID
    if id is not None:
        query = query.filter(ExampleTable.id == id)

    # Filtro por intervalo de datas
    if start_date:
        try:
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(ExampleTable.created_at >= start_date_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido para start_date. Use YYYY-MM-DD.")
    if end_date:
        try:
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(ExampleTable.created_at <= end_date_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido para end_date. Use YYYY-MM-DD.")

    # Paginação
    total_records = query.count()  # Conta o total de registros antes da paginação
    results = query.offset(offset).limit(limit).all()

    if not results:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado para os filtros aplicados.")

    return {
        "total": total_records,
        "page": offset // limit + 1,
        "page_size": limit,
        "data": results,
    }