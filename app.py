from flask import Flask, render_template, request
import requests
import smtplib

EMAIL = "unknownloop11@gmail.com"
PASSWORD = "dqrevgpozjiseqiz"

posts = requests.get(url="https://api.npoint.io/8166b49c41eccddf25c6").json()
app = Flask(__name__)


def mail(**info):
    content = f"Name: {info['name']}\nEmail: {info['email']}\nPhone: {info['phone']}\nMessage: {info['msg']}"
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.connect("smtp.gmail.com", 587)
        server.starttls()
        server.ehlo()
        server.login(user=EMAIL, password=PASSWORD)
        server.ehlo()
        server.sendmail(from_addr=EMAIL, to_addrs="slims2854@gmail.com", msg=f"Subject:Shade Blogs\n\n{content}")
        server.ehlo()


@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        mail(name=request.form['name'], email=request.form['email'], phone=request.form['phone'],
             msg=request.form['msg'])
        return render_template("success.html", name=request.form['name'])
    else:
        return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)

