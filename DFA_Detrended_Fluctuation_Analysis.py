import numpy as np
import matplotlib.pyplot as plt
import Choose_File
import os

def file_reading (text_file_series, fileName):

    file_manipulator = open(fileName, 'r')
    for i in file_manipulator:
        i = i.rstrip()
        text_file_series.append(float(i))
    file_manipulator.close()

    return text_file_series

def file_name (fileName):
   fileName = os.path.basename(fileName)
   fileName = fileName.replace (".txt","") 
   return fileName

def path_name (pathName):
    fileName = os.path.basename(pathName) 
    pathName = pathName.replace (fileName,"") 
    return pathName


def average_value_of_series(text_file_series, N) :
    
    sum_Xi = 0
    for i in range (N) :
        sum_Xi = text_file_series[i] + sum_Xi

    X = (1/N) * sum_Xi
    return X

def accumulated_series (text_file_series, N, X):

    sum_Yk = 0
    Yk = []
    for i in range (N) :
        sum_Yk = (text_file_series[i] - X) + sum_Yk
        Yk.append(sum_Yk)
    return Yk

def plot_graphic (x, y, title, fileName, pathName, x_name, y_name):
    plt.title(title)
    plt.plot(x, y, color='blue')
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.savefig(pathName + fileName + "_"+ title + ".png")

    plt.show()


def regressao_linear_simples_naosobreposto(text_file_series, N_series, yk_for_adjustment, n_pontos_ajustados, fileName, pathName):
    file_manipulator = open(pathName + fileName + '_F(n)_nãosobreposto'+'.txt', 'w')
    n_limite = n_pontos_ajustados
    y_original_serie = text_file_series
    Fn_nao_sobreposto_plot = []
    n_limite_plot = []
    
    while ( n_limite <= (int((len(N_series))/n_pontos_ajustados))):
        i = 0
        n = n_limite
        yk_adjustment = []
        yk_real = []
           
        Qb = (len(N_series)) / n 
        Qb = (int(Qb))

        for t in range (Qb): 
            x = np.array(N_series[i:n]) 
            yk = np.array(yk_for_adjustment[i:n]) 
            p1 = np.polyfit(x,yk,1) 
            yfit = p1[0] * x + p1[1] 
            yk_adjustment.append(yfit) 
            yresid = yk - yfit 
            SQresid = sum(pow(yresid,2)) 
            SQtotal = len(yk) * np.var(yk) 
            R2 = 1 - SQresid/SQtotal 
            i = n
            n = n + n_pontos_ajustados

        yk_temp = [] 
        for l in range (len(yk_adjustment)):
            yk_temp.extend(yk_adjustment[l])

        y_sum_for_Fn = 0

        for d in range (len(yk_temp)):
            
            y_sum_for_Fn = y_sum_for_Fn + ((yk_for_adjustment[d] - yk_temp[d]) ** 2) 
            
        Fn_nao_sobreposto = ((y_sum_for_Fn / (len(N_series))) ** (1/2))  
        Fn_nao_sobreposto_plot.append (Fn_nao_sobreposto)
        n_limite_plot.append (n_limite)
        Fn_file = "F(" + (str(n_limite))+") = " + (str(Fn_nao_sobreposto)) + "\n"
        file_manipulator.writelines(Fn_file)
        n_limite = n_limite + 1

    file_manipulator.close()
    plot_graphic (n_limite_plot, Fn_nao_sobreposto_plot, "F(n)_nãosobreposto",fileName, pathName, "n", "F(n)") 

def regressao_linear_simples_sobreposto(text_file_series, N_series, yk_for_adjustment, n_pontos_ajustados, fileName, pathName):
    file_manipulator = open(pathName + fileName + '_F(n)_sobreposto'+'.txt', 'w')
    n_limite = n_pontos_ajustados
    y_original_serie = text_file_series
    Fn_sobreposto_plot = []
    n_limite_plot = []
    
    while ( n_limite <= (int((len(N_series))/n_pontos_ajustados))): 
        i = 0
        n = n_limite
        yk_adjustment = []
        yk_real = []
        yk_for_sum = []

        Qb = (len(N_series)) - n 
        Qb = (int(Qb))

        for t in range (Qb): 
            x = np.array(N_series[i:(n+1)]) 
            yk = np.array(yk_for_adjustment[i:(n+1)]) 
            p1 = np.polyfit(x,yk,1) 
            yfit = p1[0] * x + p1[1] 
            yk_adjustment.append(yfit) 
            yk_real.extend(yk) 
            yresid = yk - yfit 
            SQresid = sum(pow(yresid,2)) 
            SQtotal = len(yk) * np.var(yk) 
            i = i+1
            n = n + 1
        yk_temp = [] 
        for l in range (len(yk_adjustment)):
            yk_temp.extend(yk_adjustment[l])

        y_sum_for_Fn = 0
        
        for d in range (len(yk_temp)):
            y_sum_for_Fn = y_sum_for_Fn + ((yk_real[d] - yk_temp[d]) ** 2) 

        Fn_sobreposto = ((y_sum_for_Fn / ((n_limite + 1) * (len(N_series) - n_limite))) ** (1/2))  
        Fn_sobreposto_plot.append (Fn_sobreposto)
        n_limite_plot.append (n_limite)
        Fn_file = "F(" + (str(n_limite))+") = " + (str(Fn_sobreposto)) + "\n"
        file_manipulator.writelines(Fn_file)
        
        n_limite = n_limite + 1
    file_manipulator.close()
    plot_graphic (n_limite_plot, Fn_sobreposto_plot, "F(n)_sobreposto",fileName, pathName, "n", "F(n)") 
    
def main():

    fileName = Choose_File.main()
    pathName = path_name (fileName)
    text_file_series = []
    text_file_series = file_reading (text_file_series, fileName)
    fileName = file_name (fileName)
    N = len(text_file_series) 
    N_series = []
    
    for i in range (N): 
        N_series.append(1+i)

    plot_graphic (N_series, text_file_series, "Série original", fileName, pathName, "x", "y")    
    X = average_value_of_series(text_file_series, N)
    Yk = accumulated_series (text_file_series, N, X) 
    regressao_linear_simples_naosobreposto(text_file_series, N_series, Yk, 4, fileName, pathName)
    regressao_linear_simples_sobreposto(text_file_series, N_series, Yk, 4, fileName, pathName)
 
if __name__ == '__main__': 
    main()
