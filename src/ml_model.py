
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Offer
import pandas as pd

def read_offers_to_df(db_path="voice2offer.db"):
    """Nuskaito Offer lentelės duomenis į DataFrame."""
    engine = create_engine(f"sqlite:///{db_path}")
    with Session(engine) as session:
        rows = session.query(Offer).all()
    data = []
    for r in rows:
        data.append({
            "id": r.id,
            "area": getattr(r, "area", None),
            "sum": getattr(r, "total_sum", None)
        })
    return pd.DataFrame(data)


if __name__ == "__main__":
    df = read_offers_to_df()
    print(df.head())