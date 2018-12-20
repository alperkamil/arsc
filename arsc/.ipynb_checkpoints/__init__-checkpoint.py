import pywrapfst as fst

def supervisor(MK,P=None,As=None,Aa=None):
    """Synthesizes an attack-resilient supervisor for the plant P, the desired language MK, the sensor attacker As and the actuator attacker Aa.
    
    Parameters
    ----------
    MK : pywrapfst.Fst 
        The FST for the desired language
    P : pywrapfst.Fst, optional
        The FST for the plant
    As : pywrapfst.Fst, optional
        The FST for the sensor attacker
    Aa : pywrapfst.Fst, optional
        The FST for the actuator attacker
    
    Returns
    -------
    S : pywrapfst.Fst 
        The attack-resilient supervisor
    controllable : bool
        True if the desired language is contollable
        
    Examples
    --------
    Examples should be written in doctest format, and should illustrate how
    to use the function.

    >>> import arsc
    >>> MK,P,As,Aa = arsc.example()
    >>> MK
    <vector Fst at 0x2a0a94178f0>
    >>> S, controllable = arsc.supervisor(MK,P,As,Aa)
    >>> S
    <vector Fst at 0x2a0a9417c00>
    >>> controllable
    True
    """
    
    S = MK.copy().arcsort()
    if P:
        S = fst.compose(P.copy().invert().arcsort(),S).arcsort()
    if As:
        S = fst.compose(As.copy().invert().arcsort(),S).arcsort()
    if Aa:
        S = fst.compose(S,Aa.copy().invert().arcsort()).arcsort()
        
        LO = fst.compose(fst.compose(MK.copy().arcsort(),Aa.copy().invert().arcsort()),Aa.copy().arcsort()).arcsort().project(project_output=True)
        LO = fst.determinize(fst.epsnormalize(LO)).minimize().arcsort()
        K = fst.epsnormalize(MK.copy().arcsort().project(project_output=True)).minimize().arcsort()
        controllable = fst.equivalent(LO,K)
    else:
        controllable = True
    
    return S, controllable

def example(n=2,m=2):
    """Generates example plant, model of the desired language, and attackers according to the scheduling problem described in the article.
    You can also find an illustration of the problem in examples/"Scheduling Problem.ipynb"
    
    Parameters
    ----------
    n : int, optional
        The number of players
    m : int, optional
        The number of tasks

    Parameters
    ----------
    MK : pywrapfst.Fst 
        The FST for the desired language
    P : pywrapfst.Fst, optional
        The FST for the plant
    As : pywrapfst.Fst, optional
        The FST for the sensor attacker
    Aa : pywrapfst.Fst, optional
        The FST for the actuator attacker
    """
    
    syms = fst.SymbolTable()
    syms.add_symbol('e')  # Epsilon (empty character)
    for i in range(n):
        for j in range(m):
            sym = 't_'+str(i+1)+str(j+1)
            syms.add_symbol(sym)
    
    P = fst.Fst()
    P.add_state()
    P.set_start(0).set_final(0)
    for k in range(m*n):
        P.add_arc(0,fst.Arc(k+1,k+1,0,0))
    P.set_input_symbols(syms).set_output_symbols(syms).arcsort()

    MK = fst.Fst()
    for k in range((m+1)**n):
        MK.set_final(MK.add_state())
    MK.set_start(0)

    for s in range((m+1)**n):
        q = s
        for d in range(n):
            r = q % (m+1)
            if r < m:
                t = s + (m+1)**d
                l = r + m*d + 1
                MK.add_arc(s,fst.Arc(l,l,0,t))
            q = q // (m+1)

    MK.set_input_symbols(syms).set_output_symbols(syms).arcsort()

    AO = fst.Fst()
    AO.add_state()
    AO.set_final(0).set_start(0)
    for i in range(n):
        for j in range(m):
            il = j + m*i + 1
            ol = il if i else 0
            AO.add_arc(0,fst.Arc(il,ol,0,0))

    AO.set_input_symbols(syms).set_output_symbols(syms).arcsort()

    AI = fst.Fst()
    for s in range((n-1)*m+1):
        AI.add_state()
    #     AI.set_final(AI.add_state())
    AI.set_start(0)
    AI.set_final(0)

    for j in range(m):
        t=j*(n-1)+1
        il = j + 1
        ol = il + m
        AI.add_arc(0,fst.Arc(il,ol,0,t))

        s=t+n-2
        ol = il
        il = j+(n-1)*m+1
        AI.add_arc(s,fst.Arc(il,ol,0,0))

    for s in range(1,(n-1)*m+1):
        if (s-1)%(n-1) != n-2:
            t = s+1
            j=(s-1)//(n-1)
            i=(s-1)%(n-1)+1
            il = j + m*i + 1
            ol = il + m
            AI.add_arc(s,fst.Arc(il,ol,0,t))

    for s in range(0,1): #(n-1)*m+1):
        for i in range(n):
            t = (i+1)%n
            for j in range(m):
                l = j + m*i + 1
                AI.add_arc(s,fst.Arc(l,l,0,s))

    AI = fst.compose(AI,P)
    AI.set_input_symbols(syms).set_output_symbols(syms).arcsort()
    
    return MK, P, AO, AI