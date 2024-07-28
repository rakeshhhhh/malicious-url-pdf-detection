import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from flask import jsonify
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction
from decimal import Decimal

def getResult2(url,modelname):
    if modelname=="Decision tree":       
         file = open("pickle/decisiontree.pkl","rb")
         tree = pickle.load(file)
         file.close() 
         obj = FeatureExtraction(url)
         x = np.array(obj.getFeaturesList()).reshape(1,30) 
         y_predc =tree.predict(x)[0]
         print(y_predc) 
         accuracy="0.960"
         if y_predc==1:
            y_pro_non_phishing = tree.predict_proba(x)[0,1] 
            chance=y_pro_non_phishing*100
            #chance="it has ",y_pro_non_phishing*100,"%","chance of being non malicious url"
            analysis_result="it is a legitimate url"    
            # dictt={"prediction":analysis_result,
            #         "res":prediction,
            #        "accuracy":y_predc,
            #        "chance":chance,
            #        "url":url   
            #        }
            # return dictt
         else:
               analysis_result="it is a malicious url"    
               y_pro_phishing = tree.predict_proba(x)[0,0]
               chance=y_pro_phishing*100
               print("malicious url")
         
         dictt={"results":analysis_result,
                "prediction":y_predc,
                "score":chance,
                 "url":url,
                 "accuracy":accuracy   
                   }
         return dictt 
         
        
       # a=tree.predict_proba(x)[0,0]
       # print(a)     
    if modelname=="Gradient":       
         file = open("pickle/gradient.pkl","rb")
         gradient = pickle.load(file)
         file.close() 
         obj = FeatureExtraction(url)
         accuracy="0.974"
         x = np.array(obj.getFeaturesList()).reshape(1,30) 
         y_predc =gradient.predict(x)[0]
         print(y_predc) 
         if y_predc==1:
            y_pro_non_phishing = gradient.predict_proba(x)[0,1]
            analysis_result="it is a legitimate url"
            chance=y_pro_non_phishing*100 
            print(y_pro_non_phishing*100)
            print("it has ",y_pro_non_phishing*100, " chance of being non malicious url")
            print("it is a legitimate url")
         else:
               y_pro_phishing = gradient.predict_proba(x)[0,0]
               analysis_result="it is a malicious url"
               chance=y_pro_phishing*100
               print("malicious url")
               
         dictt={"results":analysis_result,
                "prediction":y_predc,
                "score":chance,
                 "url":url,
                 "accuracy":accuracy   
                   }
         return dictt 
   
    if modelname=="RandomForest":       
         file = open("pickle/randomforest.pkl","rb")
         rand = pickle.load(file)
         file.close() 
         obj = FeatureExtraction(url)
         accuracy="0.968"
         x = np.array(obj.getFeaturesList()).reshape(1,30) 
         y_predc =rand.predict(x)[0]
         print(y_predc) 
         if y_predc==1:
            y_pro_non_phishing = rand.predict_proba(x)[0,1] 
            print(y_pro_non_phishing*100)
            print("it has ",y_pro_non_phishing*100, " chance of being non malicious url")
            analysis_result="it is a legitimate url"
            chance=y_pro_non_phishing*100 
            print("it is a legitimate url")
         else:
               y_pro_phishing = rand.predict_proba(x)[0,0]
               analysis_result="it is a malicious url"
               chance=y_pro_phishing*100
         dictt={"results":analysis_result,
                "prediction":y_predc,
                "score":chance,
                 "url":url,
                 "accuracy":accuracy   
                   }
         return dictt  
      
     
   
   
   
   #  if modelname=="Randoms":
   #          obj = FeatureExtraction(url)
   #          x = np.array(obj.getFeaturesList()).reshape(1,30)
   #          file = open("pickle/randomforest.pkl","rb")
   #          rando = pickle.load(file)
   #          file.close() 
   #          y_pred =rando.predict(x)[0]
   #          print(y_pred)
   #          # y_pro_malicious = gbc.predict_proba(x)[0,0]
   #          y_pro_non_malicious = rando.predict_proba(x)[0,0]
   #          y_pro_malicious=rando.predict_proba(x)[0,1]
   #          if y_pred==1:
   #             y_pro_non_malicious=rando.predict_proba(x)[0,1]
   #             print("it has ",y_pro_malicious*100,"chance of being non malicious url")
   #             print("it is a legitimate url")
   #          else:
   #             a= (1-y_pro_non_malicious)*100
   #             print("it has ",a,"chance of being malicious url")
   #             print("it is a malicious url")
    
    
    if modelname=="Knn":
            obj = FeatureExtraction(url)
            x = np.array(obj.getFeaturesList()).reshape(1,30)
            file = open("pickle/knn.pkl","rb")
            Knnn = pickle.load(file)
            file.close() 
            y_pred =Knnn.predict(x)[0]
            print(y_pred)
            accuracy="0.956"
            # y_pro_malicious = gbc.predict_proba(x)[0,0]
            y_pro_non_malicious = Knnn.predict_proba(x)[0,0]
            y_pro_malicious=Knnn.predict_proba(x)[0,1]
            if y_pred==1:
               print("it has ",y_pro_malicious*100,"chance of being non malicious url")
               analysis_result="it is a legitimate url"
               chance=y_pro_malicious*100 
                                          
            else:
               analysis_result="it is a malicious url"
               chance=y_pro_non_malicious*100
               print("it is a malicious url")
            
            dictt={"results":analysis_result,
                "prediction":y_pred,
                "score":chance,
                 "url":url,
                 "accuracy":accuracy   
                   }
            return dictt  
            
            
            
            
            
            
               
               
    if modelname=="Svm":
            obj = FeatureExtraction(url)
            accuracy="0.964"
            x = np.array(obj.getFeaturesList()).reshape(1,30)
            file = open("pickle/svm2.pkl","rb")
            sv = pickle.load(file)
            file.close() 
            y_pred =sv.predict(x)[0]
            print(y_pred)
            if y_pred==1:
                y_pro_non_phishing = sv.predict_proba(x)[0,1] 
                analysis_result="it is a legitimate url"
                chance=y_pro_non_phishing*100 
              
                print(y_pro_non_phishing*100)
                print("legitimate url")
            else:
               y_pro_phishing = sv.predict_proba(x)[0,0]
               analysis_result="it is a malicious url"
               chance=y_pro_phishing*100
               print("malicious url")
            dictt={"results":analysis_result,
                "prediction":y_pred,
                "score":chance,
                 "url":url,
                 "accuracy":accuracy   
                   }
            return dictt  
               
    if modelname=="Naive":
            obj = FeatureExtraction(url)
            accuracy="0.605"
            x = np.array(obj.getFeaturesList()).reshape(1,30)
            file = open("pickle/naivebayes.pkl","rb")
            naives = pickle.load(file)
            file.close() 
            y_pred =naives.predict(x)[0]
            if y_pred==1:
                y_pro_non_phishing = naives.predict_proba(x)[0,1] 
                analysis_result="it is a legitimate url"
                chance=y_pro_non_phishing*100 
                print("legitimate url")
            else:
               y_pro_phishing = naives.predict_proba(x)[0,0]
               analysis_result="it is a malicious url"
               chance=y_pro_phishing*100
               print("malicious url")
               
            dictt={"results":analysis_result,
                "prediction":y_pred,
                "score":chance,
                 "url":url,
                 "accuracy":accuracy   
                   }
            return dictt  
               
         
    if modelname=="logisticregression":     
         accuracy="0.934"  
         file = open("pickle/logreg.pkl","rb")
         logss = pickle.load(file)
         file.close() 
         obj = FeatureExtraction(url)
         x = np.array(obj.getFeaturesList()).reshape(1,30) 
         y_predc =logss.predict(x)[0]
         print(y_predc) 
         if y_predc==1:
            y_pro_non_phishing = logss.predict_proba(x)[0,1] 
            analysis_result="it is a legitimate url"
            chance=y_pro_non_phishing*100 
            print("it is a legitimate url")
         else:
               y_pro_phishing = logss.predict_proba(x)[0,0]
               analysis_result="it is a malicious url"
               chance=y_pro_phishing*100
               print("malicious url")
               
         dictt={"results":analysis_result,
                "prediction":y_predc,
                "score":chance,
                 "url":url,
                 "accuracy":accuracy   
                   }
         return dictt  
  
               
           
           
            

       
     
   

