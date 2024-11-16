from django.db import migrations, models


def add_materialized_view(apps, schema_editor):
    """
    Adds an entry for the materialized view 'client_transaction_summary'
    into the MaterializedView model.
    """
    MaterializedView = apps.get_model('data_app', 'MaterializedView')
    MaterializedView.objects.create(name='client_transaction_summary')


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0002_create_materialized_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientTransactionSummary',
            fields=[
                ('client_id', models.IntegerField(primary_key=True, serialize=False)),
                ('total_transactions', models.IntegerField()),
                ('total_spent', models.DecimalField(decimal_places=2, max_digits=15)),
                ('total_gained', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
            options={
                'db_table': 'client_transaction_summary',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MaterializedView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('last_refreshed', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(add_materialized_view),
    ]
