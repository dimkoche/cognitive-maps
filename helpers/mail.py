import sendgrid


def is_email_valid(email):
    if not email:
        return False
    return True


def send_email(email, map, username, password):
    txt = """
        Hi!

        You have created a new cognitive map: %s. To start edit this map, open URL in your browser: http://d0h.ru/map/show/%s?key=%s

        d0h.ru
    """
    html = """
        <p>Hi!</p>
        <p>You have created a new cognitive map: %s. <a href="http://d0h.ru/map/show/%s?key=%s">Start edit this map</a></p>
        <p><a href="http://d0h.ru">d'Oh.ru</a></p>
    """
    if is_email_valid(email):
        s = sendgrid.Sendgrid(username, password, secure=True)
        message = sendgrid.Message(
            "no-reply@d0h.ru",
            "New map created (%s)" % map.hash,
            txt % (map.title, map.hash, map.passkey),
            html % (map.title, map.hash, map.passkey)
        )
        message.add_to(email)
        s.web.send(message)
