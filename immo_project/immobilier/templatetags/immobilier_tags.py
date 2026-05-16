from django import template

register = template.Library()


@register.filter
def mul(value, arg):
    """Multiplie value par arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def div(value, arg):
    """Divise value par arg."""
    try:
        arg = float(arg)
        return float(value) / arg if arg != 0 else 0
    except (ValueError, TypeError):
        return 0


@register.filter
def prix_dt(value):
    """Formate un prix en Dinars Tunisiens."""
    try:
        return f"{float(value):,.0f} DT".replace(',', ' ')
    except (ValueError, TypeError):
        return "0 DT"


@register.filter
def stars(value):
    """Retourne une chaîne d'étoiles pleines/vides pour une note /5."""
    try:
        n = int(value)
        return '★' * n + '☆' * (5 - n)
    except (ValueError, TypeError):
        return '☆☆☆☆☆'


@register.simple_tag
def role_badge(role):
    mapping = {
        'admin':        ('danger',  'Administrateur'),
        'agent':        ('primary', 'Agent'),
        'vendeur':      ('success', 'Vendeur'),
        'proprietaire': ('success', 'Propriétaire'),
        'acheteur':     ('info',    'Acheteur'),
        'investisseur': ('warning', 'Investisseur'),
    }
    color, label = mapping.get(role, ('secondary', role))
    return f'<span class="badge bg-{color}">{label}</span>'
