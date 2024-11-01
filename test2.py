from datetime import datetime
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d')
print(type(formatted_date))