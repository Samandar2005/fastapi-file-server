from tortoise import fields
from tortoise.models import Model


class File(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    saved_name = fields.CharField(max_length=255, index=True)
    path = fields.CharField(max_length=255)
    date = fields.DatetimeField(auto_now_add=True)
    hash_code = fields.CharField(max_length=255, index=True)
    server = fields.CharField(max_length=255, index=True)
    is_used_by_other_servers = fields.BooleanField(default=False)
    shareable = fields.BooleanField(default=True)
    public = fields.BooleanField(default=True)
    size = fields.IntField()
    format = fields.CharField(max_length=50)

    class Meta:
        table = "files"
        indexes = ["name", "saved_name", "hash_code", "server"]
