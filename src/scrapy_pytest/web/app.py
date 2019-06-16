from flask import Flask, render_template
from .config import DevelopmentConfig
from .common import get_responses

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


@app.route('/')
def home():
    responses = get_responses()
    return render_template('index.html', **{'responses': dict(responses)})


@app.route('/delete/<req_id>')
def delete(req_id):
    pass


if __name__ == '__main__':
    app.run()
