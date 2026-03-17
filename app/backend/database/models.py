from datetime import date

from sqlalchemy import BigInteger, String, ForeignKey, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend.database.core import Base


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Связываем жанр со всеми книгами
    books: Mapped[list["Book"]] = relationship(back_populates="genre")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    cost: Mapped[int] = mapped_column(BigInteger, nullable=False)
    count: Mapped[int] = mapped_column(BigInteger, server_default="0")

    # Связываем книгу с жанром и автором
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["Author"] = relationship(back_populates="books")
    genre: Mapped["Genre"] = relationship(back_populates="books")


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Связываем автора с его книгами
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[int] = mapped_column(Integer)

    # Связываем город с клиентами из него
    clients: Mapped[list["Client"]] = relationship(back_populates="city")


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Связываем клиента и его город
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    city: Mapped["City"] = relationship(back_populates="clients")

    # Связываем клиента с его заказами
    orders: Mapped[list["Order"]] = relationship(back_populates="client")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    wishes: Mapped[str | None] = mapped_column(String(500))

    # Связываем заказ с клиентом
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped["Client"] = relationship(back_populates="orders")

    # Связываем заказ с его деталями
    books_details: Mapped[list["OrderBook"]] = relationship(back_populates="order")
    steps_details: Mapped[list["OrderStep"]] = relationship(back_populates="order")


class OrderBook(Base):
    __tablename__ = "order_books"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped["Order"] = relationship(back_populates="books_details")
    book: Mapped["Book"] = relationship()


class Step(Base):
    __tablename__ = "steps"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    order_steps: Mapped[list["OrderStep"]] = relationship(back_populates="step")


class OrderStep(Base):
    __tablename__ = "order_steps"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    step_id: Mapped[int] = mapped_column(ForeignKey("steps.id"))

    date_step_beg: Mapped[date] = mapped_column(Date, nullable=False)
    date_step_end: Mapped[date | None] = mapped_column(Date)

    order: Mapped["Order"] = relationship(back_populates="steps_details")
    step: Mapped["Step"] = relationship(back_populates="order_steps")