#1
def heterozygosity(n,x_list):
    
    if n < 2 or round(sum(x_list),1) != 1.0:
        return False
    
    m = len(x_list)
    Sub1 = 0
    for i in range(m):
        Sub1 += (x_list[i])**2
    h = (float(n)/(n-1))*(1-Sub1)
    return h
    
#2
def heterozygosity_var(n,x_list):

    if n < 2 or round(sum(x_list),1) != 1.0:
        return False
    
    sub1 = 0
    sub2 = 0
    m = len(x_list)
    for i in range(m):
        sub1 += x_list[i]**3
        sub2 += x_list[i]**2

    part1 = 2.0/(n*(n-1))
    part2 = 2.0*(n-2)*(sub1-sub2**2)

    Vh = part1 * ( part2 + sub2 - sub2**2 ) 
    return Vh

#3    
def haplotype_diversity(n,x_list):

    if n < 2 or round(sum(x_list),1) != 1.0:
        return False
    
    m = len(x_list)
    Sub1 = 0
    for i in range(m):
        Sub1 += (x_list[i])**2
    h = (float(n)/(n-1))*(1-Sub1)
    return h
#4
def haplotype_diversity_var(n,x_list):

    if n >= 2 and round(sum(x_list),4) == 1.0:
        pass
    else:
        return False
    
    sub1 = 0
    sub2 = 0
    m = len(x_list)
    for i in range(m):
        sub1 += x_list[i]**3
        sub2 += x_list[i]**2

    part1 = 2.0/(n*(n-1))
    part2 = 2.0*(n-2)*(sub1-sub2**2)

    Vhd = part1 * ( part2 + sub2 - sub2**2 ) 
    return Vhd

#5
def nucleotide_diversity(n,L,x_list):

    for subList in x_list:
        if round(sum(subList),1) != 1.0:
            return False
    if n <= 1 or L<1:
        return False
    
    def nucleotide_diversity_locus(n,x_list):
    
        m = len(x_list)
        Sub1 = 0
        for i in range(m):
            Sub1 += (x_list[i])**2
        h = (float(n)/(n-1))*(1-Sub1)
        return h

    S = len(x_list)
    sub1 = 0
    for j in range(S):
        sub1 += nucleotide_diversity_locus(n,x_list[j])

    pi = float(sub1) / L
    return pi

#6
def nucleotide_diversity_var(n,L,x_list):


    for subList in x_list:
        if round(sum(subList),1) != 1.0:
            return False
    if n <= 2 or L<1:
        return False
    
    def h_value(n,x_list):
    
        m = len(x_list)
        Sub1 = 0
        for i in range(m):
            Sub1 += (x_list[i])**2
        h = (float(n)/(n-1))*(1-Sub1)
        return h

    
    def nucleotide_diversity(n,L,x_list):
        S = len(x_list)
        sub1 = 0
        for j in range(S):
            sub1 += h_value(n,x_list[j])

        pi = float(sub1) / L
        return pi


    pi_value = nucleotide_diversity(n,L,x_list)
    
    sub1 = float(n+1)/(3*(n-1)*L)
    sub2 = float(2*(n**2+n+3))/(9*n*(n-1))
    Vpi = sub1*pi_value + sub2*(pi_value**2)
    return Vpi

#7
def nucleotide_differences(n,x_list):

    for subList in x_list:
        if round(sum(subList),1) != 1.0:
            return False
    if n <= 2:
        return False

    def h_value(n,x_list):
    
        m = len(x_list)
        Sub1 = 0
        for i in range(m):
            Sub1 += (x_list[i])**2
        h = (float(n)/(n-1))*(1-Sub1)
        return h

    S = len(x_list)

    k = 0
    for j in range(S):
        k += h_value(n,x_list[j])
    return k

#8
def nucleotide_differences_var(n,x_list):


    for subList in x_list:
        if round(sum(subList),1) != 1.0:
            return False
    if n <= 2:
        return False
    
    def h_value(n,x_list):
        m = len(x_list)
        Sub1 = 0
        for i in range(m):
            Sub1 += (x_list[i])**2
        h = (float(n)/(n-1))*(1-Sub1)
        return h

    def nucleotide_differences(n,x_list):

        S = len(x_list)

        k = 0
        for j in range(S):
            k += h_value(n,x_list[j])
        return k

    k_value = nucleotide_differences(n,x_list)


    sub1 = 3*n*(n+1)
    sub2 = 2*(n**2+n+3)
    sub3 = 11*(n**2-7*n+6)

    Vk = float(sub1*k_value+sub2*k_value**2) / sub3
    return Vk
    
#9
def Tajima_D(n,S,k):

    if n<=1 or S<1:
        return False
    
    a1 = 0
    for i in range(1,n):
        a1 += (1.0/i)

    a2 = 0
    for i in range(1,n):
        a2 += (1.0/(i**2))

    b1 = float(n+1) / (3*n-3)
    b2 = float(2*(n**2+n+3)) / (9*n*(n-1))

    c1 = b1 - 1.0/a1
    c2 = b2 - (float(n+2)/(a1*n)) + (a2/(a1**2))

    e1 = float(c1)/a1
    e2 = float(c2)/(a1**2 + a2)

    sub1 = k - float(S)/a1
    sub2 = (e1*S+e2*S*(S-1))**0.5

    D = sub1/sub2
    return D
    
#10
def Fu_Li_D(n,Eta,Etae):

    if n<=2 :
        return False
    
    an = 0
    bn = 0
    for k in range(1,n):
        an += (1.0/k)
        bn += (1.0/k**2)

    cn = float(2*(n*an-2*(n-1)))/((n-1)*(n-2))
    vd = 1+(float(an**2)/(bn+an**2))*(cn-((float(n+1))/(n-1)))
    ud = an -1-vd

    sub1 = Eta-an*Etae
    sub2 = (ud*Eta+vd*(Eta**2))**0.5

    D = float(sub1)/sub2
    return D
#11
def Fu_Li_F(n,k,Eta,Etae):

    if n<=2 :
        return False
    
    an = 0
    bn = 0
    for i in range(1,n):
        an += (1.0/i)
        bn += (1.0/i**2)
        
    anplus = an + (1.0/(i+1))
    
    cn = float(2*(n*an-2*(n-1)))/((n-1)*(n-2))

    #vF
    sub1 = (2.0*(n**2+n+3))/(9*n*(n-1))
    sub2 = an**2+bn
    vF = (cn+sub1-(2.0/(n-1)))/sub2

    #uF
    sub1 = float(n+1)/(3*n-3)
    sub2 = float(4*n+4)/((n-1)**2)
    sub3 = anplus - float(2*n)/(n+1)

    uF = (1+sub1-sub2*sub3)/an - vF


    sub1 = (uF*Eta+vF*(Eta**2))**0.5

    F = (k - Etae)/(uF*Eta + vF*Eta*Eta)**0.5
    return F
    
 #12   
def Fu_Li_Dstar(n,Eta,Etae):

    if n<=2 :
        return False
    
    an = 0
    bn = 0
    for k in range(1,n):
        an += (1.0/k)
        bn += (1.0/k**2)
    an1 = an + (1.0/n)
    cn = float(2*(n*an-2*(n-1)))/((n-1)*(n-2))

    d1 = cn + float(n - 2) / ((n - 1)**2)
    d2 = 2.0 / (n - 1) 
    d3 = 3.0/2 - (2*an1 - 3) / (n - 2) - 1.0 / n
    dn = d1 + d2*d3

    vd1 = ((float(n) / (n - 1))**2)*bn   
    vd2 = an*an*dn
    vd3 = (n*an*(an + 1) / (n - 1)**2)*2
    vd4 = an*an + bn
    vD = (vd1 + vd2 - vd3) / vd4

    ud1 = n/float(n - 1)
    ud2 = an - n/float(n - 1)
    uD = ud1*ud2 - vD
    

    D = ((float(n) / (n - 1))*Eta - an*Etae) / (( uD*Eta + vD*(Eta**2) )**0.5)
    return D

#13    
def Fu_Li_Fstar(n, k, Eta, Etae) :

    if n<=2 :
        return False
    
    an = 0
    bn = 0
    an1 = 0
    for j in range(1, n) :
        an = an + 1.0/j
        bn = bn + 1.0/(j)**2
    
    cn = ((n*an - 2*(n -1)) / float(((n -1)*(n - 2))))*2
    
    for j in range(1, n + 1) :
        an1 = an1 + 1.0/j  
    d1 = cn + float(n - 2) / ((n - 1)**2)
    d2 = 2.0 / (n - 1) 
    d3 = 3.0/2 - (2*an1 - 3) / (n - 2) - 1.0 / n
    dn = d1 + d2*d3

      
    vf1 = dn + 2.0*(n**2 + n + 3) / (9*n*(n - 1)) 
    vf2 = -2.0/(n - 1)*(4*bn - 6 + 8.0/n)
    vf3 = an*an + bn
    vF = (vf1 + vf2)/ vf3 

    uf1 = n /(n - 1.0) 
    uf2 = (n + 1) / (3.0*(n - 1))
    uf3 =  - 2*2.0/(n*(n - 1))
    uf4 = 2.0*(n + 1)/((n - 1)**2)
    uf5 =  an1 - 2.0*n/ (n + 1)

    uF = float(uf1 + uf2 + uf3 + uf4*uf5)/an - vF
    

    F = (k - (n - 1) / float(n)*Etae)/((uF*Eta + vF*(Eta**2))**0.5)
    return F

#14
def Strobeck_S(n, k, j) :

    if n <=2 or j < 1:
        return False
    
    def stirling(n, k):
        n1=n
        k1=k
        if n<=0:
            return 1
     
        elif k<=0:
            return 0
     
        elif (n==0 and k==0):
            return -1
     
        elif n!=0 and n==k:
            return 1
     
        elif n<k:
            return 0
 
        else:
            t1 = stirling(n1-1,k1)
            t2 = stirling(n1-1,k1-1)
        
        return t2-(n1-1)*t1
    sn = 1*k
    for i in range(1, n) :
        sn = sn*(k + i)
    s1 = 1.0/sn
    s2 = 0
    for i in range(1, j + 1) :
        s2 = s2 + abs(stirling(n, i))*k**i
    sn = s1*s2
    return sn

    
#15
def Fu_W(n, k, j) :
    
    if n <=2 or j < 1:
        return False
    
    an = 0
    for i in range(1, n) :
        an = an + 1.0/i

    w = k/an
    def stirling(n, w):
        n1=n
        k1=w
        if n<=0:
            return 1
     
        elif w<=0:
            return 0
     
        elif (n==0 and w==0):
            return -1
     
        elif n!=0 and n==w:
            return 1
     
        elif n<w:
            return 0
 
        else:
            t1 = stirling(n1-1,k1)
            t2 = stirling(n1-1,k1-1)
        
        return t2-(n1-1)*t1
    sn = 1*w
    for i in range(1, n) :
        sn = sn*(w + i)
    s1 = 1.0/sn
    s2 = 0
    for i in range(1, j + 1) :
        s2 = s2 + abs(stirling(n, i))*w**i
    sn = s1*s2

    return sn
    
#16
def Fu_Fs(n, k, j) :

    if n <=2 or j < 1:
        return False
    
    import math
    def stirling(n, k):
        n1=n
        k1=k
        if n<=0:
            return 1
     
        elif k<=0:
            return 0
     
        elif (n==0 and k==0):
            return -1
     
        elif n!=0 and n==k:
            return 1
     
        elif n<k:
            return 0
 
        else:
            t1 = stirling(n1-1,k1)
            t2 = stirling(n1-1,k1-1)
        
        return t2-(n1-1)*t1
    sn = 1*k
    for i in range(1, n) :
        sn = sn*(k + i)
    s1 = 1.0/sn
    s2 = 0
    for i in range(j, n + 1) :
        s2 = s2 + abs(stirling(n, i))*k**i
    s_ = s1*s2
    F = math.log(s_/(1 - s_))
    return F

# 17
def Fu_Watterson_W(x_list):
    m = len(x_list)
    if m<1:
        return False

    sub1 = 0
    for f in x_list:
        sub1 += (f**2)

    W = (sum(x_list)**(-2))*sub1
    return W
    
#18
def Fay_Wu_H(seq_number, i_list, Si_list) :

    if len(i_list) != len(Si_list):
        return False
    if seq_number <2:
        return False
    
    from itertools import izip
    theta_pi = 0
    theta_H = 0
    for i, Si in izip( i_list, Si_list) :
        theta_pi = theta_pi + 2.0*Si*i*(seq_number - i)/(seq_number*(seq_number - 1))
        theta_H = theta_H + 2.0*Si*(i**2)/(seq_number*(seq_number - 1))

    H = theta_pi - theta_H
    return H
    
#19
def Fay_Wu_H_nor(n,S, i_list, si_list) :

    if n <=1 or S< 1 :
        return False
    if len(i_list) != len(si_list):
        return False
    
    from itertools import izip
    an = 0
    bn = 0

    for i in range(1,n):
        an += (1.0/i)
        bn += (1.0/(i**2))
    bn1 = bn+(1.0/(n**2))

    
    Theta2 = float(S*(S-1))/(an**2+bn)
    Theta = float(S)/an

    var_pi_L_1 = float((n-2)*Theta)/(6*(n-1))
    var_pi_L_2 = ( 18*n*n*(3*n+2)*bn1-(88*(n**3) + 9*n*n - 13*n + 6) )*Theta2

    var_pi_L_3 = 9*n*(n-1)*(n-1)
    VarPiL = var_pi_L_1+float(var_pi_L_2)/float(var_pi_L_3)


    ThetaPi = 0
    ThetaL = 0
    for i,Si in izip(i_list, si_list):

        ThetaPi += float(2*Si*i*(n-i))/(n*(n-1))

        ThetaL += i*Si


    ThetaL = ThetaL*(1.0/(n-1))

    Hn = (ThetaPi - ThetaL)/(VarPiL**0.5)

    return Hn
    
#20
def Zeng_E(n, S, i_list, Si_list) :

    if n <=1 or S< 1 :
        return False
    if len(i_list) != len(Si_list):
        return False
    
    from itertools import izip
    theta_L = 0
    for i, Si in izip( i_list, Si_list) :
        theta_L = theta_L + 1.0/(n - 1)*i*Si 
    an = 0.0
    bn = 0.0
    for number in range(1, n) :
        an = an + 1.0/number
        bn = bn + 1.0/(number**2)
    theta_W = S/an
    theta = theta_W
    theta2 = S*(S - 1.0)/(an*an + bn)
    Var1 = n/(2.0*(n - 1)) - 1.0/an
    Var2 = bn/(an*an) + 2.0*(n/(n-1.0))**2*bn
    Var3 = -2.0*(n*bn - n + 1)/((n - 1)*an)
    Var4 = -(3.0*n + 1)/(n - 1)
    Var = Var1*theta + (Var2 + Var3 + Var4)*theta2
    E = (theta_L - theta_W)/Var**0.5
    return E
    
#21
def Ramos_Onsins_R2(n, S, k, u_list):

    if n <=1 or S< 1 :
        return False

    R = 0
    for u in u_list :
        R = R + (u - k/2.0)**2/n  
    R2 = R**0.5/S
    return R2

    
#22
def Ramos_Onsins_R3(n, S, k, u_list) :

    if n <=1 or S< 1 :
        return False
    
    R = 0
    for u in u_list :
        R = R + ((u - k/2.0)**3)/n
    if R < 0:
        R3 = 'NaN'
    else :
        R3 = R**(1.0/3)/S 
    return R3
   
#23 
def Ramos_Onsins_R4(n, S, k, u_list) :

    if n <=1 or S< 1 :
        return False
    
    R = 0
    for u in u_list :
        R = R + (u - k/2.0)**4/n
    R4 = R**(1.0/4)/S
    return R4

#24 
def Ramos_Onsins_R2E(n, S, k, v_list) :

    if n <=1 or S< 1 :
        return False
    
    R = 0 
    for v in v_list :
        R = R + (v - k/2.0)**2/n
    R2E = R**0.5/ S   
    return R2E
    
#25
def Ramos_Onsins_R3E(n, S, k, v_list) :

    if n <=1 or S< 1 :
        return False
    
    R = 0 
    for v in v_list :
        R = R + (v - k/2.0)**3/n
    if R < 0 :
        R3E = 'NaN'
    else :
        R3E = R**(1.0/3)/ S   
    return R3E

#26
def Ramos_Onsins_R4E(n, S, k, v_list) :
    R = 0 
    for v in v_list :
        R = R + (v - k/2.0)**4/n

    R4E = R**(1.0/4)/ S   
    return R4E

#27    
def Ramos_Onsins_Ch(n, S, k, U) :
    m = n*k/(n - 1.0)
    Ch = (U - m)**2*S/(m*(S - m))
    return Ch


#28
def Ramos_Onsins_Che(n, S, k, V) :

    if n < 2:
        return False
    m = n*k/(n - 1.0)
    Che = (V - m)**2*S/(m*(S - m))
    return Che

    
#29
def Ramos_Onsins_ku(n, d, k, d_list, W_list) :
    if len(d_list) != len(W_list) or n < 2 :
        return False
    
    from itertools import izip
    nc = n*(n - 1.0)/2
    q = 0
    s = 0
    for i, W in izip(d_list, W_list) :
        q += W*(i - k)**4
        s += float(W*(i - k)**2)/(nc-1)
    sub1 = float(nc*(nc+1)*q)/((nc-1)*(nc-2)*(nc-3)*(s**2))
    sub2 = float(3*((nc-1)**2))/((nc-2)*(nc-3))
    ku_value = sub1 - sub2
    return ku_value

#30    
def raggedness_index_rg(x_list) :

    if round(sum(x_list),4) != 1.0:
        return False
    d = len(x_list)
    x_list.append(0)
    rg = 0
    for i in range(1, d+1) :

        rg = rg + (x_list[i] - x_list[i - 1])**2
    return rg
    
#31
def Wright_Fst(x_list) :


    if len(x_list) <= 2:
        return False
    
    S = len(x_list)
    p_bar = float(sum(x_list))/S

    p2 = 0

    for x in x_list:
        p2 += (x-p_bar)**2
    p2 = float(p2)/S

    Fst = p2/(p_bar*(1-p_bar))
    
    return Fst
#32    
def Wright_Fst_mean(x_list, S) :

    if len(x_list)<=2:
        return False
    for x in x_list:
        if round(sum(x),4) != 1.0:
            return False
    numerator = 0.0
    denominator = 0.0
    for k in range(len(x_list[0])) :
        pk_bar = 0.0
        for s in range(S) :
            pk_bar = pk_bar + x_list[s][k]
        pk_bar = pk_bar/S
        
        denominator = denominator + pk_bar*(1 - pk_bar)
        
        a = 0.0
        for s in range(S) :
            a = a + (x_list[s][k] - pk_bar)**2
        numerator = numerator + a/S
    Fst_bar = numerator/denominator
    
    return Fst_bar

#33
def Wright_Fis(x_list) :
    if len(x_list) < 1:
        return False
    s = len(x_list)
    Gtype1 = 0.0
    Gtype2 = 0.0
    Gtype3 = 0.0
    for i in range(s) :
        Gtype1 = Gtype1 + x_list[i][0]
        Gtype2 = Gtype2 + x_list[i][2]
        Gtype3 = Gtype3 + x_list[i][1]
    He = (2*Gtype1 + Gtype3)*(2*Gtype2 + Gtype3)/(2*(Gtype1 + Gtype3 + Gtype2)**2)

    Ho = Gtype3/(Gtype1 + Gtype3 + Gtype2)
    Fis = (He - Ho)/He
    return Fis

#34
def Nei_Gst(S_list,x_list) :

    len_list = []
    for x in x_list:
        if round(sum(x),4) != 1:
            return False
        len_list.append(len(x))
    if len(set(len_list)) != 1:
        return False
    if len(x_list) != len(S_list):
        return False

    def Nei_Jt(S_list,x_list):
        S = len(x_list)
        k_max = len(x_list[0])
        wi_list = []
        sumN = sum(S_list)
        for N in S_list:
            wi_list.append(float(N)/sumN)

        Jt_list = []
        for k in range(k_max):
        
            Jt_x = 0
            for i in range(S):
                wi = wi_list[i]
                Jt_x += (wi*x_list[i][k])
            Jt_list.append(Jt_x**2)
        Jt = sum(Jt_list)
        return Jt

    def Nei_Dst(S_list,x_list) :

    
        def D(S_list,x_list):
            S = len(x_list)
            k_max = len(x_list[0])
        
            value_list = []
            for k in range(k_max):
                A1value = 0
                for i in range(S):
                    for j in range(i+1,S):
                        A1value += (x_list[i][k] - x_list[j][k])**2
                value_list.append(A1value)
            return sum(value_list)

        Dvalue = D(S_list,x_list)
        S = len(x_list)
        Dst = float(Dvalue) / (S**2)
        return Dst

    Jt = Nei_Jt(S_list,x_list)

    Dst = Nei_Dst(S_list,x_list)
    Ht = 1-Jt

    Gst = float(Dst)/Ht
    return Gst

#35
def Nei_Dst(x_list) :

    for x in x_list:
        if round(sum(x),4) != 1:
            return False

    def D(x_list):
        S = len(x_list)
        k_max = len(x_list[0])
        
        value_list = []
        for k in range(k_max):
            A1value = 0
            for i in range(S):
                for j in range(i+1,S):
                    A1value += (x_list[i][k] - x_list[j][k])**2
            value_list.append(A1value)
        return sum(value_list)

    Dvalue = D(x_list)
    S = len(x_list)
    Dst = float(Dvalue) / (S**2)
     
    return Dst

#36
def Nei_Jt(S_list,x_list):
    if len(x_list)<1:
        return False
    S = len(x_list)
    k_max = len(x_list[0])
    wi_list = []
    sumN = sum(S_list)
    for N in S_list:
        wi_list.append(float(N)/sumN)

    Jt_list = []
    for k in range(k_max):
        
        Jt_x = 0
        for i in range(S):
            wi = wi_list[i]
            Jt_x += (wi*x_list[i][k])
        Jt_list.append(Jt_x**2)
    Jt = sum(Jt_list)
    return Jt

#37
def Nei_Js(x_list) :
    if len(x_list)<1:
        return False
    for x in x_list:
        if round(sum(x),4) != 1:
            return False
        
    S = len(x_list)
    J = 0
    for x in x_list :
        for i in range(len(x)) :
            J = J + (x[i]/float(sum(x)))**2
    Js = J/S
    return Js

#38
def Nei_Rst(x_list):
    
    for x in x_list:
        if round(sum(x),4) != 1:
            return False

    def Nei_Dst(x_list) :

    
        def D(x_list):
            S = len(x_list)
            k_max = len(x_list[0])
        
            value_list = []
            for k in range(k_max):
                A1value = 0
                for i in range(S):
                    for j in range(i+1,S):
                        A1value += (x_list[i][k] - x_list[j][k])**2
                value_list.append(A1value)
            return sum(value_list)

        Dvalue = D(x_list)
        S = len(x_list)
        Dst = float(Dvalue) / (S**2)
        return Dst

    k_max = len(x_list[0])
    S = len(x_list)
    Dst = Nei_Dst(x_list)
    Dm = (float(S)/(S-1))*Dst
    
    Ji_list = []
    for k in range(k_max):
        for i in range(S):
                Ji_list.append(x_list[i][k]**2)
    Hs = 1-float(sum(Ji_list))/S
    Rst = float(Dm)/Hs
    return Rst
#39
def Hedrick_Gst_stand(S_list,x_list):

    len_list = []
    for x in x_list:
        if round(sum(x),4) != 1:
            return False
        len_list.append(len(x))
    if len(set(len_list)) != 1:
        return False
    if len(x_list) != len(S_list):
        return False
    
    def Nei_Gst(S_list,x_list) :

        def Nei_Jt(S_list,x_list):
            S = len(x_list)
            k_max = len(x_list[0])
            wi_list = []
            sumN = sum(S_list)
            for N in S_list:
                wi_list.append(float(N)/sumN)

            Jt_list = []
            for k in range(k_max):
        
                Jt_x = 0
                for i in range(S):
                    wi = wi_list[i]
                    Jt_x += (wi*x_list[i][k])
                Jt_list.append(Jt_x**2)
            Jt = sum(Jt_list)
            return Jt

        def Nei_Dst(S_list,x_list) :

    
            def D(S_list,x_list):
                S = len(x_list)
                k_max = len(x_list[0])
        
                value_list = []
                for k in range(k_max):
                    A1value = 0
                    for i in range(S):
                        for j in range(i+1,S):
                            A1value += (x_list[i][k] - x_list[j][k])**2
                    value_list.append(A1value)
                return sum(value_list)

            Dvalue = D(S_list,x_list)
            S = len(x_list)
            Dst = float(Dvalue) / (S**2)
            return Dst

        Jt = Nei_Jt(S_list,x_list)
        Dst = Nei_Dst(S_list,x_list)
        Ht = 1-Jt

        Gst = float(Dst)/Ht
        return Gst

    def J(S_list,x_list):
        S = len(x_list)
        k_max = len(x_list[0])
        
        Ji_list = []
        for k in range(k_max):
            for i in range(S):
                Ji_list.append(x_list[i][k]**2)

        return sum(Ji_list)
    
    S = len(x_list)
    J_value = J(S_list,x_list)

    Hs = 1-(float(J_value)/S)

    Gst = Nei_Gst(S_list,x_list)

    Gst_stand  = float(Gst*(S-1+Hs))/((S-1)*(1-Hs))
    return Gst_stand

#40
def Jost_D(S_list,x_list):

    len_list = []
    for x in x_list:
        if round(sum(x),4) != 1:
            return False
        len_list.append(len(x))
    if len(set(len_list)) != 1:
        return False
    if len(x_list) != len(S_list):
        return False
    
    def Ht_func(S_list,x_list) :

        def Nei_Jt(S_list,x_list):
            S = len(x_list)
            k_max = len(x_list[0])
            wi_list = []
            sumN = sum(S_list)
            for N in S_list:
                wi_list.append(float(N)/sumN)

            Jt_list = []
            for k in range(k_max):
        
                Jt_x = 0
                for i in range(S):
                    wi = wi_list[i]
                    Jt_x += (wi*x_list[i][k])
                Jt_list.append(Jt_x**2)
            Jt = sum(Jt_list)
            return Jt

        Jt = Nei_Jt(S_list,x_list)

        Ht = 1-Jt

        return Ht


    def J(S_list,x_list):
        S = len(x_list)
        k_max = len(x_list[0])
        
        Ji_list = []
        for k in range(k_max):
            for i in range(S):
                Ji_list.append(x_list[i][k]**2)

        return sum(Ji_list)
    
    S = len(x_list)
    J_value = J(S_list,x_list)

    Hs = 1-(float(J_value)/S)

    Ht = Ht_func(S_list,x_list)

    D = (float(Ht-Hs)/(1-Hs))*(float(S)/(S-1))
    return  D
#41
def Weir_Cockerham_thetaU(freq_list, heterozygosity_list, n_list) :

    if len(set([len(freq_list),len(heterozygosity_list) ,len(n_list)])) != 1:
        return False
    for freq in freq_list:
        if round(sum(freq),4) != 1:
            return False
        
    import numpy as np
    from itertools import izip
    
    n_bar = sum(n_list)/float(len(n_list))

    
    n = np.array(n_list)
    n2=sum(n*n)
    nc = (sum(n) - float(n2)/sum(n))/(len(n_list) - 1.0)

    
    numerator = 0.0
    for n in range(len(n_list)) :
        numerator = numerator + heterozygosity_list[n]*n_list[n]
    h_bar = numerator/sum(n_list)
    cu = h_bar/2.0

    theta = 0.0
    for i in range(len(freq_list[0])) :
        numerator = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator = numerator + freq_list[j][i]*n   
        pu_bar = numerator/sum(n_list)
        
        numerator1 = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator1 = numerator1 + (freq_list[j][i] - pu_bar)**2*n
        denominator = (len(n_list) - 1.0)/len(n_list)*sum(n_list)
        su2 = numerator1/denominator
        
        bu1 = n_bar/(n_bar - 1.0)
        bu2 = pu_bar*(1 - pu_bar) - su2*(len(n_list) - 1.0)/len(n_list) - h_bar*(2*n_bar - 1.0)/(4*n_bar)
        bu = bu1*bu2
        
        au1 = n_bar/nc
        au2 = pu_bar*(1.0-pu_bar) - (len(n_list) - 1.0)/len(n_list)*su2 - 1.0/4*h_bar 
        au = au1*(su2 - 1.0/(n_bar - 1)*au2)

        thetau = au/(au + bu + cu)
        theta = theta +  thetau
    theta = theta/len(freq_list[0])
    return theta

#42
def Weir_Cockerham_thetaRH(freq_list, heterozygosity_list, n_list) :


    if len(set([len(freq_list),len(heterozygosity_list) ,len(n_list)])) != 1:
        return False
    for freq in freq_list:
        if round(sum(freq),4) != 1:
            return False

        
    import numpy as np
    from itertools import izip
    
    n_bar = sum(n_list)/float(len(n_list))
    n = np.array(n_list)
    n2=sum(n*n)
    nc = (sum(n) - float(n2)/sum(n))/(len(n_list) - 1.0)
    
    numerator = 0.0
    for n in range(len(n_list)) :
        numerator = numerator + heterozygosity_list[n]*n_list[n]
    h_bar = numerator/sum(n_list)
    cu = h_bar/2.0

    theta = 0.0
    for i in range(len(freq_list[0])) :
        numerator = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator = numerator + freq_list[j][i]*n   
        pu_bar = numerator/sum(n_list)
        
        numerator1 = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator1 = numerator1 + (freq_list[j][i] - pu_bar)**2*n
        denominator = (len(n_list) - 1.0)/len(n_list)*sum(n_list)
        su2 = numerator1/denominator
        
        bu1 = n_bar/(n_bar - 1.0)
        bu2 = pu_bar*(1 - pu_bar) - su2*(len(n_list) - 1.0)/len(n_list) - h_bar*(2*n_bar - 1.0)/(4*n_bar)
        bu = bu1*bu2
        
        au1 = n_bar/nc
        au2 = pu_bar*(1.0-pu_bar) - (len(n_list) - 1.0)/len(n_list)*su2 - 1.0/4*h_bar 
        au = au1*(su2 - 1.0/(n_bar - 1)*au2)

        thetau = au/(au + bu + cu)
        theta = theta + (1.0 - pu_bar)*thetau
    theta = 1.0/(len(freq_list[0]) -1)*theta
    return theta
#43
def Weir_Cockerham_thetaW(freq_list, heterozygosity_list, n_list) :


    if len(set([len(freq_list),len(heterozygosity_list) ,len(n_list)])) != 1:
        return False
    for freq in freq_list:
        if round(sum(freq),4) != 1:
            return False
    
    import numpy as np
    from itertools import izip
    
    n_bar = sum(n_list)/float(len(n_list))
    n = np.array(n_list)
    n2=sum(n*n)
    nc = (sum(n) - float(n2)/sum(n))/(len(n_list) - 1.0)
    
    numerator = 0.0
    for n in range(len(n_list)) :
        numerator = numerator + heterozygosity_list[n]*n_list[n]
    h_bar = numerator/sum(n_list)
    cu = h_bar/2.0

    thetau = 0.0
    thetaa = 0.0
    for i in range(len(freq_list[0])) :
        numerator = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator = numerator + freq_list[j][i]*n   
        pu_bar = numerator/sum(n_list)
        
        numerator1 = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator1 = numerator1 + (freq_list[j][i] - pu_bar)**2*n
        denominator = (len(n_list) - 1.0)/len(n_list)*sum(n_list)
        su2 = numerator1/denominator
        
        bu1 = n_bar/(n_bar - 1.0)
        bu2 = pu_bar*(1 - pu_bar) - su2*(len(n_list) - 1.0)/len(n_list) - h_bar*(2*n_bar - 1.0)/(4*n_bar)
        bu = bu1*bu2
        
        au1 = n_bar/nc
        au2 = pu_bar*(1.0-pu_bar) - (len(n_list) - 1.0)/len(n_list)*su2 - 1.0/4*h_bar 
        au = au1*(su2 - 1.0/(n_bar - 1)*au2)

        thetau = thetau + au + bu + cu
        thetaa = thetaa +  au
    theta = thetaa/thetau
    return theta

#44
def Weir_Cockerham_fU(freq_list, heterozygosity_list, n_list) :


    if len(set([len(freq_list),len(heterozygosity_list) ,len(n_list)])) != 1:
        return False
    for freq in freq_list:
        if sum(freq) != 1:
            return False
    
    from itertools import izip
    
    n_bar = sum(n_list)/float(len(n_list))

    numerator = 0.0
    for n in range(len(n_list)) :
        numerator = numerator + heterozygosity_list[n]*n_list[n]
    h_bar = numerator/sum(n_list)
    cu = h_bar/2.0

    f_u = 0.0
    for i in range(len(freq_list[0])) :
        numerator = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator = numerator + freq_list[j][i]*n   
        pu_bar = numerator/sum(n_list)
        
        numerator1 = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator1 = numerator1 + (freq_list[j][i] - pu_bar)**2*n
        denominator = (len(n_list) - 1.0)/len(n_list)*sum(n_list)
        su2 = numerator1/denominator
        
        bu1 = n_bar/(n_bar - 1.0)
        bu2 = pu_bar*(1 - pu_bar) - su2*(len(n_list) - 1.0)/len(n_list) - h_bar*(2*n_bar - 1.0)/(4*n_bar)
        bu = bu1*bu2
        
        f_u = f_u + (1.0 - cu/(bu + cu))
    f_U = f_u/len(freq_list[0])
    return f_U

#45
def Weir_Cockerham_fRH(freq_list, heterozygosity_list, n_list) :

    if len(set([len(freq_list),len(heterozygosity_list) ,len(n_list)])) != 1:
        return False
    for freq in freq_list:
        if round(sum(freq),4) != 1:
            return False
    
    from itertools import izip
    
    n_bar = sum(n_list)/float(len(n_list))

    
    numerator = 0.0
    for n in range(len(n_list)) :
        numerator = numerator + heterozygosity_list[n]*n_list[n]
    h_bar = numerator/sum(n_list)
    cu = h_bar/2.0

    f_u = 0.0
    for i in range(len(freq_list[0])) :
        numerator = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator = numerator + freq_list[j][i]*n   
        pu_bar = numerator/sum(n_list)
        
        numerator1 = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator1 = numerator1 + (freq_list[j][i] - pu_bar)**2*n
        denominator = (len(n_list) - 1.0)/len(n_list)*sum(n_list)
        su2 = numerator1/denominator
        
        bu1 = n_bar/(n_bar - 1.0)
        bu2 = pu_bar*(1 - pu_bar) - su2*(len(n_list) - 1.0)/len(n_list) - h_bar*(2*n_bar - 1.0)/(4*n_bar)
        bu = bu1*bu2
        
        f_u = f_u + (1 - pu_bar)*(1.0 - cu/(bu + cu))
    f_RH = f_u/(len(freq_list[0])-1)
    return f_RH 

#46
def Weir_Cockerham_fW(freq_list, heterozygosity_list, n_list) :

    if len(set([len(freq_list),len(heterozygosity_list) ,len(n_list)])) != 1:
        return False
    for freq in freq_list:
        if round(sum(freq),4) != 1:
            return False
    
    
    import numpy as np
    from itertools import izip
    
    n_bar = sum(n_list)/float(len(n_list))
    n = np.array(n_list)
    n2=sum(n*n)
    nc = (sum(n) - float(n2)/sum(n))/(len(n_list) - 1.0)
    
    numerator = 0.0
    for n in range(len(n_list)) :
        numerator = numerator + heterozygosity_list[n]*n_list[n]
    h_bar = numerator/sum(n_list)
    cu = h_bar/2.0

    f1 = 0.0
    for i in range(len(freq_list[0])) :
        numerator = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator = numerator + freq_list[j][i]*n   
        pu_bar = numerator/sum(n_list)
        
        numerator1 = 0.0
        for j, n in izip(range(len(freq_list)), n_list) :
            numerator1 = numerator1 + (freq_list[j][i] - pu_bar)**2*n
        denominator = (len(n_list) - 1.0)/len(n_list)*sum(n_list)
        su2 = numerator1/denominator
        
        bu1 = n_bar/(n_bar - 1.0)
        bu2 = pu_bar*(1 - pu_bar) - su2*(len(n_list) - 1.0)/len(n_list) - h_bar*(2*n_bar - 1.0)/(4*n_bar)
        bu = bu1*bu2
        
        f1 = f1 + (bu + cu)
    f_w = 1 - 2.0*cu/f1 
    return f_w
        
#47
def Kelly_Zns(S, S_list):

    if S<= 1 or len(S_list)<1:
        return False
    for x in S_list:
        if len(x) != 3:
            return False
    

    def Rij(sub_list):
        Pi = sub_list[0]
        Pj = sub_list[1]
        Pij = sub_list[2]
        Dij = Pij-Pi*Pj

        sub1 = Pi*(1-Pi)*Pj*(1-Pj)

        rij = float(Dij)/sub1**0.5
        return rij

    sub2 = 2.0/(S*(S-1))


    Zns = 0
    for subList in S_list:
        Zns += Rij(subList)

    Zns = sub2*Zns
    return Zns
#48
def Kelly_Za(S, S_list):

    if S<= 1 or len(S_list)<1:
        return False
    for x in S_list:
        if len(x) != 3:
            return False
    

    def Rij(sub_list):
        Pi = sub_list[0]
        Pj = sub_list[1]
        Pij = sub_list[2]
        Dij = Pij-Pi*Pj

        sub1 = Pi*(1-Pi)*Pj*(1-Pj)

        rij = float(Dij)/sub1**0.5
        return rij

    sub2 = 1.0/(S-1)


    Zns = 0
    for subList in S_list:
        Zns += Rij(subList)

    Zns = sub2*Zns
    return Zns

#49
def polymorphism_information_content(a_list):
    if round(sum(a_list),4)!=1:
        return False
    b=0
    for xi in a_list:
        b+=xi**2
        
    m=len(a_list)
    c=0
    for i in range(m-1):
        xi=a_list[i]
        for j in range(i+1,m):
            xj=a_list[j]
            c+=2*xi**2*xj**2
            
    PIC=1-b-c
    return PIC
