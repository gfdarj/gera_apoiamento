import locale
from datetime import datetime


def data_formatada(data):
    locale.setlocale(locale.LC_TIME, 'pt_BR')
    resultado = datetime.strptime(data, '%m/%d/%Y').strftime('%d de %B de %Y')
    if resultado.startswith('0'):
        resultado = resultado[1:]

    return resultado


def is_valid_date(date_str, date_format):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def data_por_extenso(data_str):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    data_str = data_str.replace("/", "-")
    data_conv = datetime.strptime(data_str, "%d-%m-%Y")

    return data_conv.strftime('%d de %B de %Y')


