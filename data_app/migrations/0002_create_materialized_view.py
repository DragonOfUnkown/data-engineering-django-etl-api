from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('data_app', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE MATERIALIZED VIEW client_transaction_summary AS
            SELECT
                client_id,
                COUNT(*) AS total_transactions,
                SUM(CASE WHEN transaction_type = 'buy' THEN amount ELSE 0 END) AS total_spent,
                SUM(CASE WHEN transaction_type = 'sell' THEN amount ELSE 0 END) AS total_gained
            FROM
                data_app_transaction
            GROUP BY
                client_id;
            """
        ),
    ]
