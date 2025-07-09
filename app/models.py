from tortoise import fields, models
from datetime import datetime


class User(models.Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)

    class Meta:
        table = "User"


class Permission(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='permissions')
    task = fields.ForeignKeyField('models.Task', related_name='permissions', on_delete=fields.CASCADE)
    can_read = fields.BooleanField(default=False)
    can_write = fields.BooleanField(default=True)
    can_delete = fields.BooleanField(default=False)
    can_update = fields.BooleanField(default=False)

    class Meta:
        table = "Permission"
        unique_together = (("user", "task"),)


class Task(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    description = fields.TextField()
    created_at = fields.DatetimeField(default=datetime.now)
    owner = fields.ForeignKeyField('models.User', related_name='owner_task')

    class Meta:
        table = "Task"