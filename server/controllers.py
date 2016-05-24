import io

from flask_security import login_required
from flask_login import current_user
from flask_login import logout_user
from flask import request, send_file, send_from_directory
from flask import render_template
from flask import url_for
from flask import redirect

from server import app
from server.forms import EditForm
from server.utils import update_user_profile


@app.route('/', methods=['GET'])
@login_required
def index():
    """
    Home page
    :return:
    """
    return render_template('_index.html')


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    Home page
    :return:
    """
    return render_template('dashboard_pages/dashboard.html')


@app.route('/home', methods=['GET'])
def index2():
    """
    Home page
    :return:
    """
    return render_template('_index.html')


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditForm()

    if request.method == 'POST':
        if form.validate():
            image_data = request.files.get('avatar')
            update_user_profile(form, current_user.id,
                                image_data=image_data)
            return redirect(url_for('index'))
        else:
            return render_template('edit.html', form=form)
    else:
        return render_template('edit.html', form=form)


@app.route('/avatar', methods=['GET'])
@login_required
def get_avatar():
    """
    Gets avatar image from database.
    :return:
    """
    if current_user.avatar_image:
        avatar = current_user.avatar_image
    elif current_user.social_profiles:
        avatars = [p.avatar for p in current_user.social_profiles if p.avatar]

        if avatars:
            avatar = avatars[0]
        else:
            avatar = ''
    else:
        avatar = ''

    return send_file(io.BytesIO(avatar),
                     attachment_filename='avatar.png',
                     mimetype='image/png')


@app.route('/static/<path>', methods=['GET'])
def static_content(path):
    return send_from_directory(app.static_folder, path)
