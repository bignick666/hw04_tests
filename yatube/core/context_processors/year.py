import datetime


def year(request):
    """Adding a parameter with current year"""
    return {
        'year': int(datetime.datetime.today().year)
    }
