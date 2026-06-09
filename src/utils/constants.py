from datetime import datetime

APP_NAME = "Inventário IA"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Sistema Inteligente de Gestão"
APP_YEAR = datetime.now().year

CURRENCY_SYMBOL = "Kz"
CURRENCY_NAME = "Kwanza"
CURRENCY_CODE = "AOA"

DATE_FORMAT = "%d/%m/%Y"
DATETIME_FORMAT = "%d/%m/%Y %H:%M"
DATE_FORMAT_DISPLAY = "%d de %B de %Y"

ESTOQUE_MINIMO_PADRAO = 10
PONTO_PEDIDO_MARGEM = 10
DIAS_PREVISAO_PADRAO = 30
DIAS_HISTORICO_PADRAO = 60

PERFIL_ADMIN = "admin"
PERFIL_OPERADOR = "operador"

STATUS_ESTOQUE_NORMAL = "Normal"
STATUS_ESTOQUE_BAIXO = "Baixo"
STATUS_ESTOQUE_ESGOTADO = "Esgotado"

MENSAGENS = {
    'confirmar_saida': "Deseja realmente sair do sistema?",
    'confirmar_remocao': "Tem certeza que deseja remover este item?",
    'sucesso_cadastro': "Cadastro realizado com sucesso!",
    'sucesso_venda': "Venda registrada com sucesso!",
    'sucesso_remocao': "Item removido com sucesso!",
    'erro_autenticacao': "Nome de utilizador ou palavra-passe inválidos.",
    'estoque_insuficiente': "Estoque insuficiente para esta operação.",
    'sem_produtos': "Não há produtos cadastrados no sistema.",
}


def format_currency(value):
    if value is None:
        return f"{CURRENCY_SYMBOL} 0,00"
    return f"{CURRENCY_SYMBOL} {value:,.2f}"


def format_date(date_obj):
    if date_obj is None:
        return ""
    return date_obj.strftime(DATE_FORMAT)


def format_datetime(datetime_obj):
    if datetime_obj is None:
        return ""
    return datetime_obj.strftime(DATETIME_FORMAT)