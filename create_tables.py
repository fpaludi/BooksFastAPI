import contextlib
import pandas as pd
from sqlalchemy.exc import ArgumentError
from settings import update_settings
from src.db.models.orm import metadata, start_mappers
from src.db.models.books import Books


def create_tables(engine, session):  # noqa
    print(f"\nCreating Tables in {engine.url}\n")
    try:
        start_mappers()
    except ArgumentError:
        pass
    metadata.create_all(engine)

    # Add books info
    books_df = pd.read_csv("src/data/books.csv")
    print("Saving books...")
    for _, row in books_df.iterrows():
        book = Books(
            isbn=row["isbn"], title=row["title"], author=row["author"], year=row["year"]
        )
        session.add(book)

    # Commit Changes
    print("Commiting changes...")
    session.commit()


def delete_tables(engine, session):  # noqa
    print("\nRemoving Tables...\n")
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(metadata.sorted_tables):
            con.execute(table.delete())
        for table in reversed(metadata.sorted_tables):
            con.execute(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE")
        trans.commit()


if __name__ == "__main__":
    update_settings("default")
    from src.db.repositories import RepositoryContainer

    engine = RepositoryContainer.engine()
    session = RepositoryContainer.DEFAULT_SESSIONFACTORY()

    create_tables(engine, session)
