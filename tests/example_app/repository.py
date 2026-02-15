from collections.abc import Sequence
from typing import cast

from pydantic_core import to_jsonable_python
from real_ladybug import QueryResult

from wheke_ladybug import LadybugRepository

from .models import Post, User


class UserRepository(LadybugRepository):
    def create_table(self) -> None:
        with self.db.connection as conn:
            conn.execute(
                """
                CREATE NODE TABLE IF NOT EXISTS User
                (id SERIAL PRIMARY KEY, name STRING, meta JSON);
                """
            )

    async def create(self, user: User) -> None:
        with self.db.async_connection as conn:
            response = cast(
                QueryResult,
                await conn.execute(
                    """
                    CREATE (n:User {name: $name, meta: to_json($meta)})
                    RETURN n.id as id;
                    """,
                    parameters={
                        "name": user.name,
                        "meta": to_jsonable_python(user.meta),
                    },
                ),
            )

            response = cast(list[dict], response.rows_as_dict().get_all())
            user.id = response[0]["id"]

    async def list(self) -> Sequence[User]:
        with self.db.async_connection as conn:
            response = cast(
                QueryResult,
                await conn.execute(
                    """
                    MATCH (n:User)
                    RETURN n.id as id, n.name as name, n.meta as meta;
                    """
                ),
            )

            response = response.rows_as_dict().get_all()

            return [User(**row) for row in cast(list[dict], response)]


class PostRepository(LadybugRepository):
    def create_table(self) -> None:
        with self.db.connection as conn:
            conn.execute(
                """
                CREATE NODE TABLE IF NOT EXISTS Post
                (id SERIAL PRIMARY KEY, message STRING);
                CREATE REL TABLE IF NOT EXISTS Posted
                (FROM User TO Post, ONE_MANY);
                """
            )

    async def create(self, user_id: int, post: Post) -> None:
        with self.db.async_connection as conn:
            await conn.execute(
                """
                CREATE (n:Post {message: $message})
                WITH n
                MATCH (from:User {id: $user_id}), (to:Post {id: n.id})
                CREATE (from)-[r:Posted]->(to);
                """,
                parameters={
                    "message": post.message,
                    "user_id": user_id,
                },
            )

    async def list(self, user_id: int) -> Sequence[Post]:
        with self.db.async_connection as conn:
            response = cast(
                QueryResult,
                await conn.execute(
                    """
                    MATCH (u:User)-[r:Posted]->(p:Post)
                    WHERE u.id = $user_id
                    RETURN p.id as id, p.message as message;
                    """,
                    parameters={"user_id": user_id}
                ),
            )

            response = response.rows_as_dict().get_all()

            return [Post(**row) for row in cast(list[dict], response)]
