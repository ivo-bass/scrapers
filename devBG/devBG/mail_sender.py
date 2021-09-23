from .config import config
import sqlite3
from datetime import date, timedelta


def send_email():
    # get new offers from db - last 2 days if not is_sent
    jobs = get_new_offers()

    # send msg, if not new offers send msg to confirm that
    send_msg(jobs)

    # set is_sent to 1 for each
    set_items_sent_in_db(jobs)


def get_new_offers():
    jobs_to_send = []
    try:
        connection = sqlite3.connect('./jobs.db')
        cursor = connection.cursor()
        print("Connected to SQLite")

        select_query = """
        SELECT rowid, * from jobs
        WHERE is_sent = 0
        """
        cursor.execute(select_query)
        records = cursor.fetchall()  # list(tuples)

        for row in records:
            row_date = row[4]
            job_date = get_job_date(row_date)
            if not job_date in dates_of_interest():
                continue
            jobs_to_send.append(row)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed")
        return jobs_to_send


def send_msg(jobs):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg["From"] = config.EMAIL_USER
    msg["To"] = config.EMAIL_USER
    msg["Subject"] = "Daily jobs report"
    content = set_msg_content(jobs)
    msg.set_content(content, subtype='html')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config.EMAIL_USER, config.EMAIL_PASS)
    server.send_message(msg)
    server.quit()

    print("Mail sent")


def set_msg_content(jobs):
    msg = """
    <!DOCTYPE html>
    <html>
    <body style="
    background-color: azure;
    color: #333;
    font-family: Helvetica, sans-serif;
    font-size: 14px;
    font-weight: 500;
    margin: 0;
    padding: 10px;
    ">

        <h1 style="color:darkslategrey;">Hello from the job scraper!</h1>
    """

    if jobs:
        msg += """
        <br>
        <p>I have found some new job offers.</p>
        <br>
        """
        for row in jobs:
            _, position, company, location, row_date, link, _ = row
            msg += f"""
            <hr>
            <table>
                <tr><td>Position:</td><td>{position}</td></tr>
                <tr><td>Company:</td><td>{company}</td></tr>
                <tr><td>Location:</td><td>{location}</td></tr>
                <tr><td>Date:</td><td>{row_date}</td></tr>
                <tr><td>Link:</td><td>{link}</td></tr>
            </table>
            <hr>
            """
    else:
        msg += """
        <br>
        <p>I have not found any new job offers today.</p>
        <br>
        """
    msg += """
        <br>
        <h3 style="color: darkslategray;">Have a nice day!</h3>
    </body>
    </html>
    """
    return msg


def set_items_sent_in_db(jobs):
    con = sqlite3.connect('./jobs.db')
    cur = con.cursor()
    for row in jobs:
        row_id = row[0]
        print(f"ID: {row_id} is sent")
        cur.execute(
            '''UPDATE jobs SET is_sent = 1 WHERE rowid = ?''',
            (row_id,)
        )
        con.commit()


def get_job_date(row_date):
    year, month, day = row_date.split('-')
    return date(int(year), int(month), int(day))


def dates_of_interest():
    current_date = date.today()
    yesterday = current_date - timedelta(days=1)
    return current_date, yesterday
