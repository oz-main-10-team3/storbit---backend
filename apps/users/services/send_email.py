from django.core.mail import send_mail

from config.settings.base import EMAIL_HOST_USER


class SendEmailService:
    @staticmethod
    def signup_send_email(email, code):
        send_mail(
            subject="[Storbit] 회원가입 인증 코드 발송",
            message=f"인증코드: {code}\n 5분안에 입력해 주세요.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

    @staticmethod
    def find_password_send_email(email, code):
        send_mail(
            subject="[Storbit] 비밀번호 인증 코드 발송",
            message=f"인증코드: {code}\n 5분안에 입력해 주세요.",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
