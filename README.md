from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def submit_message():
    if request.method == 'POST':
        message = request.form.get('message')
        email = request.form.get('email')
        text_message = request.form.get('text_message')
        return render_template('confirmation.html', message=message, email=email, text_message=text_message)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
    <!DOCTYPE html>
<html>
<head>
    <title>Submit a Message</title>
</head>
<body>
    <h2>Submit a Message</h2>
    <form method="POST" action="/Submit">
        Email: <input type="email" name="name"><br><br>
        Message: <input type="text" name="message"><br><br>
        <input type="Submit" value="Submit">
        </form>
    <p>See all message at <a href="/messages">/messages</a></p>
</body>
</html>
