from sqlalchemy.orm import Session

from sql_app import models


def get_marker(db: Session, marker_id: int) -> models.Marker:
    query = db.query(models.Marker)
    query_filter = query.filter(models.Marker.id == marker_id)
    first = query_filter.first()
    return first
