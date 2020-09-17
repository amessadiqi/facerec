from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)

app.config.from_object('config')

from .utils import add_user, find_user_by_email, find_user_by_id, get_users, find_user_by_image, save_uploaded_image, \
    compare_faces, detect_faces


@app.route('/')
@app.route('/index/')
def index():
    if 'id' in session:
        users = get_users()
        return render_template('home.html', userId=session['id'], users=users)
    else:
        return render_template('login.html')


@app.route('/search/', methods=['POST'])
def search():
    if 'id' in session:
        image_path, _, image_filename = save_uploaded_image(request.files['image'], dir='/static/img/temp/')

        users = get_users()

        from time import time
        t1 = time()

        try:
            user_found = find_user_by_image(image_path)
        except:
            flash('No faces detected in this image')
            return redirect(url_for('index'))

        calculation_time = time() - t1

        # os.remove(image_path)

        return render_template('search.html', userId=session['id'], users=users, time=round(calculation_time, 4),
                               result=user_found, uploaded_image=image_filename)
    else:
        return render_template('404.html')


@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user = find_user_by_email(email=request.form['email'])

        if user is not None:
            if user.password == request.form['password']:
                session['id'] = user.id
            else:
                flash('Email or password is incorrect')
        else:
            flash('Email or password is incorrect')

    return redirect(url_for('index'))


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = find_user_by_email(email=request.form['email'])
        if user is not None:
            flash("Email already exists !")
            return render_template('signup.html')

        _, picture_uri, _ = save_uploaded_image(request.files['facialPicture'], dir='/static/img/pictures/')

        add_user(email=request.form['email'],
                 password=request.form['password'],
                 first_name=request.form['firstName'],
                 last_name=request.form['lastName'],
                 gender=request.form['gender'],
                 profile_picture=picture_uri,
                 birthday=request.form['birthday'],
                 address=request.form['address'])
        user = find_user_by_email(email=request.form['email'])
        session['id'] = user.id
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('signup.html')


@app.route('/compare/', methods=['POST'])
def compare():
    if 'id' in session:
        image1_path, _, image1_filename = save_uploaded_image(request.files['image1'], dir='/static/img/temp/')
        image2_path, _, image2_filename = save_uploaded_image(request.files['image2'], dir='/static/img/temp/')

        from time import time
        t1 = time()

        try:
            match = compare_faces(image1_path, image2_path)
        except:
            flash('No faces detected in one of these images or both')
            return redirect(url_for('index'))

        calculation_time = time() - t1

        users = get_users()

        return render_template('compare.html', users=users, result=match[0], img1=image1_filename, img2=image2_filename,
                               time=round(calculation_time, 4))
    else:
        return render_template('404.html')


@app.route('/analyser/')
def analyser():
    return render_template('analyser.html')


@app.route('/analyse/', methods=['POST'])
def analyse():
    if 'id' in session:
        image_path, _, image_filename = save_uploaded_image(request.files['image'], dir='/static/img/temp/')

        from time import time
        t1 = time()

        img_res = detect_faces(image_path, image_filename)

        calculation_time = time() - t1

        return render_template('analyse.html', img=img_res, time=round(calculation_time, 4))
    else:
        return render_template('404.html')


@app.route('/logout/')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')
