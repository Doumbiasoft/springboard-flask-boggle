from flask import Flask,redirect,render_template,session,request,flash,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] ="AzertyQuerty"
app.config['DEBUG_TB_INTERCEPT_REDIRECT'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
toolbar = DebugToolbarExtension(app)


boggle_game = Boggle()
boggle_board="board"
high_score="high_score"
number_of_play="number_of_play"
board_size="board_size"

@app.route("/")
def init():
    """Setting the board by selecting the size of the board."""
    return render_template("init.html")

@app.route("/start-game", methods=["POST"])
def start():
    session[board_size]=request.form.get("size",4)
    return redirect("/index")

@app.route("/index")
def index():
    """Generate board."""

    boardsize = session.get(board_size, 4)
    board = boggle_game.make_board(boardsize)
    session[boggle_board] = board
    highscore = session.get(high_score, 0)
    numbofplay = session.get(number_of_play, 0)

    return render_template("index.html", board=board,highscore=highscore,numbofplay=numbofplay)


@app.route("/check-word")
def check_valid_word():
    """Check if word is valid word."""

    word = request.args.get("word")
    board = session.get(boggle_board)
    result = boggle_game.check_valid_word(board, word)

    return jsonify({'result': result})


@app.route("/post-score", methods=["POST"])
def send_score():
    """Receive current score and check if current score is grater than highest score update so ."""

    currentscore = request.json.get("score")
    highscore = session.get(high_score, 0)
    numbofplay = session.get(number_of_play, 0)

    session[number_of_play] = numbofplay + 1
    session[high_score] = max(currentscore, highscore)

    if currentscore > highscore:
       new_highscore=currentscore

    return jsonify(new_highscore=new_highscore)

