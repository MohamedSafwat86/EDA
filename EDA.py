import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import validators
import opendatasets as od
import os.path 
from IPython.display import display
import seaborn as sns
from warnings import filterwarnings


def Get_Database_Path():
    print("Please,Enter Path or URL of your database")
    while True:
        database_path=input("Please,Enter Path of your database -->")
        if os.path.exists(database_path)!= True:
            print("Path is not valid...")
            continue
        if (database_path.split('.')[-1]).upper()=="CSV" or (database_path.split('.')[-1]).upper()=="XLSX" or (database_path.split('.')[-1]).upper()=="SQL":
            break
        else:
            continue
    return database_path    
        
def Database_Summary(df):
    df=pd.DataFrame(df)
    print("The database has {0} Columns (Features)".format(df.shape[1]))
    print("The database has {0} Rows".format(df.shape[0]))
    print("The number of duplicated Rows:{0} ".format(sum(df.duplicated(keep=False))))
    print("The number of duplicated Rows(%):{0}% ".format(((sum(df.duplicated(keep=False)))/df.shape[0])*100))
    nalst=[]
    for col in df.columns:
        nalst.append(df[col].isna().sum())
    print("The number of Missing Cells:{0} ".format(sum(nalst)))
    print("The number of Missing Cells(%):{0}% ".format((sum(nalst)/(df.shape[0]*df.shape[1]))*100))
    print("\nColumns data types:")
    d=dict(df.dtypes)
    lst1=d.keys()
    lst2=d.values()
    df_types=pd.DataFrame({"Columns_Name":lst1,"Data_Types":lst2})
    df_types["Is_Numerical"]=df_types["Data_Types"].apply(lambda x:True if np.issubdtype(x, np.number) else False)
    display(df_types)
    
def Features_pre_processing(df):
    df=pd.DataFrame(df)
    index=1;
    print("*"*10,"Feature pre processing","*"*10,sep="")
    for column_name in df.columns:
        print("*"*20)
        print("{0}-{1}:".format(index,column_name))
        is_numerical=np.issubdtype(df[column_name].dtype, np.number)
        if is_numerical:
            print("DataType:{0} (Numerical)".format(df[column_name].dtype))
        else: 
            print("DataType:{0} (Categrical)".format(df[column_name].dtype))
        
        missing=df[column_name].isna().sum()
        print("Missing:{0}".format(missing))
        if is_numerical:
            column_max=df[column_name].max()
            print("The max value: {0}".format(column_max))
            column_min=df[column_name].min()
            print("The min value: {0}".format(column_min))
            column_std=df[column_name].std()
            print("The standard deviation: {0}".format(column_std))
            column_mean=df[column_name].mean()
            print("the mean: {0}".format(column_mean))
            column_median=df[column_name].median()
            print("The median: {0}".format(column_median))
            plt.hist(df[column_name])
            plt.xlabel(column_name)
            plt.ylabel("Frequency")
            plt.title(column_name+" hisrogram")
            plt.show()
            if missing!=0:
                print("The {0} column has {1} missing value,Replace them with (select from below): ".format(column_name,missing))
                print("1-The Mean value:","2-The Median value","3-Replace with 0",sep="\n")
                while True:
                    try:
                        sel=int(input("Enter Your select (1~3):"))
                    except:
                        print("Invalid input,Please try again...")
                    else:
                        if sel in [1,2,3]:
                            break
                if sel==1:
                   df[column_name]= df[column_name].fillna(column_mean)
                elif sel==2:
                   df[column_name]= df[column_name].fillna(column_median)
                elif sel==3:
                    df[column_name]=df[column_name].fillna(0)
                print("**Done**\n\n")
            print("*****Scaling Numerical Features*******")   
            print("Please Select the scaling method for applying to the folumn values (select from below): ".format(column_name,missing))
            print("1-Min-Max Scaling:","2-Normalization","3-Standardization","4-No Scaling needed",sep="\n")
            while True:
                try:
                    sel=int(input("Enter Your select (1~4):"))
                except:
                    print("Invalid input,Please try again...")
                else:
                    if sel in [1,2,3,4]:
                        break
            if sel==1:
                df[column_name]= df[column_name].apply(lambda x:((x-column_min)/(column_max-column_min)))
            elif sel==2:
                df[column_name]= df[column_name].apply(lambda x:((x-column_mean)/(column_max-column_min)))
            elif sel==3:
                df[column_name]= df[column_name].apply(lambda x:((x-column_mean)/(column_std)))
                
            
        else:
            print("The Count of Caterical values:")
            count_dic=dict(df[column_name].value_counts())
            if len(count_dic)<10:
                for value,count in count_dic.items():
                    print("{0} --->{1}".format(value,count))
            else:
                count_list=list(count_dic.items())
                for i in range(0,10):
                    print("{0} --->{1}".format((count_list[i])[0],(count_list[i])[1]))
                other_sum=0
                for i in range(10,len(count_list)):
                    other_sum+=(count_list[i])[1]
                print("Others --->{0}".format(other_sum))
                count_list=count_list[:10]
                count_list.append(("Others",other_sum))
                count_dic=dict(count_list)
            df_bar=pd.DataFrame(count_dic,index=["0"])
            df_bar=df_bar.T
            plt.barh(df_bar.T.columns,df_bar["0"])
            plt.title(column_name+" Bar Graph")
            plt.ylabel(column_name)
            plt.show()
            if missing!=0:
                print("The {0} column has {1} missing value,Will be replaced with most occurring value ".format(column_name,missing))
                d=pd.DataFrame(df[column_name].value_counts())
                df[column_name]= df[column_name].fillna((d.index)[0])
            
                    
        print("If you want to drop this column (feature) from database Press (Y/N)")
        j=input("Enter your choice:")
        if j.lower()=='y':
            df.drop([column_name],axis=1,inplace=True)
            continue            
        index+=1
    display(df.head(5))
    
        
def Visualization(df):
    df=pd.DataFrame(df)
    print("*"*10,"Visualization","*"*10,sep="")
    print("*"*10,"Take some time to finish Please Wait and Scroll down","*"*10,sep="")
    for column_name in df.columns:
        is_numerical=np.issubdtype(df[column_name].dtype, np.number)
        sns.set_style('darkgrid')
        if is_numerical:
            plt.figure()
            sns.displot(df[column_name], kde = False, color ='red', bins = 30)
        else:
            plt.figure()
            sns.countplot(x =column_name, data = df)
       
    



print("*************Welcome Automated Exploratory Data Analysis***************")
database_path=Get_Database_Path()
if (database_path.split('.')[-1]).upper()=="CSV":
    while True:
        try:
            df=pd.read_csv(database_path)
        except:
            print("Error...")
        else:
            break
elif (database_path.split('.')[-1]).upper()=="XLSX":
    while True:
        try:
            df=pd.read_excel(database_path)
        except:
            print("Error...")
        else:
            break
else:
    while True:
        try:
            df=pd.read_sql(database_path)
        except:
            print("Error...")
        else:
            break
    
    
print("Succefully import database...")
print("Samples of first 5 rows shown below:")
display(df.head(5))
Database_Summary(df)
Features_pre_processing(df)
while True:
    print("Enter Name to save the database and wait the visualization")
    name=input("Enter database name:")
    if ((name.split('.')[-1]).upper()=="CSV" or (name.split('.')[-1]).upper()=="XLSX" or (name.split('.')[-1]).upper()=="SQL"):
        try:
            if (name.split('.')[-1]).upper()=="CSV":
                df.to_csv(name)
            elif (name.split('.')[-1]).upper()=="XLSX":
                df.to_excel(name)
            else:
                df.to_sql(name)
        except:
            print("Invalid file name")
        else:
            break
Visualization(df)

print("****Done****")    
        

    