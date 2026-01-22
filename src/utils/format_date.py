def format_date(dt):
    if dt is None:
        return None

    if isinstance(dt, str):
        return dt 
    
    return dt.strftime('%Y-%m-%d')