from datetime import datetime, timedelta
from .models import License, Client, LicenseLog, EmailsLog
from django.core.mail import send_mail
from tabulate import tabulate
from email.mime.text import MIMEText
from django.utils import timezone
from pytz import timezone as tz

def enviar_licencias_a_clientes():
    clients = Client.objects.all()
    for client in clients:
        print(client)
        client_lisenses_4_mounth = getLisensesByDateFilter(client, "4_meses")
        client_lisenses_1_week = getLisensesByDateFilter(client, "1_semana")
        client_lisenses_1_month = getLisensesByDateFilter(client, "1_mes_lunes")
        if(len(client_lisenses_4_mounth) > 0):
            sendLisensesByEmail(client, client_lisenses_4_mounth, "Licencias que caducan en 4 meses")
        if(len(client_lisenses_1_week) > 0):
            sendLisensesByEmail(client, client_lisenses_1_week, "Licencias que caducan en 1 semana")
        if(len(client_lisenses_1_month) > 0):
            sendLisensesByEmail(client, client_lisenses_1_month, "Licencias que caducan en 1 mes y hoy es lunes")

def getLisensesByDateFilter(client, date_filter):
    local_tz = tz(timezone.get_current_timezone_name())
    hoy = local_tz.localize(datetime.now())
    print('datetoday')
    print(hoy)
    # Calcula las fechas de vencimiento para los diferentes criterios
    cuatro_meses_despues = hoy + timedelta(days=30 * 4)
    un_mes_despues = hoy + timedelta(days=30)
    una_semana_despues = hoy + timedelta(days=7)

    if date_filter == "4_meses":
        return License.objects.all()
    elif date_filter == "1_mes_lunes":
        return License.objects.filter(
            expiration_datetime=un_mes_despues,
            expiration_datetime__week_day=0 if hoy.weekday() == 0 else -1
        )
    elif date_filter == "1_semana":
        return License.objects.filter(expiration_datetime=una_semana_despues)
    


def sendLisensesByEmail(client, lisenses, mensaje):
    print('sendLisensesByEmail')
    tabla_html = "<table>"
    tabla_html += "<tr><th>Package</th><th>License Type</th><th>Expiration Date</th></tr>"
    for licencia in lisenses:
        tabla_html += f"<tr><td>{licencia.get_lisense_package_display()}</td><td>{licencia.get_license_type_display()}</td><td>{licencia.expiration_datetime}</td></tr>"
    tabla_html += "</table>"

    subject = mensaje
    message = MIMEText(tabla_html, 'html')
    from_email = 'afinidata@gmail.com'  # Reemplaza con tu dirección de correo
    recipient_list = [client.poc_contact_email]  # Reemplaza con la dirección de correo del destinatario
    
    send_mail(subject, '', from_email, recipient_list,  html_message=str(tabla_html), fail_silently=False)
    LicenseLog.objects.create(license=lisenses[0])
    EmailsLog.objects.create(subject=subject, sender=from_email, recipient=recipient_list[0], body=tabla_html)