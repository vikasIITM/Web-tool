import streamlit as st
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge

from sklearn.model_selection import GridSearchCV
from sklearn import svm
import xgboost as xg
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
from prophet.plot import plot_plotly, plot_components_plotly
from prophet import Prophet
df=pd.read_csv('Daily.txt',index_col='DATE',parse_dates=True)
df=df.dropna()
#print('Shape of data',df.shape)
#df.head()
df = df.reset_index()
#df
X=np.array(df["Sunrise"]).reshape(-1,1)
y=np.array(df['AvgTemp']).reshape(-1,1)
scaler = MinMaxScaler()
scaler.fit(X,y)
model  = pickle.load(open("model.pkl",'rb'))
st.title("Web tool for perdiction of Non - Linear Dynamical Systems.")



df = df[['DATE', 'AvgTemp']]
df['AvgTemp_Lastday']=df['AvgTemp'].shift(+1)
df['AvgTemp_2Lastday']=df['AvgTemp'].shift(+2)
df['AvgTemp_3Lastday']=df['AvgTemp'].shift(+3)
df['AvgTemp_4Lastday']=df['AvgTemp'].shift(+4)
df['AvgTemp_5Lastday']=df['AvgTemp'].shift(+5)
df=df.dropna()  
from sklearn.linear_model import LinearRegression
lin_model=LinearRegression()
import numpy as np
x1,x2,x3,x4,y=df['AvgTemp_Lastday'],df['AvgTemp_2Lastday'],df['AvgTemp_3Lastday'],df['AvgTemp_4Lastday'],df['AvgTemp']
x1,x2,x3,x4,y=np.array(x1),np.array(x2),np.array(x3),np.array(x4),np.array(y)
x1,x2,x3,x4,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),x4.reshape(-1,1),y.reshape(-1,1)
final_x=np.concatenate((x1,x2,x3,x4),axis=1)
X_train,X_test,y_train,y_test=final_x[:-360],final_x[-360:],y[:-360],y[-360:]





genre = st.radio(
    "Select a  Model for Prediction",
    ('Sun-Average', 'Moving- Avg', 'Lasso-Reg','Ridge-Reg','Model- Comparasion'))

if genre == 'Sun-Average':
    df=pd.read_csv('Daily.txt',index_col='DATE',parse_dates=True)
    df=df.dropna()
    #print('Shape of data',df.shape)
    #df.head()
    df = df.reset_index()
    #df
    X=np.array(df["Sunrise"]).reshape(-1,1)
    y=np.array(df['AvgTemp']).reshape(-1,1)
    scaler = MinMaxScaler()
    scaler.fit(X,y)

    st.write('You selected comedy.')
    title = float(st.text_input('Enter a number between 0 & 1','0.0'))
    z=model.predict([[title]])
    lin_pred=scaler.inverse_transform(z)
    st.write('You Have entered a number : ', title)
    st.write("Prediction: ",lin_pred)
    X1=scaler.fit_transform(X)
    y1=scaler.fit_transform(y)
    from sklearn.model_selection import train_test_split
    X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.33, random_state=42)
    model.fit(X1_train,y1_train)
    z=model.predict(X1_test)
    lin_pred=scaler.inverse_transform(z)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    plt.rcParams["figure.figsize"] = (11,6)
    ax.plot(lin_pred,label='Linear_Regression_Predictions')
    ax.plot(scaler.inverse_transform(y1_test),label='Actual value')
    ax.legend(loc="upper left")
    st.pyplot(fig)

if genre == 'Moving- Avg':
    def moving_average():  
        lin_model.fit(X_train,y_train)
        lin_pred=lin_model.predict(X_test)
        import matplotlib.pyplot as plt
        
        from sklearn.metrics import mean_squared_error
        from math import sqrt
        rmse_lr=sqrt(mean_squared_error(lin_pred,y_test))
        arr = np.random.normal(1, 1, size=100)
        fig, ax = plt.subplots()
        plt.rcParams["figure.figsize"] = (11,6)
        ax.plot(lin_pred,label='Linear_Regression_Predictions')
        ax.plot(y_test,label='Actual Temp')
        ax.legend(loc="upper left")
        
        
        #ax.hist(arr, bins=20)
        st.pyplot(fig)
        st.write("RMSE",rmse_lr)
        st.write("R2_score",lin_model.score(X_test,y_test))
    moving_average()

if genre == 'Lasso-Reg':
    def Lasso_reg():  
    #from sklearn.linear_model import Lasso
        model_l1 = Lasso(alpha=1.0)
        model_l1.fit(X_train,y_train)
        model_l1.predict(X_train)
        st.write("Lasso Regression R2 Socre : ",model_l1.score(X_test,y_test))
    Lasso_reg()

if genre == 'Ridge-Reg':
    def reg_reg():  
    #from sklearn.linear_model import Ridge
        model_l2 = Ridge(alpha=1.0)
        model_l2.fit(X_train,y_train)
        model_l2.predict(X_train)
        st.write("Ridge Regression R2",model_l2.score(X_test,y_test))
    reg_reg()


if genre == 'Model- Comparasion':
    def model_comp():
  #import warnings
  #warnings.filterwarnings(action='ignore', category=FutureWarning) 
        from sklearn.model_selection import GridSearchCV
        from sklearn import svm
        import xgboost as xg
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.linear_model import LogisticRegression
        from sklearn.tree import DecisionTreeRegressor
        model_params = {
            'svm': {
                'model': svm.SVC(gamma='auto'),
                'params' : {
                    'C': [1,2,3],
                    'kernel': ['rbf','linear']
                }  
            },
            'random_forest': {
                'model': RandomForestRegressor(),
                'params' : {
                    'n_estimators': [10,20,30,40,60,80,100]
                }
            },
            'logistic_regression' : {
                'model': LogisticRegression(solver='liblinear',multi_class='auto'),
                'params': {
                    'C': [1,5,10]
                }
            },

            'Descission_Tree' : {
                'model': DecisionTreeRegressor(criterion='squared_error',splitter = 'random'),
                'params': {
                    'max_depth': [3,5,7],
                    'criterion': ['mse', 'mae'],
                    #'max_features': [0.25, 0.5, 1.0],
                    #'min_samples_split': [0.25, 0.5, 1.0],
                }
            },
            'xgboost_regression' : {
                'model': xg.XGBRegressor(objective ='reg:linear',seed=123),
                'params' : {
                    'n_estimators': [40,60,80,100],
                    'learning_rate': [0.05,0.10,0.20,0.30,0.40],
                    # 'max_depth': [3,5,8,10,12],
                    #'gamma': [0.0,0.1,0.2,0.3],
                    

                }
            }
            

        }

        scores = []

        for model_name, mp in model_params.items():
            clf =  GridSearchCV(mp['model'], mp['params'], cv=2, return_train_score=False)
            clf.fit(X_train,y_train)
            scores.append({
                'model': model_name,
                'best_score': clf.best_score_,
                'best_params': clf.best_params_
            })
            
        df = pd.DataFrame(scores,columns=['model','best_score','best_params'])
        return df
    
    st.dataframe(model_comp())
    
