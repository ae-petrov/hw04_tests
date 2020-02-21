import datetime as dt

def year(request):
    d = dt.datetime.today()
    return {
        'year': d.year
    }