from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import datetime


app = Flask(__name__, static_url_path='/static')
app.secret_key = "your_secret_key"

users = []

isLoggedIn = True

@app.route("/")
def index():
    if "username" in session:
        return render_template("home.html", username=session["username"],isLoggedIn=isLoggedIn)
    else:
        return redirect(url_for("home", message="Invalid"))

@app.route("/home")
def home():
    return render_template("home.html",isLoggedIn=False)
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        for user in users:
            if user["username"] == username and user["password"] == password:
                session["username"] = username
                return redirect(url_for("index"))
        return render_template("login.html", message="Invalid username or password")
    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            return render_template("signup.html", message="Passwords do not match")
        for user in users:
            if user["username"] == username:
                return render_template("signup.html", message="Username already exists")
        users.append({"username": username, "password": password})
        session["username"] = username
        return redirect(url_for("index"))
    else:
        return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route('/ece')
def ece():
    return render_template('ece.html')

@app.route('/semester')
def semester():
    return render_template('semester.html')


@app.route('/forum')
def forum():
    return render_template('forum.html')

@app.route('/selfnotes')
def selfnotes():
    return render_template('selfnotes.html')

posts = []

@app.route('/post1', methods=['GET', 'POST'])
def post1():
    if request.method == 'POST':
        post_content = request.form['content']
        username = session.get('username')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post = {'content': post_content, 'date': current_time, 'username': username, 'replies': []}

        # Get the index of the post being replied to, if any
        reply_to = request.args.get('reply_to')
        if reply_to is not None:
            reply_to_index = int(reply_to)
            post_to_reply = posts[reply_to_index]
            reply_content = request.form['reply']
            reply = {'content': reply_content, 'date': current_time, 'username': username}
            post_to_reply['replies'].append(reply)

        # Add the new post to the list of posts
        posts.append(post)

        return redirect('/post1')
    else:
        return render_template('post.html', posts=posts)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    post = posts[post_id]
    username = session.get('username')
    if post['username'] == username:
        posts.pop(post_id)
        flash('Post deleted successfully')
        return redirect('/post1')
    else:
        flash('You are not authorized to delete this post.')
        return redirect('/post1')


@app.route('/reply/<int:post_index>', methods=['POST'])
def reply(post_index):
    reply_content = request.form['reply']
    username = session.get('username')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    reply = {'content': reply_content, 'date': current_time, 'username': username }
    posts[post_index]['replies'].append(reply)
    return redirect('/post1')




if __name__ == "__main__":
    app.run(debug=True)



