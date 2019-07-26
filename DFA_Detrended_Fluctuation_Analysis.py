import numpy as np
import matplotlib.pyplot as plt
import Choose_File
import os

def file_reading (text_file_series, fileName): #lê arquivo

    file_manipulator = open(fileName, 'r')
    for i in file_manipulator:
        i = i.rstrip()
        text_file_series.append(float(i))
    file_manipulator.close()
    #print(text_file_series)

    return text_file_series

def file_name (fileName):
   fileName = os.path.basename(fileName) #Pega apenas o nome do arquivo, dado um diretório completo
   fileName = fileName.replace (".txt","") #Retira a extensão
   return fileName

def path_name (pathName):
    fileName = os.path.basename(pathName) #Pega apenas o nome do diretório
    pathName = pathName.replace (fileName,"") #Retira a extensão e o nome do arquivo
    return pathName


def average_value_of_series(text_file_series, N) : #valor médio dos elementos da série
    
    sum_Xi = 0
    for i in range (N) :
        sum_Xi = text_file_series[i] + sum_Xi
    #print (sum_Xi)

    X = (1/N) * sum_Xi
    #print (X)

    return X

def accumulated_series (text_file_series, N, X): #série acumulada

    sum_Yk = 0
    Yk = []
    for i in range (N) :
        sum_Yk = (text_file_series[i] - X) + sum_Yk
        Yk.append(sum_Yk)
    #print(sum_Yk)
    #print(Yk)

    return Yk

def plot_graphic (x, y, title, fileName, pathName):
    plt.title(title)
    plt.plot(x, y,'k:', color='blue')
    plt.xlabel("n")
    plt.ylabel("F(n)")
    plt.savefig(pathName + fileName + "_"+ title + ".png")

    plt.show()

############################################################# NÃO SOBREPOSTO ###############################################################

def regressao_linear_simples_naosobreposto(text_file_series, N_series, yk_for_adjustment, n_pontos_ajustados, fileName, pathName):
    file_manipulator = open(pathName + fileName + '_F(n)_nãosobreposto'+'.txt', 'w')
    n_limite = n_pontos_ajustados
    y_original_serie = text_file_series
    Fn_nao_sobreposto_plot = []
    n_limite_plot = []
    
    while ( n_limite <= (int((len(N_series))/n_pontos_ajustados))): #Faz o calculo dos vários F(n)
        i = 0
        #n = n_pontos_ajustados
        n = n_limite
        #plt.plot(N_series, yk_for_adjustment)
        yk_adjustment = []
        yk_real = []
           
        Qb = (len(N_series)) / n #Quantidade de blocos ajustados (não sobreposto)
        Qb = (int(Qb))

        for t in range (Qb): #ajuste não sobreposto
            x = np.array(N_series[i:n]) # vetor com os valores de x
            yk = np.array(yk_for_adjustment[i:n]) # vetor com os valores de yk (série acumulada)
            p1 = np.polyfit(x,yk,1) # fornece os valores do intercepto e a inclinação, 1 é o grau do polinômio
            yfit = p1[0] * x + p1[1] # calcula os valores preditos
            #print (yfit)
            yk_adjustment.append(yfit) ######pontos valor ajustado (aqui tem um bloco de n pontos)
            #yk_real.append(yk) ############ pontos valor yK sem ajuste (aqui tem um bloco de n pontos)
            yresid = yk - yfit # resíduo = valor real yk - valor ajustado yk (valor predito)
            SQresid = sum(pow(yresid,2)) # soma dos quadrados dos resíduos 
            SQtotal = len(yk) * np.var(yk) # número de elementos do vetor y vezes a variância de y
            R2 = 1 - SQresid/SQtotal # coeficiente de determinação
            #print(p1) # imprime o intercepto e a inclinação
            #print(R2) # imprime coeficiente de determinação
            #plt.plot(x_adjustment, y_adjustment)
            #plt.plot(x,y,'o')
            '''plt.plot(x,np.polyval(p1,x), color='red')
            plt.xlabel("x")
            plt.ylabel("y")'''
            i = n
            n = n + n_pontos_ajustados
        #plt.show()

        yk_temp = [] #todos os pontos (yk) ajustados
        for l in range (len(yk_adjustment)):
            yk_temp.extend(yk_adjustment[l])

        #print ("Pontos ajustados:", len(yk_temp))    

        ######## F(n) não sobreposto

        y_sum_for_Fn = 0

        for d in range (len(yk_temp)):
            
            y_sum_for_Fn = y_sum_for_Fn + ((yk_for_adjustment[d] - yk_temp[d]) ** 2) # somatorio (N vzs) do (valor Yk da série - ajustados de yk)^2
        #print("sum", y_sum_for_Fn)
            
        Fn_nao_sobreposto = ((y_sum_for_Fn / (len(N_series))) ** (1/2))  #Fn igual a raiz do somatório dividido por N (quantidade de pontos da série)
        #print ("Série não sobreposta: F(",n_limite,") = ", Fn_nao_sobreposto)
        Fn_nao_sobreposto_plot.append (Fn_nao_sobreposto)
        n_limite_plot.append (n_limite)
        Fn_file = "F(" + (str(n_limite))+") = " + (str(Fn_nao_sobreposto)) + "\n"
        file_manipulator.writelines(Fn_file)
        n_limite = n_limite + 1

    #file_manipulator.writelines(Fn_file)
    file_manipulator.close()
    plot_graphic (n_limite_plot, Fn_nao_sobreposto_plot, "F(n)_nãosobreposto",fileName, pathName) #Gráfico F(n)

############################################################# SOBREPOSTO ###############################################################

def regressao_linear_simples_sobreposto(text_file_series, N_series, yk_for_adjustment, n_pontos_ajustados, fileName, pathName):
    file_manipulator = open(pathName + fileName + '_F(n)_sobreposto'+'.txt', 'w')
    n_limite = n_pontos_ajustados
    y_original_serie = text_file_series
    Fn_sobreposto_plot = []
    n_limite_plot = []
    
    while ( n_limite <= (int((len(N_series))/n_pontos_ajustados))): #Faz o calculo dos vários F(n)
        i = 0
        #n = n_pontos_ajustados
        n = n_limite
        #plt.plot(N_series, yk_for_adjustment)
        yk_adjustment = []
        yk_real = []
        yk_for_sum = []

        Qb = (len(N_series)) - n #Quantidade de blocos ajustados (sobreposto)
        Qb = (int(Qb))

        for t in range (Qb): #ajuste sobreposto
            x = np.array(N_series[i:(n+1)]) # vetor com os valores de x
            yk = np.array(yk_for_adjustment[i:(n+1)]) # vetor com os valores de yk (série acumulada)

            #print ("yk: ", yk)
            p1 = np.polyfit(x,yk,1) # fornece os valores do intercepto e a inclinação, 1 é o grau do polinômio
            yfit = p1[0] * x + p1[1] # calcula os valores preditos
            #print (yfit)
            yk_adjustment.append(yfit) ######pontos valor ajustado (aqui tem um bloco de n pontos)
            yk_real.extend(yk) ############ pontos valor yK sem ajuste (aqui tem um bloco de n pontos)
            yresid = yk - yfit # resíduo = valor real yk - valor ajustado yk (valor predito)
            SQresid = sum(pow(yresid,2)) # soma dos quadrados dos resíduos 
            SQtotal = len(yk) * np.var(yk) # número de elementos do vetor y vezes a variância de y
            R2 = 1 - SQresid/SQtotal # coeficiente de determinação
            #print(p1) # imprime o intercepto e a inclinação
            #print(R2) # imprime coeficiente de determinação
            #plt.plot(x_adjustment, y_adjustment)
            #plt.plot(x,y,'o')
            '''plt.plot(x,np.polyval(p1,x), color='red')
            plt.xlabel("x")
            plt.ylabel("y")'''
            i = i+1
            n = n + 1
        #print ("yk: ", len(yk_real))    
        #plt.show()
        yk_temp = [] #todos os pontos (yk) ajustados
        for l in range (len(yk_adjustment)):
            yk_temp.extend(yk_adjustment[l])

        #print ("Pontos ajustados:", len(yk_temp))

        ### até aqui, perfeito.

        ######## F(n) sobreposto
        y_sum_for_Fn = 0
        
        for d in range (len(yk_temp)):
            y_sum_for_Fn = y_sum_for_Fn + ((yk_real[d] - yk_temp[d]) ** 2) # somatorio (N vzs) do (valor Yk da série - ajustados de yk)^2

        Fn_sobreposto = ((y_sum_for_Fn / ((n_limite + 1) * (len(N_series) - n_limite))) ** (1/2))  #Fn igual a raiz do somatório dividido por (n+1)*(N-n)
        #print ("Série sobreposta: F(",n_limite,") = ", Fn_sobreposto)
        Fn_sobreposto_plot.append (Fn_sobreposto)
        n_limite_plot.append (n_limite)
        Fn_file = "F(" + (str(n_limite))+") = " + (str(Fn_sobreposto)) + "\n"
        file_manipulator.writelines(Fn_file)
        
        n_limite = n_limite + 1
    file_manipulator.close()
    plot_graphic (n_limite_plot, Fn_sobreposto_plot, "F(n)_sobreposto",fileName, pathName) #Gráfico F(n)
    
def main():

    fileName = Choose_File.main()
    pathName = path_name (fileName)
    text_file_series = []
    text_file_series = file_reading (text_file_series, fileName)
    fileName = file_name (fileName)
    N = len(text_file_series) #serie size
    #print ("N: ", N)
    N_series = []
    
    for i in range (N): 
        N_series.append(1+i)
        
    #plot_graphic (N_series, text_file_series) # Original time series
    X = average_value_of_series(text_file_series, N)
    Yk = accumulated_series (text_file_series, N, X) # Cumulative after the average was withdrawn
    #plot_graphic(N_series, Yk)
    regressao_linear_simples_naosobreposto(text_file_series, N_series, Yk, 4, fileName, pathName)
    regressao_linear_simples_sobreposto(text_file_series, N_series, Yk, 4, fileName, pathName)
 

#-----------------------------------------------------
if __name__ == '__main__': 
    main()
