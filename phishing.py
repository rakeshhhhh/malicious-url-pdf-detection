from fileinput import filename
import os
import pandas as pd
import fitz  # PyMuPDF
import pickle
import base64
import nice

from flask import Flask, render_template, request, session, redirect, url_for
from DBConnection import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "Remya"

UPLOAD_FOLDER = '/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['pdf'])  # Restrict to PDF only for this part of the app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load the model, scaler, imputer, and column names
with open('knn_model.pkl', 'rb') as model_file, \
     open('scaler.pkl', 'rb') as scaler_file, \
     open('imputer.pkl', 'rb') as imputer_file, \
     open('column_names.pkl', 'rb') as columns_file:
    model = pickle.load(model_file)
    scaler = pickle.load(scaler_file)
    imputer = pickle.load(imputer_file)
    columns = pickle.load(columns_file)

def extract_pdf_features(pdf_file):
    features = []
    try:
        # Open the PDF file
        pdf_file.seek(0)
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

        # Feature 1: Size of the PDF file in bytes
        pdf_file.seek(0, 2)
        pdfsize = pdf_file.tell() / 1024  # Convert bytes to kilobytes
        pdf_file.seek(0)

        # Feature 2: Number of pages
        pages = doc.page_count

        # Feature 3: Number of title characters
        title_chars = len(doc.metadata.get("title", ""))

        # Feature 4: Number of images
        images = sum(len(page.get_images(full=True)) for page in doc)

        # Read the PDF content as bytes
        pdf_content = pdf_file.read()
        
        # Reset the pointer after reading
        pdf_file.seek(0)

        # Feature 5-18: Count occurrences of specific keywords
        keywords = [b'obj', b'endobj', b'stream', b'endstream', b'xref', b'trailer',
                    b'startxref', b'ObjStm', b'JS', b'OBS_JS', b'Javascript', b'OBS_Javascript',
                    b'OpenAction', b'OBS_OpenAction', b'Acroform', b'OBS_Acroform']
        keyword_counts = [pdf_content.count(keyword) for keyword in keywords]

        features = [pdfsize, pages, title_chars, images] + keyword_counts

        doc.close()

    except Exception as e:
        print(f"Error reading PDF: {e}")

    print(f"Extracted features: {features} (Length: {len(features)})")
    return features

@app.route('/')
def login():
    return render_template("index.html")

@app.route('/result_predict', methods=['POST'])
def result_predict():
    if 'pdf_file' not in request.files:
        return render_template('user/detecter.html', error="No file uploaded.")

    pdf_file = request.files['pdf_file']

    # Check if file is a PDF
    if pdf_file.filename == '':
        return render_template('user/detecter.html', error="No selected file.")

    if not allowed_file(pdf_file.filename):
        return render_template('detecter.html', error="File type not allowed. Please upload a PDF file.")

    try:
        # Extract features from the PDF
        pdf_features = extract_pdf_features(pdf_file)

        if len(pdf_features) != len(columns):
            return render_template('user/detecter.html', error=f"Invalid PDF file format. Extracted features: {len(pdf_features)}.")

        # Convert features to DataFrame and handle missing values
        pdf_df = pd.DataFrame([pdf_features], columns=columns)
        pdf_df_imputed = pd.DataFrame(imputer.transform(pdf_df), columns=columns)

        # Standardize the features
        pdf_features_scaled = scaler.transform(pdf_df_imputed)

        # After extracting and scaling features, add debug statements
        print(f"Extracted features: {pdf_features}")
        print(f"Imputed features: {pdf_df_imputed}")
        print(f"Scaled features: {pdf_features_scaled}")

        # Make prediction
        prediction = model.predict(pdf_features_scaled)
        result = 'Malicious' if prediction[0] == 0 else 'Benign'
        
        if result == 'Benign':
            # Read the PDF content
            pdf_file.seek(0)
            pdf_content = pdf_file.read()
            encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')
            return render_template('user/detecter.html', result=f"The uploaded PDF is: {result}", benign=True, pdf_content=encoded_pdf)
        else:
            return render_template('user/detecter.html', result=f"The uploaded PDF is: {result}")

    except Exception as e:
        print(f"Error during PDF processing: {e}")
        return render_template('user/detecter.html', error="An error occurred while processing the PDF.")

@app.route('/detecter')
def detecter():
    return render_template("user/detecter.html")


@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    db=Db()
    qry="SELECT * FROM `login` WHERE `User_name`='"+username+"' AND `Password`='"+password+"'"
    res=db.selectOne(qry)
    if res is not None:
        session['lid']=res['Login_id']
        if res['User_type']=='admin':
            return redirect('/ahome')
        elif res['User_type']=='user':
            return redirect('/uhome')
        else:
            return '''<script>alert("invalid user");window.location='/'</script>'''
    else:
        return '''<script>alert("invalid user");window.location='/'</script>'''

@app.route('/logout')
def logout():
    session['lid']=''
    return redirect('/login')

@app.route('/ahome')
def ahome():
    if session['lid']!='':
        return render_template("admin/index.html")
    else:
        return redirect('/login')

@app.route('/change_password')
def change_password():
    if session['lid'] != '':
        return render_template("admin/Change_password.html")
    else:
        return redirect('/login')
@app.route('/change_password_post',methods=['post'])
def change_password_post():
    currentpassword=request.form['textfield']
    newpassword=request.form['textfield2']
    confirmpassword=request.form['textfield3']
    db=Db()
    qry="SELECT * FROM `login` WHERE `Password`='"+currentpassword+"' AND `Login_id`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    if res is not None:
        if newpassword==confirmpassword:
            db=Db()
            qry1="update `login` set `Password`='"+confirmpassword+"' where `Login_id`='"+str(session['lid'])+"'"
            res1=db.update(qry1)

            return '''<script>alert("Password successfully changed");window.location='/'</script>'''
        else:
            return '''<script>alert("Password does not match");window.location='/change_password'</script>'''
    else:
      return  '''<script>alert("invalid user");window.location='/change_password'</script>'''





#########################user




@app.route('/uhome')
def uhome():
    return render_template("user/u_index.html")


@app.route('/view_profile')
def view_profile():
    db=Db()
    qry="SELECT * FROM `user` WHERE `Login_id`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    return render_template("user/view_profile.html",data=res)



@app.route('/user_change_password')
def user_change_password():
    return render_template("user/changepassword.html")

@app.route('/user_change_password_post',methods=['post'])
def user_change_password_post():
    db=Db()
    current_password=request.form['textfield']
    new_password=request.form['textfield2']
    confirm_password=request.form['textfield3']
    qry = "SELECT * FROM `login` WHERE `Password`='" + current_password + "' AND `Login_id`='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    if res is not None:
        if new_password == confirm_password:
            db = Db()
            qry ="update `login` set `Password`='" + confirm_password + "' Where `Login_id`='" + str(session['lid']) + "'"
            res = db.update(qry)
            return '''<script>alert("Password successfully changed");window.location='/'</script>'''
        else:
            return '''<script>alert("Password does not match");window.location='/user_change_password'</script>'''
    else:
        return '''<script>alert("invalid user");window.location='/user_change_password'</script>'''

@app.route('/edit_profile')
def edit_profile():
    db=Db()
    qry="SELECT * FROM `user` WHERE `Login_id`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)

    return render_template("user/edit_profile.html",data=res)

@app.route('/user_edit_profile',methods=['post'])
def user_edit_profile():
    db=Db()
    Name=request.form['textfield']
    Place=request.form['textfield2']
    Post=request.form['textfield3']
    Pin=request.form['textfield4']
    District=request.form['textfield5']
    Phone_no=request.form['textfield6']
    Gender=request.form['RadioGroup1']
    Email=request.form['textfield7']
    qry="UPDATE `user` SET `Name`='"+Name+"',`place`='"+Place+"',`post`='"+Post+"',`Pin`='"+Pin+"',`District`='"+District+"',`Phone_no`='"+Phone_no+"',`Gender`='"+Gender+"',`Email`='"+Email+"' WHERE `Login_id`='"+str(session['lid'])+"'"
    res=db.update(qry)


    return '''<script>alert("successfully updated");window.location='/view_profile'</script>'''

@app.route('/signup')
def signup():
    return render_template("user/registerindex.html")

@app.route('/signup_post',methods=['post'])
def signup_post():

    db=Db()
    Name=request.form['textfield']
    Place=request.form['textfield2']
    Post=request.form['textfield3']
    Pin=request.form['textfield4']
    District=request.form['textfield5']
    Phone_no=request.form['textfield6']
    Gender=request.form['RadioGroup1']
    Email=request.form['textfield7']
    Password=request.form['textfield8']
    Confirm_password=request.form['textfield9']
    if Password==Confirm_password:
        qry="INSERT INTO `login`(`User_name`,`Password`,`User_type`)VALUES('"+Email+"','"+Confirm_password+"','user')"
        res=db.insert(qry)
        qry2="INSERT INTO `user`(`Login_id`,`Name`,`place`,`post`,`Pin`,`District`,`Phone_no`,`Gender`,`Email`)VALUES('"+str(res)+"','"+Name+"','"+Place+"','"+Post+"','"+Pin+"','"+District+"','"+Phone_no+"','"+Gender+"','"+Email+"')"
        res2=db.insert(qry2)
        return '''<script>alert("success");window.location='/'</script>'''
    else:
        return '''<script>alert("incorrect password");window.location='/'</script>'''


@app.route('/user_detect', methods=['GET', 'POST'])
def user_detect():
    if request.method == 'POST':
        if 'file' not in request.files:
            return '''<script>alert("No file part");window.location='/user_detect'</script>'''
        file = request.files['file']
        if file.filename == '':
            return '''<script>alert("No selected file");window.location='/user_detect'</script>'''
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '''<script>alert("File uploaded successfully");window.location='/user_detect'</script>'''
    return render_template("user/index2.html")


@app.route('/predict',methods=["GET", "POST"])
def result():
    if request.method == "POST":
        url = request.form["url"]
        method=request.form["modelname"]
        print(method)
        data   = nice.getResult2(url,method)
        print(data)
        return render_template('user/result.html',data=data)
  #  url  = request.args['url']
  #  modelname  = request.args['modelname']
        # print(url,"haiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        # if method=="logisticregression" or method=="RandomForest":
        #     data   = phishing_detection.getResult(url,method)
        #     print(data)
        #     return render_template('user/index2.html',data=data)
        # else:
        #     phishing_detection.getResult2(url,method)





if __name__ == '__main__':
    app.run(debug=True)
