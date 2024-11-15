import pandas as pd
from django.core.management.base import BaseCommand
from data_app.models import Client, Transaction


class Command(BaseCommand):
    help = "Load data from CSV and XLSX into PostgreSQL"

    def handle(self, *args, **kwargs):
        # Load clients
        clients_df = pd.read_csv('clients.csv', parse_dates=['date_of_birth'])
        for _, row in clients_df.iterrows():
            Client.objects.create(
                client_id=row['client_id'],
                name=row['name'],
                email=row['email'],
                date_of_birth=row['date_of_birth'],
                country=row['country'],
                account_balance=row['account_balance']
            )

        # Load transactions
        transactions_df = pd.read_excel('transactions.xlsx')
        for _, row in transactions_df.iterrows():
            Transaction.objects.create(
                transaction_id=row['transaction_id'],
                client_id=row['client_id'],
                transaction_type=row['transaction_type'],
                transaction_date=row['transaction_date'],
                amount=row['amount'],
                currency=row['currency']
            )

        self.stdout.write("Data loaded successfully")
