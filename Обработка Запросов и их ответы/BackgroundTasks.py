from fastapi import BackgroundTasks, FastAPI

app=FastAPI()


#В этом примере, когда клиент отправляет запрос на маршрут /send-notification/{email}, ответ отправляется сразу,
# но задача отправки уведомления (запись в файл) выполняется в фоновом режиме.
def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}