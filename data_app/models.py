from django.db import models


class Client(models.Model):
    client_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=50)
    account_balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Transaction(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=10)


class MaterializedView(models.Model):
    name = models.CharField(max_length=255, unique=True)
    last_refreshed = models.DateTimeField(auto_now=True)

    def refresh_view(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(f"REFRESH MATERIALIZED VIEW {self.name}")
        self.last_refreshed = models.DateTimeField(auto_now=True)
        self.save()

    def __str__(self):
        return self.name


class ClientTransactionSummary(models.Model):
    client_id = models.IntegerField(primary_key=True)
    total_transactions = models.IntegerField()
    total_spent = models.DecimalField(max_digits=15, decimal_places=2)
    total_gained = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False  # Django will not manage the table
        db_table = 'client_transaction_summary'
