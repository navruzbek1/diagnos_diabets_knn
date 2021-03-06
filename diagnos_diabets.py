# -*- coding: utf-8 -*-
"""diagnos_diabets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13JeXvHPyRHehBiL7B1c1Qk-l1CAKJ_w_

# Maqsad diagnostik o’lchovlar asosida bemorda diabet bor-yo’qligini taxmin qilishdir




---

                                                                                                  created by Navruzbek_Abduganiyev
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
import sklearn
import matplotlib.pyplot as plt
# %matplotlib inline

df = pd.read_csv("/content/diabetes.csv")
df.head()

"""**Ustunlar:**
*  Pregnancies: homilador bo’lish soni
*  Glucose: glyukozaga test natijasi
*  BloodPressure: diastolik qon bosimi (mm Hg)
*  SkinThickness: Triceps teri burmasining qalinligi (mm)
*  Insulin: 2 soatlik sarum insulini (mu U/ml)
*  BMI: Tana massasi indeksi (vazn kg / (m bo’yi) ^ 2)
*  DiabetesPedigreeFunction: diabetning naslchilik funktsiyasi
*  Age: Yosh (yil)
*  Outcome: Class (0 – diabet yo’q, 1 – diabet)

**Tarkib:**

Dataset ichidagi barcha bemorlar kamida 21 yoshli ayollar
"""

df.shape

df.info()

df.isnull().sum()

df['Outcome'].value_counts()  # balans juda yomon holatda,farq juda katta

corr_matrix=df.corr().abs()
corr_matrix.style.background_gradient(cmap="coolwarm")

df.corrwith(df["Outcome"]).abs().sort_values(ascending=False)

####################################

df.columns

for i in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction']:
  print(f"df['{i}']={len(df[df[i]==0])}")  # df ustunlaridagi jami nollar soni

# yoshlar bo'yicha gruppalaymanda,0 qiymatlarni np.nan qiymatga aylantirib chiqaman
df[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction']]=df[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction']].replace({0:np.nan})

# ikki ustundan tashqari hamma ustunlardagi 0 qiymatlar np.nan qiymatga aylantirildi

for i in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin','BMI', 'DiabetesPedigreeFunction']:
  print(f"df['{i}']={len(df[df[i]==0])}")  # df ustunlaridagi jami nollar soni

df.describe()

# yoshlar ko'lami bo'yicha ham chegaralab bitta df ga ustun po'shamiz
bins=[20,24.5,29.5,41.5,81.5]  # bunday o'nlik qiymat berishimga sabab,yoshni saralab olishda komp notogri ishlamaydi
df["age_fill"]=pd.cut(df["Age"],bins=bins,labels=[1,2,3,4])
df.head()

pd.cut(df.Age,bins).value_counts()  # oraliqqa kiruvchi yoshlarning sonini ko'rishimiz mumkin "DEYARLI BALANS YAXSHI"

df["age_fill"].value_counts()

from numpy.lib.function_base import median
df[df["age_fill"]==1]=df[df["age_fill"]==1].fillna(method="ffill")
df[df["age_fill"]==2]=df[df["age_fill"]==2].fillna(method="ffill")
df[df["age_fill"]==3]=df[df["age_fill"]==3].fillna(method="ffill")
df[df["age_fill"]==4]=df[df["age_fill"]==4].fillna(method="ffill")

df["Insulin"]=df["Insulin"].fillna(method="bfill")
df.isnull().sum()

df.isnull().sum()   # bitta kichik yutuqqa erishdik,yoshlar ko'lami bo'yicha nan qiymtalarni to'ldirib chiqdik

df.corrwith(df["Outcome"]).sort_values(ascending=False) #corr ni biroz bolsa ham ko'taribiz::)

"""# **ML ga tayyorlaymiz**"""

# ML ga tayyorlanamiz
df.drop("age_fill",axis=1,inplace=True)
X = df.drop("Outcome",axis=1).values
y = df["Outcome"]

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

X = scaler.fit_transform(X)

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=21,train_size=0.8)

"""# **ML**"""

# modelni quramiz
from sklearn.neighbors import KNeighborsClassifier
knn_model = KNeighborsClassifier(n_neighbors=5)

knn_model.fit(X_train,y_train)

y_predict = knn_model.predict(X_test)

"""# **Baholash**

**Jaccard index**
"""

from sklearn.metrics import jaccard_score
jaccard_score(y_predict,y_test)

"""**confusion matrix**"""

from sklearn.metrics import confusion_matrix
confu_matr = confusion_matrix(y_predict,y_test)
confu_matr  #aslini olganda juda yomon,:))

plt.figure(figsize=(8,6))
sns.heatmap(confu_matr,annot=True)
plt.show()

# o'lchashning boshqa usullarini ham ko'ramiz

from sklearn.metrics import precision_score,recall_score,accuracy_score,f1_score
precision = precision_score(y_test, y_predict)
recall = recall_score(y_test, y_predict)
f1 = f1_score(y_test, y_predict)
accuracy = accuracy_score(y_test, y_predict)
print(f"precision={precision} \nrecall={recall} \nf1={f1} \naccuracy={accuracy}")

from sklearn.metrics import classification_report
print(classification_report(y_predict,y_test))

"""**Cross-validation yordamida ham tekshirishimiz mumkin**"""

from sklearn.model_selection import cross_val_predict
predict = cross_val_predict(estimator=knn_model,X=X,y=y,cv=5)

print(f"Classification_report: {classification_report(predict,y)}")

from sklearn.model_selection import cross_val_predict
predict_ = cross_val_predict(estimator=knn_model,X=X_test,y=y_test,cv=5)

print(f"Classification_report: {classification_report(predict_,y_test)}")

"""# Eng yaxshi k ni topish
for yordamida
"""

from matplotlib.markers import MarkerStyle
f=[]
for k in range(1,25):
  knn = KNeighborsClassifier(n_neighbors=k)
  knn.fit(X_train,y_train)
  predict = knn.predict(X_test)
  f.append(f1_score(predict,y_test))
plt.figure(figsize=(12,8))
plt.xticks(range(1,25))
plt.plot(range(1,25),f,marker="o",color="r")
plt.grid()
plt.show()             
# grafikning y ustunidagi max qiymat biz uchun eng optimal qiymat boladi.Demak n_neighbors=5 eng yaxshi javob ekan

"""## **Grid Search yordamida ham foydali ma'luotlarni olishimiz mumkin**"""

#  knn = KNeighborsClassifier(n_neighbors=k) ga teng edi
knn_ = KNeighborsClassifier(n_neighbors=5)
from sklearn.model_selection import GridSearchCV

param_grid = {"n_neighbors":np.arange(1,25)}

knn_gscv = GridSearchCV(knn_,param_grid,cv=5)

knn_gscv.fit(X,y)

knn_gscv.cv_results_  #bu usulda bizga kerak bolgan eng yaxshi ustunlarni ko'rishimiz mumkin

knn_gscv.cv_results_['rank_test_score']

knn_gscv.best_params_  
#eng yaxshi ko'rsatgichni olishimiz mumkin n_neghbors uchun:bunda biz

knn_gscv.best_score_  # eng yaxshi ko'rsatgich

plt.figure(figsize=(10,6))
plt.plot(param_grid['n_neighbors'], knn_gscv.cv_results_['rank_test_score'])
plt.xticks(param_grid['n_neighbors'])
plt.xlabel("k")
plt.ylabel("Xatolik reytingi")
plt.grid()
plt.show()

#n_neighbors=15 da eng kam xtolikka olib kelyapti,bu yaxshi

"""

---
                                                    created by Navruzbek_Anduganiyev
"""