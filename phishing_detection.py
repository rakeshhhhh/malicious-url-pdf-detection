import numpy as np
import pandas as pd
import feature_extraction
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression 
from flask import jsonify
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
from decimal import Decimal
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

def getResult(url,method):
    print(url,"-----------------------------------------")
    #Importing dataset
    data = pd.read_csv('Dataset\dataset.csv',delimiter=",")

    #Seperating features and labels
    X = np.array(data.iloc[: , :-1])
    y = np.array(data.iloc[: , -1])

    #print(type(X))
    #Seperating training features, testing features, training labels & testing labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
   # classifier = RandomForestClassifier()
    if method=="logisticregression":            
            classifier = LogisticRegression()
            classifier.fit(X_train, y_train)
            score = classifier.score(X_test, y_test)
            score = score*100
            print(score,"::::::::::::score")
            X_new = []
            X_input = url
            X_new=feature_extraction.generate_data_set(X_input)
            X_new = np.array(X_new).reshape(1,-1)
            analysis_result = ""
            try:
                prediction = classifier.predict(X_new)
                print(prediction)
                print("------------------------------")
                if prediction == -1:
                    analysis_result = "Phishing URL"
                    
                elif prediction == 0:
                    analysis_result = "This website has been detected as Suspecious"
                else:
                    analysis_result = "This website has been detected as Legitimate URL"
            except Exception as a:
                print(a)
                analysis_result = "This website has been detected as Phishing URL"

            result_of_analysis = """<section class="iq-about overview-block-pt iq-hide">
                                            <div class="container">
                                                <div class="row align-items-end">
                                                    <div class="col-lg-8 col-md-12">
                                                        <div class="about-content">
                                                            <h1 class="text-about iq-tw-6">Result of Your URL : <span class="iq-font-green iq-fw-8">"""+url+"""</span></h1>
                                                            <ul class="listing-mark iq-mtb-20 iq-tw-6 iq-font-black">
                                                                <li class="good">"""+analysis_result+"""</li>
                                                            </ul>
                                                            <h5 class="iq-mt-20 iq-mb-20" style="color: #65d972;font-size: 16px;">Accuracy : """+str(score)+"""div>
                                                    </div>
                                                </div></h5>
                                                        </
                                            </div>
                                        </section>
                                        """
            dictt={"prediction":analysis_result,
                "res":prediction,
                   "score":score,
                   "url":url   
                   }
            return dictt 
    else:
        classifier = RandomForestClassifier()
        classifier.fit(X_train, y_train)
        score = classifier.score(X_test, y_test)
        score = score*100
        print(score,"::::::::::::score")
        X_new = []
        X_input = url
        X_new=feature_extraction.generate_data_set(X_input)
        X_new = np.array(X_new).reshape(1,-1)
        analysis_result = ""
        try:
            prediction = classifier.predict(X_new)
            print(prediction)
            if prediction == -1:
                analysis_result = "Phishing URL"
            elif prediction == 0:
                analysis_result = "This website has been detected as Suspecious"
            else:
                analysis_result = "This website has been detected as Legitimate URL"
        except Exception as a:
           
            analysis_result = "This website has been detected as Phishing URL"

        result_of_analysis = """<section class="iq-about overview-block-pt iq-hide">
                                        <div class="container">
                                            <div class="row align-items-end">
                                                <div class="col-lg-8 col-md-12">
                                                    <div class="about-content">
                                                        <h1 class="text-about iq-tw-6">Result of Your URL : <span class="iq-font-green iq-fw-8">"""+url+"""</span></h1>
                                                        <ul class="listing-mark iq-mtb-20 iq-tw-6 iq-font-black">
                                                            <li class="good">"""+analysis_result+"""</li>
                                                        </ul>
                                                        <h5 class="iq-mt-20 iq-mb-20" style="color: #65d972;font-size: 16px;">Accuracy : """+str(score)+"""div>
                                                </div>
                                            </div></h5>
                                                    </
                                        </div>
                                    </section>
                                    """
   #     print(result_of_analysis,"resssssssssssssssssssssult")
        dictt={"prediction":analysis_result,
                "res":prediction,
                   "score":score,   
                    "url":url  
                   }
        print("-----------------------------------------------")
        print(dictt)
        
    #        print(result_of_analysis,"resssssssssssssssssssssult")
        return dictt

    
    
        
        
              
    
    
    
def getResult2(url,modelname):
    if modelname=="Decision tree":       
        file = open("pickle/model.pkl","rb")
        tree = pickle.load(file)
        file.close() 
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 
        y_predc =tree.predict(x)[0]
        print(y_predc)
       # a=tree.predict_proba(x)[0,0]
       # print(a)
    if modelname=="Gradient":
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30)
        file = open("picle/best.pkl","rb")
        gbc = pickle.load(file)
        file.close() 
        y_pred =gbc.predict(x)[0]
        # y_pro_malicious = gbc.predict_proba(x)[0,0]
        y_pro_non_malicious = gbc.predict_proba(x)[0,1]
        y_pro_malicious= Decimal('1') - Decimal(str(y_pro_non_malicious))
        y_pro_malicious=float(y_pro_malicious)
        print(y_pro_malicious)
        if y_pro_malicious>0.50:
           print("it is a malicious url")
        else:
           print("it is a legitimate url")