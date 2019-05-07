import numpy as np
import matplotlib.pyplot as plt

def file_reading (text_file_series): #lê arquivo
    
    file_manipulator = open('teste.txt', 'r')
    for i in file_manipulator:
        i = i.rstrip()
        text_file_series.append(float(i))
    file_manipulator.close()
    #print(text_file_series)

    return text_file_series

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

def plot_graphic (x, y):
    plt.plot(x, y)
    plt.show()

def regressao_linear_simples_naosobreposto(text_file_series, N_series, yk_for_adjustment, n_pontos_ajustados):
    n_limite = n_pontos_ajustados
    while ( n_limite <= (int((len(N_series))/n_pontos_ajustados))):
        i = 0
        #n = n_pontos_ajustados
        n = n_limite
        plt.plot(N_series, yk_for_adjustment)
        yk_adjustment = []
        yk_real = []
        y_original_serie = text_file_series
           
        Qb = (len(N_series)) / n #Quantidade de blocos ajustados (não sobreposto)
        Qb = (int(Qb))

        for t in range (Qb): #ajuste não sobreposto
            x = np.array(N_series[i:n]) # vetor com os valores de x
            yk = np.array(yk_for_adjustment[i:n]) # vetor com os valores de yk (série acumulada)
            p1 = np.polyfit(x,yk,1) # fornece os valores do intercepto e a inclinação, 1 é o grau do polinômio
            yfit = p1[0] * x + p1[1] # calcula os valores preditos
            #print (yfit)
            yk_adjustment.append(yfit) ######pontos valor ajustado (aqui tem um bloco de n pontos)
            yk_real.append(yk) ############ pontos valor yK sem ajuste (aqui tem um bloco de n pontos)
            yresid = yk - yfit # resíduo = valor real yk - valor ajustado yk (valor predito)
            SQresid = sum(pow(yresid,2)) # soma dos quadrados dos resíduos 
            SQtotal = len(yk) * np.var(yk) # número de elementos do vetor y vezes a variância de y
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

        yk_temp = [] #todos os pontos (yk) ajustados
        for l in range (len(yk_adjustment)):
            yk_temp.extend(yk_adjustment[l])

        print ("Pontos ajustados:", len(yk_temp))    

        ######## F(n) não sobreposto

        y_sum_for_Fn = 0

        for d in range (len(yk_temp)):
            
            y_sum_for_Fn = y_sum_for_Fn + ((y_original_serie[d] - yk_temp[d]) ** 2) # somatorio (N vzs) do (valor real da série - ajustados de yk)^2
        #print("sum", y_sum_for_Fn)
            
        Fn_nao_sobreposto = ((y_sum_for_Fn / (len(N_series))) ** (1/2))  #Fn igual a raiz do somatório dividido por N (quantidade de pontos da série)
        print ("Série não sobreposta: F(",n_limite,") = ", Fn_nao_sobreposto)

        n_limite = n_limite + 1

'''def regressao_linear_simples_sobreposto(text_file_series, N_series, yk_for_adjustment, n_pontos_ajustados):
    i = 0
    n = n_pontos_ajustados
    plt.plot(N_series, yk_for_adjustment)
    yk_adjustment = []
    yk_real = []
    y_original_serie = text_file_series

    Qb = (len(N_series)) - n #Quantidade de blocos ajustados (sobreposto)
    Qb = (int(Qb))

    for t in range (Qb): #ajuste sobreposto
        x = np.array(N_series[i:(n+1)]) # vetor com os valores de x
        yk = np.array(yk_for_adjustment[i:(n+1)]) # vetor com os valores de yk (série acumulada)
        p1 = np.polyfit(x,yk,1) # fornece os valores do intercepto e a inclinação, 1 é o grau do polinômio
        yfit = p1[0] * x + p1[1] # calcula os valores preditos
        #print (yfit)
        yk_adjustment.append(yfit) ######pontos valor ajustado (aqui tem um bloco de n pontos)
        yk_real.append(yk) ############ pontos valor yK sem ajuste (aqui tem um bloco de n pontos)
        yresid = yk - yfit # resíduo = valor real yk - valor ajustado yk (valor predito)
        SQresid = sum(pow(yresid,2)) # soma dos quadrados dos resíduos 
        SQtotal = len(yk) * np.var(yk) # número de elementos do vetor y vezes a variância de y
        R2 = 1 - SQresid/SQtotal # coeficiente de determinação
        #print(p1) # imprime o intercepto e a inclinação
        #print(R2) # imprime coeficiente de determinação
        #plt.plot(x_adjustment, y_adjustment)
        #plt.plot(x,y,'o')
        plt.plot(x,np.polyval(p1,x), color='red')
        plt.xlabel("x")
        plt.ylabel("y")
        i = i+1
        n = n + 1
    plt.show()

    yk_temp = [] #todos os pontos (yk) ajustados
    for l in range (len(yk_adjustment)):
        yk_temp.extend(yk_adjustment[l])

    print ("Pontos ajustados:", len(yk_temp))

    ######## F(n) sobreposto
    y_sum_for_Fn = 0
    e = 0
    contador = 0
    q = n_pontos_ajustados
    for d in range ((n_pontos_ajustados+1)*(len(N_series)-n_pontos_ajustados)):
        if (e == q):
            contador = contador + 1
            e = contador
            q = q + 1
        print (" i ", e, "i, n ", d)    
        #y_sum_for_Fn = y_sum_for_Fn + ((y_original_serie[e] - yk_temp [d])**2)    
        e = e + 1   
        
    #print("sum", y_sum_for_Fn)
        
    Fn_sobreposto = ((y_sum_for_Fn / ((n_pontos_ajustados+1)*(len(N_series)-n_pontos_ajustados))) ** (1/2))  #Fn igual a raiz do somatório dividido por ((n_pontos_ajustados+1)*(len(N_series)-n_pontos_ajustados))
    print ("Série sobreposta: F(n) = ", Fn_sobreposto)'''

def main():
    
    text_file_series = []
    text_file_series = file_reading (text_file_series)
    N = len(text_file_series) #serie size
    print ("N: ", N)
    N_series = []
    
    for i in range (N): 
        N_series.append(1+i)
        
    #plot_graphic (N_series, text_file_series) # Original time series
    X = average_value_of_series(text_file_series, N)
    Yk = accumulated_series (text_file_series, N, X) # Cumulative after the average was withdrawn
    #plot_graphic(N_series, Yk)
    regressao_linear_simples_naosobreposto(text_file_series, N_series, Yk, 4)
    #regressao_linear_simples_sobreposto(text_file_series, N_series, Yk, 4)
 

#-----------------------------------------------------
if __name__ == '__main__': 
    main()
