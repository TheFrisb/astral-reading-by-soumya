import uuid

from django.core.exceptions import ValidationError
from django.db import transaction

from core.forms.checkout_form import CheckoutForm
from core.models import ReadingType, Order, OrderInformation, OrderItem
from core.services.checkout.stripe_service import InternalStripeService


class InternalCheckoutService:
    def __init__(self):
        self.payment_service = InternalStripeService()

    def get_checkout_url(self, form: CheckoutForm) -> str:
        reading_type = self.get_reading_type(form.cleaned_data.get("reading_type"))

        order = self.create_order(form.cleaned_data, reading_type)

        return self.payment_service.create_checkout_session(order)

    def get_reading_type(self, reading_type: uuid.UUID) -> ReadingType:
        try:
            return ReadingType.objects.get(pk=reading_type, reading__is_active=True)
        except ReadingType.DoesNotExist:
            raise ValidationError("Invalid consultation type selected.")

    @transaction.atomic
    def create_order(self, form: dict, reading_type: ReadingType):
        order = Order.objects.create()

        order_information = OrderInformation.objects.create(
            order=order,
            full_name=form["full_name"],
            email=form["email"],
            phone_number=form["phone_number"],
            date_of_birth=form["date_of_birth"],
            place_of_birth=form["place_of_birth"],
            time_of_birth=form["time_of_birth"],
            gender=form["gender"],
            birth_city=["birth_city"],
            birth_country=form["birth_country"],
            birth_state=form["birth_state"],
            comment=form["comment"],
        )

        order_item = OrderItem.objects.create(
            order=order,
            reading_type=reading_type,
            quantity=1,
            price=reading_type.sale_price,
        )

        return (
            Order.objects.select_related("information", "item")
            .prefetch_related("item__reading_type", "item__reading_type__reading")
            .get(pk=order.id)
        )
