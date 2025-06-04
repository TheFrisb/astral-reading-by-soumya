import logging
from enum import Enum

import stripe
from django.conf import settings
from django.urls import reverse

from core.models import Order, OrderItem
from core.services.mail.mail_service import MailService

log = logging.getLogger(__name__)


class StripeWebhookEvent(Enum):
    CHECKOUT_SESSION_COMPLETED = "checkout.session.completed"
    CHECKOUT_SESSION_EXPIRED = "checkout.session.expired"


class InternalStripeService:
    def __init__(self):
        self.api_key = settings.STRIPE_API_SECRET_KEY
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET_KEY
        self.base_url = settings.BASE_URL
        self.mailer = MailService()

    def create_checkout_session(self, order: Order) -> str:
        """Create a new Stripe Checkout session."""
        checkout_session = stripe.checkout.Session.create(
            api_key=self.api_key,
            payment_method_types=["card"],
            line_items=self.get_line_items(order),
            customer_email=order.information.email,
            mode="payment",
            metadata=self.get_metadata(order),
            success_url=self.get_success_url(order),
            cancel_url=self.get_cancel_url(),
        )

        return checkout_session.url

    def get_success_url(self, order: Order) -> str:
        relative_url = reverse("core:thank_you", kwargs={"order_id": order.id})
        return f"{self.base_url}{relative_url}"

    def get_cancel_url(self) -> str:
        relative_url = reverse("core:readings")
        return f"{self.base_url}{relative_url}"

    def get_line_items(self, order: Order):
        """
        Retrieve the line items for the Stripe Checkout session.
        """

        item = order.item

        return [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{item.reading_type.reading.name} - {item.reading_type.get_type_display()}",
                    },
                    "unit_amount": self.get_reading_type_price(item),
                },
                "quantity": item.quantity,
            }
        ]

    def get_reading_type_price(self, order_item: OrderItem) -> int:
        """Retrieve the price of a ReadingType."""
        return int(order_item.get_total_price() * 100)

    def get_metadata(self, order: Order) -> dict:
        """Return the metadata for the Stripe Checkout session."""
        return {
            "order_id": str(order.id),
        }

    def process_stripe_event(self, payload: dict, sig_header: str):
        event = stripe.Webhook.construct_event(payload, sig_header, self.webhook_secret)
        event_type = event["type"]

        if event_type == StripeWebhookEvent.CHECKOUT_SESSION_COMPLETED.value:
            log.info("Processing checkout session completed event")
            self.process_checkout_session_completed(event["data"]["object"])

        elif event_type == StripeWebhookEvent.CHECKOUT_SESSION_EXPIRED.value:
            log.info("Processing checkout session expired event")
            self.process_checkout_session_expired(event["data"]["object"])

        else:
            log.warning(f"Unhandled event type: {event_type}")

    def process_checkout_session_completed(self, event_data: dict):
        order_id = event_data["metadata"]["order_id"]

        order = Order.objects.get(id=order_id)
        order.status = Order.Status.COMPLETED

        order.save()
        log.info(f"Order {order_id} has been marked as completed.")

        try:
            self.mailer.send_thank_you_email(order.information.email, order)

            notification_email = settings.SENDGRID_NOTIFICATION_EMAIL_SINGLE_RECIPIENT
            if notification_email:
                self.mailer.send_thank_you_email(notification_email, order)
        except Exception as e:
            log.error(
                f"Failed to send thank you email to {order.information.email}: {e}"
            )
        return order

    def process_checkout_session_expired(self, event_data: dict):
        order_id = event_data["metadata"]["order_id"]
        order = Order.objects.get(id=order_id)
        order.status = Order.Status.CANCELLED
        order.save()
        return order
