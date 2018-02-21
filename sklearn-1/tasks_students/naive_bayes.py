import numpy as np
from scipy.stats import norm
from sklearn.base import BaseEstimator




class NaiveBayesNominal:
    
    def __init__(self):
        self.classes_ = None
        self.model = dict()
        self.y_prior = []
        self.class_prob = {}
        self.results_dict = []

    def partial_prob(self, X, y, a, class_dict):
        unique_dict = {}
        
        for i in range(len(y)):
           count = 0
           p=X[i][a]
           q=y[i]
           for j in range(len(y)):
              if(X[j][a]==p and y[j]==q):
                 count+=1
              unique_dict.update({(p,q):count/class_dict[q]})
            
        return unique_dict


    def fit(self, X, y):
        class_dict = {}

        for i in range(len(y)):
            if(y[i] in class_dict.keys()):
              class_dict[(y[i])]+=1
            else:
              class_dict.update({y[i]:1})
        for k,v in class_dict.items():
            self.class_prob.update({k:(v/len(y))})
        
        for i in range(len(X[0])):
            self.results_dict.append(self.partial_prob(X,y,i,class_dict))
              
        print(self.results_dict)


    def predict_proba(self,X):
        prob_dict={}
        for i in range(len(X)):
            for k,v in self.class_prob.items():
                product=v
                print(product)
                for j in range(len(X[i])):
                    print(X[i][j],k)
                    if((X[i][j],k) in self.results_dict[j]):
                        product=product*self.results_dict[j][(X[i][j],k)] 
                    else:
                        product=0
                    #print(product)
                    
                if(i not in prob_dict.keys()):
                    prob_dict.update({i:[product]})
                else:
                    prob_dict[i].append(product)
        #print(prob_dict)        
        return prob_dict

    def predict(self,X):
        result_list=[]
        for k,v in self.predict_proba(X).items():
            result_list.append(np.argmax(v))
        
        return result_list


class NaiveBayesGaussian:
    
    def __init__(self):
        self.data_dict = {}
        self.measures_dict = {}
        self.class_prob = {}

    def density(self,x,m,d):
        density = 1/(np.sqrt(2*np.pi)*d)*np.exp((-np.power((x-m),2))/(2*np.power(d,2)))
        return density

    def fit(self, X, y):
        class_dict = {}
        
        for i in range(len(y)):
            if(y[i] in class_dict.keys()):
              class_dict[(y[i])]+=1
            else:
              class_dict.update({y[i]:1})
        for k,v in class_dict.items():
            self.class_prob.update({k:(v/len(y))})
        
        for i in range(len(X)):
            for j in range(len(X[i])):
                if((j,y[i]) not in self.data_dict):
                    self.data_dict.update({(j,y[i]):[X[i][j]]})
                else:
                    self.data_dict[(j,y[i])].append(X[i][j])
        
        for k,v in self.data_dict.items():
            self.measures_dict.update({k:[np.mean(v),np.std(v)]})
        print(self.measures_dict)

    def predict_proba(self, X):
        prob_dict = {}
        for i in range(len(X)):
            for k,v in self.class_prob.items():
                product=v
                for j in range(len(X[i])):
                    if((j,k) in self.data_dict):
                        product=product*self.density(X[i][j],self.measures_dict[(j,k)][0],self.measures_dict[(j,k)][1]) 
                    else:
                        product=1*np.power(10,-21)
                if(i not in prob_dict.keys()):
                    prob_dict.update({i:[product]})
                else:
                    prob_dict[i].append(product)            
        return prob_dict

    def predict(self, X):
        result_list=[]
        for k,v in self.predict_proba(X).items():
            result_list.append(np.argmax(v))
        
        return result_list
    
class NaiveBayesBoth():
    
    def __init__(self):
        self.features_type_vector = []
    
    def density(self,x,m,d):
        density = 1/(np.sqrt(2*np.pi)*d)*np.exp((-np.power((x-m),2))/(2*np.power(d,2)))
        return density
    
    def partial_prob(self, X, y, a, class_dict):
        unique_dict = {}
        
        for i in range(len(y)):
           count = 0
           p=X[i][a]
           q=y[i]
           for j in range(len(y)):
              if(X[j][a]==p and y[j]==q):
                 count+=1
              unique_dict.update({(p,q):count/class_dict[q]})
            
        return unique_dict
    
    def fit(self,X,y):
        class_dict = {}

        for i in range(len(y)):
            if(y[i] in class_dict.keys()):
              class_dict[(y[i])]+=1
            else:
              class_dict.update({y[i]:1})
        for k,v in class_dict.items():
            self.class_prob.update({k:(v/len(y))})
        
        for i in range(len(X)):
            for j in range(len(X[i])):
                if(self.features_type_vector[j]==True):
                    if((j,y[i]) not in self.data_dict):
                        self.data_dict.update({(j,y[i]):[X[i][j]]})
                    else:
                        self.data_dict[(j,y[i])].append(X[i][j])
        
        for i in range(len(X[0])):
            if(self.features_type_vector[i]==False):
                self.results_dict.append(self.partial_prob(X,y,i,class_dict))
        
        
        for k,v in self.data_dict.items():
            self.measures_dict.update({k:[np.mean(v),np.std(v)]})
            
    def predict_proba(self,X):
        prob_dict = {}
        for i in range(len(X)):
            for k,v in self.class_prob.items():
                product=v
                for j in range(len(X[i])):
                    if((j,k) in self.data_dict):
                        if(self.features_type_vector[j]==True):
                            product=product*self.results_dict[j][(X[i][j],k)] 
                        else:
                            product=product*self.density(X[i][j],self.measures_dict[(j,k)][0],self.measures_dict[(j,k)][1]) 
                    else:
                        product=1*np.power(10,-21)
                if(i not in prob_dict.keys()):
                    prob_dict.update({i:[product]})
                else:
                    prob_dict[i].append(product)
        #print(prob_dict)            
        return prob_dict
        
        
    def predict(self, X):
        result_list=[]
        for k,v in self.predict_proba(X).items():
            result_list.append(np.argmax(v))
        
        return result_list
        

class NaiveBayesNumNom(BaseEstimator):
    def __init__(self, is_cat=None, m=0.0):
        raise NotImplementedError

    def fit(self, X, yy):
        raise NotImplementedError

    def predict_proba(self, X):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError