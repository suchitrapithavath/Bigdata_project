from random import randint
import json
import pandas as pd
import numpy as np
from pprint import pprint
import pandas as pd
import numpy as np
#correlated files used for regression
files = ['correlated1.csv','correlated2.csv','correlated3.csv','correlated4.csv','correlated5.csv','correlated6.csv','correlated7.csv','correlated8.csv','correlated9.csv','correlated10.csv','correlated11.csv','correlated12.csv','correlated13.csv','correlated14.csv','correlated15.csv']
my_matrix = []# for storing regression coefficients
for file in files:
    coeff = []#This is the coefficient matrix
    dataset = pd.read_csv(file)#loading the file
    my_list =list(dataset)
    X = dataset[[my_list[1],my_list[2] ]]# independent variables
    y = dataset[my_list[0]]# attribute that should be predicted 
    coeff.append(my_list[0])
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)#splitting the data into training set and testing set
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)#fitting the regression model
    coeff.append(regressor.intercept_)# tetha not
    coeff.append(regressor.coef_.flat[0])#tetha1
    coeff.append(regressor.coef_.flat[1])#tetha2
    my_matrix.append(coeff)

    
    y_pred = regressor.predict(X_test)
    df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

with open('lessAttribute.json') as f:
	data = json.load(f)
with open('fullAttribute.json') as full:
	full_attr = json.load(full)




def correlated(missing_data,missing_list):
	regression_values=[]# to store regression values
	my_dict={}
	out = open("full_data1.txt", 'a')
	with open("correlation.txt", "r") as filestream:
		for m_data in missing_data:
			for line in filestream:
				currentline = line.split(",")#splittng the correlation attribute line
				third =currentline[2].split("\n")
				m_data=m_data.replace('"', '')
				missing_dict=(json.loads(missing_list))
				if(json.dumps(m_data) == json.dumps(currentline[0])):#comparing missing attribute with correlated attribute
                    			if(currentline[1] in json.dumps(missing_dict.keys()) and third[0] in json.dumps(missing_dict.keys())):	
                                		for j in range(len(my_matrix)):
							if(m_data == my_matrix[j][0]):
                                                                # y =theta+theta1*x1+thetha2*x2
								reg_eq=float(my_matrix[j][1])+float(my_matrix[j][2])*float(json.dumps(missing_dict[currentline[1]]))+float(my_matrix[j][3])*float(json.dumps(missing_dict[third[0]]))
                                                		my_dict=(json.loads(missing_list))
                                                		my_dict.update({m_data:reg_eq})#after calculating the regression value storing it in json file
					else:				
						rand_value=full_attr[randint(0, 9)]#randomly selecting the json object from full atrribute list to get the correlated value
						value1=str(rand_value[currentline[1]])
						value2=str(rand_value[third[0]])
						for j in range(len(my_matrix)):
                                                        if(m_data == my_matrix[j][0]):
                                                                reg_eq=float(my_matrix[j][1])+float(my_matrix[j][2])*float(value1)+float(my_matrix[j][3])*float(value2)
                                                                my_dict=(json.loads(missing_list))
                                                                my_dict.update({m_data:reg_eq})
		dict_list =json.dumps(my_dict)#converting dict in to json
        	out.write(dict_list)#writing the missing attribute in mssing dataset
        	out.close		
			
list=[];
#list of all 18 attributes
full_attrlist =["crime_index","traffic_time_index","cpi_and_rent_index","purchasing_power_incl_rent_index","restaurant_price_index","property_price_to_income_ratio","climate_index","safety_index","traffic_co2_index","cpi_index","traffic_inefficiency_index","quality_of_life_index","rent_index","health_care_index","traffic_index","groceries_index","name","pollution_index"]
for item in data:# iterating missing dataset
	for (key,value) in item.items():#splitting in to key and value
		if (json.dumps(key) not in full_attrlist):
			list.append(json.dumps(key))# appending missing keys in the list
			correlated(list,json.dumps(item))
                        del list[:]# emptying the list



