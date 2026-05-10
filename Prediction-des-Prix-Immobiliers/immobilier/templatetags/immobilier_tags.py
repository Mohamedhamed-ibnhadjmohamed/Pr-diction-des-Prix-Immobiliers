from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplie deux valeurs"""
    try:
        return value * arg
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divise deux valeurs"""
    try:
        return value / arg if arg != 0 else 0
    except (ValueError, TypeError):
        return 0

@register.filter
def times(value):
    """Crée une séquence de nombres pour les boucles"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)

@register.simple_tag
def get_user_role_class(user):
    """Retourne la classe CSS correspondant au rôle de l'utilisateur"""
    if user.is_agent:
        return 'badge-primary'
    elif user.is_vendeur:
        return 'badge-success'
    elif user.is_acheteur:
        return 'badge-info'
    else:
        return 'badge-secondary'

@register.simple_tag
def get_property_status_class(property):
    """Retourne la classe CSS pour le statut d'une propriété"""
    # Vous pouvez ajouter une logique pour déterminer le statut
    return 'badge-secondary'

@register.filter
def format_price(price):
    """Formate un prix pour l'affichage"""
    try:
        return f"{float(price):,.0f}€".replace(',', ' ')
    except (ValueError, TypeError):
        return "0€"

@register.filter
def truncatechars_custom(value, arg):
    """Version personnalisée de truncatechars"""
    try:
        length = int(arg)
        if len(value) > length:
            return value[:length] + '...'
        return value
    except (ValueError, TypeError):
        return value
