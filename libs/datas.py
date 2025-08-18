import locale
from datetime import datetime


def data_formatada(data):
    locale.setlocale(locale.LC_TIME, 'pt_BR')
    resultado = datetime.strptime(data, '%m/%d/%Y').strftime('%d de %B de %Y')
    if resultado.startswith('0'):
        resultado = resultado[1:]

    return resultado
