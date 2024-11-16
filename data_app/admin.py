from django.contrib import admin
from .models import Client, Transaction, ClientTransactionSummary, MaterializedView
from django.core.management import call_command


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'name', 'email', 'country', 'account_balance')
    search_fields = ('name', 'email')
    list_filter = ('country',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'client', 'transaction_type', 'transaction_date', 'amount', 'currency')
    search_fields = ('transaction_id', 'client__name', 'transaction_type')
    list_filter = ('transaction_type', 'currency', 'transaction_date')


@admin.register(MaterializedView)
class MaterializedViewAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_refreshed')
    actions = ['refresh_materialized_view', 'trigger_etl']

    @admin.action(description='Refresh selected materialized views')
    def refresh_materialized_view(self, request, queryset):
        for view in queryset:
            view.refresh_view()
        self.message_user(request, "Selected materialized views refreshed successfully.")

    @admin.action(description='Trigger ETL Process')
    def trigger_etl(self, request, queryset):
        call_command('load_data')  # Runs the custom load_data command
        self.message_user(request, "ETL process triggered successfully.")


@admin.register(ClientTransactionSummary)
class ClientTransactionSummaryAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'total_transactions', 'total_spent', 'total_gained')
    search_fields = ('client_id',)
