from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

def print_hello():
    print("Hello")

scheduler = BlockingScheduler()
# scheduler = BackgroundScheduler()
scheduler.add_job(print_hello, trigger='interval', seconds=4)
scheduler.start()