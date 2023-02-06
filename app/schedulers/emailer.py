from django.core.mail import send_mail

from app.models import User, EmailHistory
from app.schedulers.re_connect_db import db_auto_reconnect
from app.utils import predict
from rainday.settings import EMAIL_HOST_USER


@db_auto_reconnect
def send_email():
    users = User.objects.filter(locations__isnull=False, is_staff=False, is_superuser=False, is_active=True).distinct()
    for user in users:
        try:
            send_mail(
                subject="[우리동네 기상청] 기상정보를 확인해보세요!",
                message="HTML을 지원하는 메일로 읽어보세요!",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
                html_message=get_html_message(user),
            )
        except Exception:
            EmailHistory.objects.create(user=user, success=False)
        else:
            EmailHistory.objects.create(user=user)
            print(f"Email sent to {user.email}")


def get_html_message(user):
    table = ""
    for location in user.locations.all():
        if predict(location):
            prediction = "비가 올 예정 입니다."
        else:
            prediction = "비가 오지 않을 예정 입니다."

        table += f"""
        <tr>
            <td>{location.station_name}</td>
            <td>{prediction}</td>
        </tr>
        """

    html_message = f"""
    <html>
        <head>
            <style>
                table, th, td {{
                    border: 1px solid black;
                    border-collapse: collapse;
                }}   
            </style>
        </head>
        <body>
            <h1>{user.username} 님 안녕하세요.</h1>
            <p>구독하신 지역의 기상정보를 확인해보세요!</p>
            <table>
                <tr>
                    <th>지역</th>
                    <th>예보</th>
                </tr>
                {table}
            </table>
        </body>
    </html>
    """
    return html_message
