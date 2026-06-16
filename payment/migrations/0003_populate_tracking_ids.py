import uuid
from django.db import migrations

def gen_unique_uuids(apps, schema_editor):
    Transaction = apps.get_model('payment', 'Transaction')
    # Loop over every single transaction currently inside your database
    for row in Transaction.objects.all():
        if not row.tracking_id:
            row.tracking_id = uuid.uuid4().hex
            row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_transaction_tracking_id_and_more'), # This must match the name of the file right before this one
    ]

    operations = [
        migrations.RunPython(gen_unique_uuids, reverse_code=migrations.RunPython.noop),
    ]