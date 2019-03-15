import numpy as np
import matplotlib.pyplot as plt

def file_reading (text_file_series): #lê arquivo
    
    file_manipulator = open('random.txt', 'r')
    for i in file_manipulator:
        i = i.rstrip()
        text_file_series.append(float(i))
    file_manipulator.close()
    print(text_file_series)

    return text_file_series

def average_value_of_series(text_file_series, N) : #valor médio dos elementos da série
    
    sum_Xi = 0
    for i in range (N) :
        sum_Xi = text_file_series[i] + sum_Xi
    print (sum_Xi)

    X = (1/N) * sum_Xi
    print (X)

    return X

def accumulated_series (text_file_series, N, X): #série acumulada

    sum_Yk = 0
    Yk = []
    for i in range (N) :
        sum_Yk = (text_file_series[i] - X) + sum_Yk
        Yk.append(sum_Yk)
    print(sum_Yk)
    print(Yk)

    return Yk

def plot_graphic (x, y):
    plt.plot(x, y)
    plt.show()

def regressao_linear_simples_naosobreposto(x_for_adjustment, y_for_adjustment, n_pontos_ajustados):
    i = 0
    n = n_pontos_ajustados
    plt.plot(x_for_adjustment, y_for_adjustment)
    y_adjustment = []
    y_real = []

    Qb = (len(x_for_adjustment)) / n #Quantidade de blocos ajustados (não sobreposto)
    Qb = (int(Qb))

    for t in range (Qb): #ajuste não sobreposto
        x = np.array(x_for_adjustment[i:n]) # vetor com os valores de x
        y = np.array(y_for_adjustment[i:n]) # vetor com os valores de y
        p1 = np.polyfit(x,y,1) # fornece os valores do intercepto e a inclinação, 1 é o grau do polinômio
        yfit = p1[0] * x + p1[1] # calcula os valores preditos
        #print (yfit)
        y_adjustment.append(yfit) ######pontos valor ajustado (aqui tem um bloco de n pontos)
        y_real.append(y) ############ pontos valor real (aqui tem um bloco de n pontos)
        yresid = y - yfit # resíduo = valor real - valor ajustado (valor predito)
        SQresid = sum(pow(yresid,2)) # soma dos quadrados dos resíduos 
        SQtotal = len(y) * np.var(y) # número de elementos do vetor y vezes a variância de y
        R2 = 1 - SQresid/SQtotal # coeficiente de determinação
        #print(p1) # imprime o intercepto e a inclinação
        #print(R2) # imprime coeficiente de determinação
        #plt.plot(x_adjustment, y_adjustment)
        #plt.plot(x,y,'o')
        plt.plot(x,np.polyval(p1,x), color='red')
        plt.xlabel("x")
        plt.ylabel("y")
        i = n
        n = n + n_pontos_ajustados
    plt.show()

    y_temp = [] #todos os pontos (yk) ajustados
    for l in range (len(y_adjustment)):
        y_temp.extend(y_adjustment[l])

    ######## F(n) não sobreposto

    y_sum_for_Fn = 0

    for d in range (len(y_temp)):
        y_sum_for_Fn = y_sum_for_Fn + ((y_for_adjustment[d] - y_temp[d]) ** 2) # somatorio (N vzs) do (valor real - ajustados)^2

    Fn_nao_sobreposto = ((y_sum_for_Fn / (len(x_for_adjustment))) ** (1/2))  #Fn igual a raiz do somatório dividido por N (quantidade de pontos da série)
    print (Fn_nao_sobreposto)

def main():
    
    text_file_series = []
    N = 10000 # Series size
    N_series = []

    text_file_series = file_reading (text_file_series)
    
    for i in range (N): 
        N_series.append(1+i)
        
    #plot_graphic (N_series, text_file_series) # Original time series
    X = average_value_of_series(text_file_series, N)
    Yk = accumulated_series (text_file_series, N, X) # Cumulative after the average was withdrawn
    #plot_graphic(N_series, Yk)
    regressao_linear_simples_naosobreposto(N_series, Yk, 10)
 

#-----------------------------------------------------
if __name__ == '__main__': 
    main()
