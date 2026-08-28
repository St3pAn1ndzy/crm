from django import forms

from customers.models import Customer
from leads.models import Lead
from services.models import Service


class ConvertLeadForm(forms.Form):
    lead = forms.ModelChoiceField(
        queryset=Lead.objects.exclude(status="converted"),
        required=True,
        label="Выберите потенциального клиента (лида)"
    )

    contract_title = forms.CharField(
        max_length=150, required=True, label="Название/Номер контракта"
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        required=True,
        label="Предоставляемая услуга",
    )
    document = forms.FileField(required=True, label="Файл с документом")
    start_date = forms.DateField(
        required=True,
        label="Дата заключения",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = forms.DateField(
        required=True,
        label="Период действия",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    cost = forms.DecimalField(
        max_digits=12, decimal_places=2, required=True, label="Сумма"
    )


class CustomerEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label="Имя")
    last_name = forms.CharField(max_length=50, label="Фамилия")
    phone = forms.CharField(max_length=20, label="Телефон")
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = Customer
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.lead:
            self.fields["first_name"].initial = self.instance.lead.first_name
            self.fields["last_name"].initial = self.instance.lead.last_name
            self.fields["phone"].initial = self.instance.lead.phone
            self.fields["email"].initial = self.instance.lead.email
