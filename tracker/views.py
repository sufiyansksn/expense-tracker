from django.shortcuts import render, redirect
from .models import TrackingHistory, CurrentBalance

def index(request):
    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
        expence_type = "CREDIT"
        if float(amount) < 0:
            expence_type = "DEBIT"

        tracking_history = TrackingHistory.objects.create(
            amount=amount,
            expence_type=expence_type,
            current_balance=current_balance,
            description=description
        )
        current_balance.current_balance += float(tracking_history.amount)
        current_balance.save()

        return redirect('/')

    # GET request — fetch everything from DB and pass to template
    current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
    transactions = TrackingHistory.objects.all().order_by('-created_at')

    income = sum(t.amount for t in transactions if t.expence_type == 'CREDIT')
    expense = sum(t.amount for t in transactions if t.expence_type == 'DEBIT')

    return render(request, 'index.html', {
        'current_balance': current_balance,
        'transactions': transactions,
        'income': income,
        'expense': abs(expense),
    })


def delete_transaction(request, id):
    transaction = TrackingHistory.objects.get(id=id)

    current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
    current_balance.current_balance -= transaction.amount
    current_balance.save()

    transaction.delete()
    return redirect('/')


