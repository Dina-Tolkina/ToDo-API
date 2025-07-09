from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "User" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "login" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "Task" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL,
    "completed" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "User" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Permission" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "can_read" BOOL NOT NULL DEFAULT False,
    "can_write" BOOL NOT NULL DEFAULT True,
    "can_delete" BOOL NOT NULL DEFAULT False,
    "can_update" BOOL NOT NULL DEFAULT False,
    "task_id" INT NOT NULL REFERENCES "Task" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "User" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_Permission_user_id_8beb67" UNIQUE ("user_id", "task_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
