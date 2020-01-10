import sys
import os
from flask import render_template, flash, redirect, url_for, request, send_file
from app import app
from app.forms import ChooseForm, PreviewForm
from PIL import Image, ImageFont, ImageDraw
from uuid import uuid4 as uuid

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    title = 'Memexter'
    form = ChooseForm()

    if form.validate_on_submit():
        fontsize = int(form.fontSize.data)
        text1 = form.textU.data
        useD = form.useD.data
        text2 = form.textD.data
        app.logger.debug('test1')
        app.logger.debug(useD)
        if form.field.data == '1':
            if useD == True:
                app.logger.debug('debug1')
                return redirect(url_for('preview', filename="1.jpg", fontsize=fontsize, text1=text1, text2=text2, useD=useD))
            elif useD == False:
                app.logger.debug('debug2')
                return redirect(url_for('preview', filename="1.jpg", fontsize=fontsize, text1=text1, useD=useD))

             # Skicka vidare användaren till lämplig sida.
        elif form.field.data == '2':
            if useD == True:
                app.logger.debug('used=true')
                return redirect(url_for('preview', filename="2.jpg", fontsize=fontsize, text1=text1, text2=text2, useD=useD))
            elif useD == False:
                app.logger.debug('used=false')
                return redirect(url_for('preview', filename="2.jpg", fontsize=fontsize, text1=text1, useD=useD))
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
    useD = request.args['useD']
    if useD == "True":
        text2 = request.args['text2']

    form = PreviewForm()
    if form.validate_on_submit():
        if useD == "True" and text1 is not None and text2 is not None:
            X1 = form.left1.data
            Y1 = form.top1.data
            X2 = form.left2.data
            Y2 = form.top2.data
            return redirect(url_for('output', choice=choice, fontsize=fontsize, text1=text1, text2=text2, X1=X1, Y1=Y1, X2=X2, Y2=Y2, useD=useD))
        elif useD == "False" and text1 is not None:
            form.left2(disabled=True)
            form.top2(disabled=True)
            X1 = form.left1.data
            Y1 = form.top1.data
            return redirect(url_for('output', choice=choice, fontsize=fontsize, text1=text1, X1=X1, Y1=Y1, useD=useD))

    if useD == "True":
        return render_template('preview.html', imgpath=imgpath, fontsize=fontsize, text1=text1, text2=text2, form=form)
    elif useD == "False":
        return render_template('preview.html', imgpath=imgpath, fontsize=fontsize, text1=text1, form=form)



@app.route('/output', methods=['GET', 'POST'])
def output():
    uid = str(uuid())
    fontsize = request.args['fontsize']
    choice = request.args['choice']
    text1 = request.args['text1']
    text2 = request.args['text2']
    X1 = int(request.args['X1'])
    Y1 = int(request.args['Y1'])
    useD = request.args['useD']

    basedir = os.path.dirname(__file__)
    im = Image.open(os.path.join(basedir, 'static/images', choice))
    width, height = im.size
    xConst = width / 700
    yConst = height / 700
    newX = xConst * X1
    newY = yConst * Y1
    '''
    img cont  = 700px
    '''
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join(basedir, 'fonts', 'Roboto-Regular.ttf'), int(fontsize))
    draw.text((int(newX),int(newY)), text1, (0,0,0), font=font)
    if useD == "True":
        X2 = int(request.args['X2'])
        Y2 = int(request.args['Y2'])
        newX2 = xConst * X2
        newY2 = yConst * Y2
        draw.text((int(newX2),int(newY2)), text2, (0,0,0), font=font)
    path = os.path.join(basedir, 'static/memes', '{}.jpg'.format(uid))
    im.save(path)
    app.logger.debug('X1: %s', X1)
    app.logger.debug('Y1: %s', Y1)
    return render_template('output.html', fontsize=fontsize, text1=text1, text2=text2, X1=X1, Y1=Y1, uid=uid, id=id)
