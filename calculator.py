#python module meant to store all calculation algos (to be expanded in future)

def calculate_venn2_sizes(a,b,anb):
    #calculate the sizes of combined regions in a 2-circle Venn diagram, returns them in dictionary

    a_total = a + anb
    b_total = b + anb
    aub = a + b + anb

    result = {"a_total":a_total,"b_total":b_total,"aub":aub}
    return result 

def calculate_venn3_sizes(a,b,c,anb,anc,bnc,anbnc):
    
    #Calculate the sizes of combined region in a 3-circle Venn diagram. returns them in a dictioanry

    #calculate a total, b total, c total
    a_total = a + anb + anc + anbnc 
    b_total = b + anb + bnc + anbnc
    c_total = c + anc + bnc + anbnc
    # aub, auc, buc and aubuc
    aub = a_total + b_total - anb
    auc = a_total + c_total - anc
    buc = b_total + c_total - bnc
    aubuc = a + b + c + anb + anc + bnc + anbnc

    result = {"a_total":a_total,"b_total":b_total,"c_total":c_total,"aub":aub,"auc":auc,"buc":buc,"aubuc":aubuc}
    return result