from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from data_app.models import Transaction
from datetime import datetime


class ClientTransactionsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, client_id):
        # Validate client_id
        if not isinstance(client_id, int):
            return Response({"error": "Invalid client_id. Must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Validate date format
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid start_date format. Expected YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid end_date format. Expected YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure start_date is not after end_date
        if start_date and end_date and start_date > end_date:
            return Response({"error": "start_date cannot be after end_date."}, status=status.HTTP_400_BAD_REQUEST)

        # Query transactions with validated inputs
        transactions = Transaction.objects.filter(client_id=client_id)
        if start_date and end_date:
            transactions = transactions.filter(transaction_date__range=[start_date, end_date])

        data = transactions.values('transaction_id', 'transaction_type', 'transaction_date', 'amount', 'currency')
        return Response(data)
