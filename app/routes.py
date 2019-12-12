import sys
from PIL import Image, ImageFont, ImageDraw
from flask import render_template, flash, redirect, url_for, request, send_file
from app import app
from app.forms import ChooseForm, PreviewForm
import os
from uuid import uuid4 as uuid

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    title = 'Memexter'
    form = ChooseForm()

    if form.validate_on_submit():
        if form.field.data == '1':
            fontsize = int(form.fontSize.data)
            text1 = form.textU.data
            text2 = form.textD.data
            return redirect(url_for('preview', filename="1.jpg", fontsize=fontsize, text1=text1, text2=text2))

             # Skicka vidare användaren till lämplig sida.
        elif form.field.data == '2':
            fontsize = int(form.fontSize.data)
            basedir = os.path.dirname(__file__)
            im = Image.open(os.path.join(basedir, 'static/images', '2.jpg'))
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype(os.path.join(basedir, 'fonts', 'Roboto-Regular.ttf'), fontsize)
            draw.text((400, 150), form.textU.data, (0,0,0), font=font)
            draw.text((400,400), form.textD.data, (0,0,0), font=font)

            path = os.path.join(basedir, 'static/memes', '{}.jpg'.format(id))
            im.save(path)
            app.logger.debug('Choice: %s', form.field.data)
            app.logger.debug('Id: %s', id)
            app.logger.debug('Path: %s', path) #tillämpa bilden
            return redirect(url_for('output', id=id))
        else:
            return 'error'

    return render_template('index.html', title=title, form=form)

@app.route('/preview', methods=['GET', 'POST'])
def preview():
    title = 'preview'
    choice = request.args['filename']
    imgpath = 'images/' + choice
    fontsize = request.args['fontsize']
    text1 = request.args['text1']
    text2 = request.args['text2']
    form = PreviewForm()
    if form.validate_on_submit() and text1 is not None and text2 is not None:
        X1 = form.left1.data
        Y1 = form.top1.data
        return redirect(url_for('output', id=id, fontsize=fontsize, text1=text1, text2=text2, X1=X1, Y1=Y1))
    return render_template('preview.html', imgpath=imgpath, fontsize=fontsize, text1=text1, text2=text2, form=form)



@app.route('/output', methods=['GET', 'POST'])
def output():
    uid = str(uuid())
    fontsize = request.args['fontsize']
    text1 = request.args['text1']
    text2 = request.args['text2']
    X1 = request.args['X1']
    Y1 = request.args['Y1']
    basedir = os.path.dirname(__file__)
    im = Image.open(os.path.join(basedir, 'static/images', "1.jpg"))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join(basedir, 'fonts', 'Roboto-Regular.ttf'), int(fontsize))
    draw.text((int(X1),int(Y1)), text1, (0,0,0), font=font)
    draw.text((700,500), text2, (0,0,0), font=font)
    path = os.path.join(basedir, 'static/memes', '{}.jpg'.format(uid))
    im.save(path)
    app.logger.debug('X1: %s', X1)
    app.logger.debug('Y1: %s', Y1)
    return render_template('output.html', fontsize=fontsize, text1=text1, text2=text2, X1=X1, Y1=Y1, uid=uid)
