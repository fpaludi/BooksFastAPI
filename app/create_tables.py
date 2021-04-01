import contextlib
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
# from src.db.models.orm import metadata, start_mappers
from src.db.models.book import Book
from src.db.base_class import Base


def create_tables(engine: Engine, session: Session):  # noqa
    print(f"\nCreating Tables in {engine.url}\n")
    Base.metadata.create_all(engine)
    session.commit()

    # If book table is empty add books
    if session.query(Book).first() is None:
        # Add books info
        books_df = pd.read_csv("src/data/books.csv")
        print("Saving books...")
        for _, row in books_df.iterrows():
            book = Book(
                isbn=row["isbn"],
                title=row["title"],
                author=row["author"],
                year=row["year"],
            )
            session.add(book)

        # Commit Changes
        print("Commiting changes...")
        session.commit()
    else:
        print("Table already has data")


def delete_tables(engine: Engine, session: Session):  # noqa
    print("\nRemoving Tables...\n")
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(f"TRUNCATE TABLE public.{table.name} RESTART IDENTITY CASCADE;")
        trans.commit()


if __name__ == "__main__":
    from settings import settings  # noqa
    from src.db.session import engine, SessionLocal

    session = SessionLocal()
    create_tables(engine, session)
    #delete_tables(engine, session)
    session.close()  # noqa
    engine.dispose()
