from flask import Flask, request, render_template, redirect, url_for
from dto import UserDTO, BoardDTO
from dao import UserDAO, BoardDAO
import datetime
from flask_recaptcha import ReCaptcha
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['RECAPTCHA_SITE_KEY'] = '6LdI60gbAAAAAO9llS8p0UrBetVojtlG-1kuGm-l'
app.config['RECAPTCHA_SECRET_KEY'] = '6LdI60gbAAAAAPl2g8q9guBs2lFohFUnNNkdpLSQ'
recaptcha = ReCaptcha(app)


@app.route('/', methods=['POST', 'GET'])
def get():
    message = ''  # Create empty message
    print(request.method)
    if request.method == 'POST':  # Check to see if flask.request.method is POST
        if recaptcha.verify():  # Use verify() method to see if ReCaptcha is filled out
            message = 'Thanks for filling out the form!'  # Send success message
        else:
            message = 'Please fill out the ReCaptcha!'  # Send error message
    return render_template('index.html', message=message)


@app.route('/membership', methods=['GET', 'POST'])
def membership():
    return render_template('member.html')


@app.route('/insert', methods=['POST'])
def userinsert():
    global index_user_counter

    index_user_counter += 1

    dto = UserDTO(index_user_counter, request.form.get('user_name'),
                  request.form.get('user_pw'), request.form.get('user_interest'))
    dao = UserDAO().userinsert(dto)

    return render_template('index.html')


@app.route('/login', methods=['post'])
def userlogin():
    global uname
    uname = request.form.get('username')

    data = UserDAO().userone(request.form.get('username'), request.form.get('userpw'))
    print(data)
    if data is False:
        return render_template('index.html')
    else:
        return render_template('menu.html')


@app.route('/menu', methods=['get'])
def getmenu():
    return render_template('menu.html')


@app.route('/todolist', methods=['get'])
def gettodolist():
    return render_template('todolist.html')


@app.route('/list', methods=['get'])
def getlist():
    return render_template('list.html')


@app.route('/char2', methods=['get'])
def getchar2():
    return render_template('char2.html')


@app.route('/index2', methods=['get'])
def getchar3():
    return render_template('index2.html')


@app.route('/board', methods=['get'])
def getchar4():
    return render_template('board.html')


@app.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
    return render_template('menu.html')


@app.route('/todolist/gettext', methods=['post'])
def gettext():
    global index_text_counter
    global uname

    index_text_counter += 1
    dao = BoardDAO()
    uid = dao.getuserID(uname)

    now = datetime.datetime.now()
 
    nowDate = now.strftime('%Y-%m-%d')

    dto = BoardDTO(index_text_counter, request.form.get(
        'user_title'), request.form.get('user_text'), nowDate, uid[0])

    BoardDAO().textinsert(dto)
    return request.form.get('user_title')


@app.route('/list/showlist', methods=['post'])
def showtext():
    global uname
    print(uname)
    uid = BoardDAO().getuserID(uname)
    print(uid[0])
    data = BoardDAO().boardall(uid[0])

    return data


if __name__ == "__main__":
    index_user_counter = UserDAO().getIndex()
    index_text_counter = BoardDAO().getTextIndex()
    app.run(debug=True, host="127.0.0.1", port="5000")
