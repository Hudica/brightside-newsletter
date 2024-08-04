from app import app
from app import Subscriber
ctx = app.app_context()
ctx.push()
subscribers = Subscriber.query.all()

for sub in subscribers:
    print(sub.email)

ctx.pop()

# Exit the Python shell
exit()