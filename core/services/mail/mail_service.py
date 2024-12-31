import logging

from django.conf import settings
from django.urls import reverse
from sendgrid import SendGridAPIClient

from core.models import Order, ReadingType, SiteSettings

log = logging.getLogger(__name__)


class MailService:
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.default_from_mail = settings.DEFAULT_FROM_EMAIL
        self.client = SendGridAPIClient(self.api_key)

    def send_thank_you_email(self, to_email, order: Order):
        message = {
            "personalizations": [
                {
                    "to": [{"email": to_email}],
                    "dynamic_template_data": self.get_thank_you_params(order),
                }
            ],
            "from": {"email": self.default_from_mail},
            "template_id": str(SiteSettings.get_solo().thank_you_template_id),
        }

        result = self.client.send(message)
        log.info(f"Sent thank you email to {to_email}, with result: {result}")

        return result

    def send_leave_a_review_email(self, to_email, order: Order):
        message = {
            "personalizations": [
                {
                    "to": [{"email": to_email}],
                    "dynamic_template_data": self.get_leave_a_review_params(order),
                }
            ],
            "from": {"email": self.default_from_mail},
            "template_id": str(SiteSettings.get_solo().leave_a_review_template_id),
        }

        result = self.client.send(message)
        log.info(f"Sent leave a review email to {to_email}, with result: {result}")
        return result

    def get_thank_you_params(self, order: Order):
        if order.item.reading_type.type == ReadingType.Type.CALL:
            info_text = "Click the button below to schedule your call."
            primary_button_text = "Schedule Call"
            primary_button_url = f"{settings.BASE_URL}{reverse(
                "booking:book_appointment", kwargs={"order_id": order.id}
            )}"
        else:
            info_text = (
                "You will receive an email with your reading in the next 7 days."
            )
            primary_button_text = "View other readings"
            primary_button_url = settings.BASE_URL

        return {
            "order_id": str(order.id),
            "order_total": str(order.item.get_total_price()),
            "order_item_name": order.item.reading_type.get_display_name,
            "info_text": info_text,
            "primary_button_text": primary_button_text,
            "primary_button_url": primary_button_url,
        }

    def get_leave_a_review_params(self, order):
        return {
            "primary_button_url": f"{settings.BASE_URL}{reverse('core:leave_review', kwargs={'order_id': order.id})}",
        }
