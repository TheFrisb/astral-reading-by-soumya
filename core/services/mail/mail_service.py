import logging

from django.conf import settings
from django.urls import reverse
from django.utils.timezone import activate, deactivate
from sendgrid import SendGridAPIClient, Mail

from booking.models import ScheduledAppointment
from core.models import Order, ReadingType, SiteSettings

log = logging.getLogger(__name__)


class MailService:
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.default_from_mail = settings.DEFAULT_FROM_EMAIL
        self.notification_email_recipients = (
            settings.SENDGRID_NOTIFICATION_EMAIL_RECIPIENT
        )
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

    def send_booking_notification_email(
            self, scheduled_appointment: ScheduledAppointment
    ):
        """
        Sends a booking notification email with details about
        the Order, OrderItem, OrderInformation, and the ScheduledAppointment.
        """
        # 1) Activate PST timezone
        activate("America/Los_Angeles")

        # 2) Gather required data
        order = scheduled_appointment.order
        order_item = order.item
        order_info = order.information

        # 3) Construct the email subject
        subject = f"Booking Notification - Order #{order.id}"

        # 4) Construct the email body (HTML)
        body = f"""
        <html>
        <head></head>
        <body>
            <h1>Booking Notification</h1>

            <h2>Order Details</h2>
            <p><strong>Order ID:</strong> {order.id}</p>
            <p><strong>Status:</strong> {order.status}</p>

            <h2>Order Item</h2>
            <p><strong>Reading Type:</strong> {order_item.reading_type.get_display_name}</p>
            <p><strong>Quantity:</strong> {order_item.quantity}</p>
            <p><strong>Price:</strong> ${order_item.price}</p>
            <p><strong>Total Price:</strong> ${order_item.get_total_price()}</p>

            <h2>Order Information</h2>
            <p><strong>Full Name:</strong> {order_info.full_name}</p>
            <p><strong>Email:</strong> {order_info.email}</p>
            <p><strong>Phone Number:</strong> {order_info.phone_number}</p>
            <p><strong>Date of Birth:</strong> {order_info.date_of_birth}</p>
            <p><strong>Place of Birth:</strong> {order_info.place_of_birth}</p>
            <p><strong>Time of Birth:</strong> {order_info.time_of_birth}</p>
            <p><strong>Day Part:</strong> {order_info.day_part}</p>
            <p><strong>Comment:</strong> {order_info.comment}</p>

            <h2>Scheduled Appointment</h2>
            <p><strong>Start Time (PST):</strong> {scheduled_appointment.start_time}</p>
            <p><strong>End Time (PST):</strong> {scheduled_appointment.end_time}</p>
        </body>
        </html>
        """

        # 5) Create the SendGrid Mail object
        message = Mail(
            from_email=self.default_from_mail,
            to_emails=self.notification_email_recipients,
            subject=subject,
            html_content=body,
        )

        # 6) Send the email via SendGrid
        try:
            response = self.client.send(message)
            log.info(
                f"Sent booking notification email for Order #{order.id} with result: {response}"
            )
        except Exception as e:
            log.error(f"Failed to send booking notification email: {e}")
            raise e

        deactivate()
