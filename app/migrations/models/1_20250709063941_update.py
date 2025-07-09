from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "Task" DROP COLUMN "completed";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "Task" ADD "completed" BOOL NOT NULL DEFAULT False;"""
