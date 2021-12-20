from django.core.mail import send_mail

from hotel._celery import app


@app.task
def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/account/activate/{activation_code}'
    message = f"""
        Thank you for signing up.
        Please, activate your account.
        Activation link: {activation_url}
    """
    send_mail(
        'Activate your account',
        message,
        'test@test.com',
        [email, ],
        fail_silently=False
    )

@app.task
def send_reset_code(email, activation_code):
    message = f"""
        Activation code: {activation_code}
    """
    send_mail(
        'Reset your password',
        message,
        'test@test.com',
        [email, ],
        fail_silently=False
    )


@app.task
def send_order_info(email, message):
    send_mail(
        'Order info',
        message,
        'test@test.com',
        [email, ],
        fail_silently=False        
    )