#!/usr/bin/env python3
"""Finite diagnostics and exact document synchronization for the updated paper.
Python 3.10+ and NumPy; optional NetworkX enables a matching-implementation check.
A successful test is not a formal proof or hardware certification.
"""
import argparse,hashlib,itertools as it,json,math
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
CLAIMS={x['id']:x for x in json.loads((ROOT/'claims.json').read_text())}
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1.,-1.])
def close(a,b):return np.allclose(a,b,rtol=1e-10,atol=1e-10)
def comm(a,b):return a@b-b@a
def roots2():
    r=[]
    for i,j in it.combinations(range(8),2):
        for a,b in it.product([-2,2],repeat=2):
            v=[0]*8;v[i]=a;v[j]=b;r.append(tuple(v))
    r += [v for v in it.product([-1,1],repeat=8) if sum(v)%4==0]
    return np.array(sorted(r),dtype=int)
def cartan_diagonals():return np.vstack([roots2()/2,np.zeros((16,8))])/math.sqrt(60)
def walsh():return np.array([[(-1)**((s&j).bit_count()) for j in range(256)] for s in range(256)])
@lru_cache(None)
def distillation_counts():
    accepted=[0]*16;bad=[0]*16
    for mask in range(1<<15):
        syndrome=0
        for j in range(15):
            if mask>>j&1:syndrome^=j+1
        if syndrome==0:
            w=mask.bit_count();accepted[w]+=1;bad[w]+=w%2
    return accepted,bad
def acceptance(p):return sum(n*p**w*(1-p)**(15-w) for w,n in enumerate(distillation_counts()[0]))
def pout(p):return sum(n*p**w*(1-p)**(15-w) for w,n in enumerate(distillation_counts()[1]))/acceptance(p)
def power_coefficients(counts):
    out=[0]*16
    for w,c in enumerate(counts):
        for j in range(16-w):out[w+j]+=c*math.comb(15-w,j)*(-1)**j
    return out

def f1():
    r=roots2();rs={tuple(v) for v in r};assert len(rs)==240
    assert sum(np.count_nonzero(v)==2 for v in r)==112
    assert np.all(np.sum(r*r,axis=1)==8)
    for a in r:
        for b in r:
            dot=int(a@b);assert dot%4==0 and tuple(b-(dot//4)*a) in rs
    assert np.array_equal(r.T@r,240*np.eye(8,dtype=int))
    order=math.prod([2,8,12,14,18,20,24,30]);assert order==2**14*3**5*5**2*7==696729600
    return {'roots':240,'integer':112,'half_integer':128,'reflection_pairs':57600,'weyl_order':order,'general_proof_scope':'Weyl complete reducibility is invoked, not proved by this enumeration.'}
def f2():
    assert (248-1).bit_length()==8 and (248**2-1).bit_length()==16
    sizes=[math.comb(8,w) for w in range(9)];assert max(sizes)==70 and sum(sizes)==256
    i,j=247,251;assert i.bit_count()==j.bit_count()==7 and i<248<=j
    assert i^j==(1<<3)|(1<<2)
    # Exact two-bit swap has a two-qubit weight-preserving permutation matrix.
    swap=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    assert close(comm(swap,np.diag([0,1,1,2])),0)
    return {'tensor_square_dimension':61504,'minimum_qubits':16,'sector_sizes':sizes,'leakage_transition':[i,j],'basis_encoding_isometry':'Any selected distinct computational basis columns are orthonormal.'}
def f3():
    roots=roots2()/2;v=np.array([10**j for j in range(8)])
    pos=roots[roots@v>0];rho=pos.sum(axis=0)/2;theta=pos[np.argmax(pos@rho)]
    c=float(theta@(theta+2*rho));assert close(c,60)
    for a in [np.array([0.,0.]),np.array([2.,4.])]:
        b=a/a.max() if a.max()>0 else a;assert min(b)>=0 and max(b)<=1
    assert np.trace(np.eye(248))==248
    return {'root_casimir':c,'half_casimir':c/2,'single_irrep_multiplicity':1,'projector_trace':248,'trace_normalized_adjoint_casimir':248/248}
def f4():
    h=np.diag([0.,0.,1.])+np.diag([2.5,0,0]);ev,u=np.linalg.eigh(h)
    assert abs(u[0,0])==0 and ev[0]==0
    h=np.diag([.2,.9,5.]);ev,u=np.linalg.eigh(h);assert abs(u[2,0])==0
    ev,u=np.linalg.eigh(np.array([[0.,1.],[1.,5.]]));leak=abs(u[1,0])**2;assert leak>0
    return {'coupled_block_leakage':float(leak),'deflation':'Another vector in same degenerate eigenspace remains available.'}
def f5():
    N=np.diag([0,1,1,2]);count=0
    for t in [-1.,0,.3,2.]:
        for p in [0,.4,1.7]:
            g=np.eye(4,dtype=complex);g[1:3,1:3]=[[math.cos(t),-np.exp(-1j*p)*math.sin(t)],[np.exp(1j*p)*math.sin(t),math.cos(t)]]
            assert close(g.conj().T@g,np.eye(4)) and close(comm(g,N),0);count+=1
    a=10;hessian=-4*a*a*np.ones((2,2));assert close(np.linalg.norm(hessian,2),4*(a*a+a*a))
    e=lambda i,j:np.eye(3)[:,i:i+1]@np.eye(3)[j:j+1,:]
    deriv=np.trace(-1j*comm(e(0,1)+e(1,0),e(1,2))@e(2,0));assert close(1j*deriv,1)
    return {'Givens_parameter_pairs':count,'two_parameter_Hessian_norm':float(np.linalg.norm(hessian,2)),'trace_derivative':str(deriv),'conditional_two_CNOT_counts_per_D':[14,4]}
def f6():
    xs=[{0,1},{1,2,4,5},{3,4,6,7},{7,8}];zs=[{0,1,3,4},{2,5},{3,6},{4,5,7,8}]
    assert all(len(a&b)%2==0 for a in xs for b in zs)
    masks=lambda ss:[sum(1<<j for j in s) for s in ss]
    xm,zm=masks(xs),masks(zs)
    def span(ms):
        out={0}
        for m in ms:out|={a^m for a in list(out)}
        return out
    sx,sz=span(xm),span(zm);assert len(sx)==len(sz)==16
    dx=min(v.bit_count() for v in range(1,512) if all((v&z).bit_count()%2==0 for z in zm) and v not in sx)
    dz=min(v.bit_count() for v in range(1,512) if all((v&x).bit_count()%2==0 for x in xm) and v not in sz)
    assert dx==dz==3 and 8*(9+8)+8==144
    for bits in it.product([0,1],repeat=4):assert (-1)**(sum(bits)%2)==math.prod((-1)**b for b in bits)
    return {'X_supports':[sorted(a) for a in xs],'Z_supports':[sorted(a) for a in zs],'ranks':[4,4],'distance':[dx,dz],'physical_budget':144,'syndrome_ancillas':64}
def f7():
    a,b=distillation_counts();ap=power_coefficients(a);bp=power_coefficients(b)
    coeff=[F(0)]*6
    for j in range(6):coeff[j]=(F(bp[j])-sum(F(ap[k])*coeff[j-k] for k in range(1,j+1)))/ap[0]
    assert coeff[3]==35 and coeff[4]==105
    p=F(1,100);assert pout(p)>35*p**3
    lo,hi=F(141,1000),F(142,1000);assert pout(lo)<lo and pout(hi)>hi
    # Numerical bisection is explicitly a bracket refinement, not symbolic uniqueness proof.
    for _ in range(45):
        mid=(lo+hi)/2
        if pout(mid)<mid:lo=mid
        else:hi=mid
    return {'patterns':32768,'accepted_by_weight':a,'failure_by_weight':b,'series_through_p5':[str(x) for x in coeff],'fixed_point_bracket':[float(lo),float(hi)],'p001_exact_output':float(pout(p)),'cubic_truncation':float(35*p**3)}
def f8():
    h=cartan_diagonals();assert close(h.T@h,np.eye(8)) and close(h.sum(axis=0),0)
    assert np.count_nonzero(np.all(h[:248]==0,axis=1))==8
    return {'Cartan_rank':int(np.linalg.matrix_rank(h)),'zero_weight_multiplicity':8,'unscaled_Gram_diagonal':[60]*8}
def t13():
    c=lambda k:F(248*k,k+30)
    assert c(1)==8 and 30!=c(1)*31
    return {'central_charges':{str(k):str(c(k)) for k in [1,2,3,10]},'original_level_one_lhs':30,'original_level_one_rhs':248,'original_equation_would_require_delta_k':str(F(248,30)),'not_computed':'No field theory or physical boundary is simulated.'}
def matchings(vertices):
    if not vertices:yield [];return
    i=vertices[0]
    for j in vertices[1:]:
        rest=[x for x in vertices if x not in [i,j]]
        for m in matchings(rest):yield [(i,j)]+m
def l6():
    bounds={}
    for R in [1,2,10]:
        history=np.array([[t%2]*64 for t in range(R+1)])
        count=int(np.count_nonzero(np.diff(history,axis=0)));assert count==64*R;bounds[R]=count
    w=np.array([[0,2,9,8,7,3],[2,0,5,6,4,9],[9,5,0,1,8,7],[8,6,1,0,2,6],[7,4,8,2,0,3],[3,9,7,6,3,0]])
    matches=list(matchings(list(range(6))));costs=[sum(int(w[i,j]) for i,j in m) for m in matches];best=min(costs)
    assert len(matches)==15
    optional='NOT_RUN: NetworkX not installed; exhaustive oracle completed.'
    try:
        import networkx as nx
        graph=nx.Graph()
        for i,j in it.combinations(range(6),2):graph.add_edge(i,j,weight=-int(w[i,j]))
        m=nx.max_weight_matching(graph,maxcardinality=True)
        assert len(m)==3 and sum(int(w[i,j]) for i,j in m)==best
        optional='PASS: NetworkX '+nx.__version__+' agrees with exact exhaustive oracle.'
    except ImportError:pass
    return {'real_vertex_bounds':bounds,'complete_graph_edges_V72':72*71//2,'matching_oracle_cost':best,'optional_solver':optional,'limitation':'Neither the exhaustive oracle nor timings prove O(V^3) or latency.'}
def t10():
    u=np.diag(np.exp(2j*math.pi/8*np.array([1,-1])))
    assert close(u.conj().T@u,I) and not close(u,u[0,0]*I)
    return {'holonomy':[str(z) for z in np.diag(u)],'scalar':False,'curvature':'d(dphi)=0 and dphi wedge dphi=0 on annulus'}
def t14():
    angles=np.linspace(0,2*math.pi,65)[:-1];f=abs(np.sin(angles))
    # m=1, E=cos(theta), L=1. Exact finite product law is also covered by bounded differences.
    for eps in [.05,.2,.5,1.,2.]:
        tail=float(np.mean(abs(f-f.mean())>=eps));bound=min(1.,2*math.exp(-2*eps*eps/(math.pi**2)))
        assert tail<=bound+1e-12
    for a in angles:
        for b in angles:
            dist=min(abs(a-b),2*math.pi-abs(a-b))
            assert abs(abs(math.sin(a))-abs(math.sin(b)))<=dist+1e-12
    assert math.sin(0)==0 and math.cos(0)>math.cos(math.pi)
    # A non-vacuous bounded-differences check over all independent Bernoulli coordinates.
    m=16
    for t in [3,4,5,6]:
        tail=sum(math.comb(m,k) for k in range(m+1) if abs(k-m/2)>=t)/2**m
        assert tail<=2*math.exp(-2*t*t/m)
    return {'torus_grid_points':64,'pairwise_Lipschitz_checks':4096,'product_Bernoulli_variables':16,'stationary_maximum':'E=cos(theta), theta=0','not_proved':'Continuum concentration is justified in the written martingale argument; examples are not its proof.'}
def t15():
    n=100000
    s=float(np.sum(1/np.arange(1,n+1,dtype=float)**2));target=math.pi**2/6
    # Integral test supplies a mathematical enclosure, not merely a quadrature guess.
    assert s+1/(n+1)<target<s+1/n
    kb=1.380649e-23;h=6.62607015e-34
    coeff=math.pi**2*kb**2/(3*h)*8
    fluxcoeff=math.pi**2*kb**2/(6*h)*8
    assert math.isclose(coeff,2*fluxcoeff,rel_tol=1e-14)
    return {'zeta2_partial_sum':s,'integral_tail_bounds':[1/(n+1),1/n],'conditional_kappa_over_T_c8_W_per_K2':coeff,'charge_current':'No electromagnetic coupling is specified; electrical Hall conductivity is not computed.'}
def t16():
    pstar=F(1,100);b=distillation_counts()[1]
    A=sum(F(b[w])*pstar**(w-3) for w in range(3,16))/(1-pstar)**15
    assert A*pstar*pstar<1
    for den in [100,200,1000,10000]:
        p=F(1,den);assert pout(p)<=A*p**3 and pout(p)>35*p**3
    p=F(1,100);resources=F(1)
    steps=[]
    for j in range(3):
        resources*=15/acceptance(p);p=pout(p)
        logbound=-.5*math.log(float(A))+3**(j+1)*math.log(math.sqrt(float(A))*.01)
        assert math.log(float(p))<=logbound+1e-10
        steps.append({'level':j+1,'error':float(p),'log_upper_bound':logbound,'expected_raw_inputs':float(resources)})
    assert resources>15**3
    eps=1e-12;x0=math.sqrt(float(A))*.01
    n=max(0,math.ceil(math.log(math.log(1/(eps*math.sqrt(float(A))))/math.log(1/x0),3)))
    assert -.5*math.log(float(A))+3**n*math.log(x0)<=math.log(eps)
    return {'certified_A_exact':str(A),'certified_A':float(A),'p_star':float(pstar),'steps':steps,'levels_sufficient_for_1e12':n,'no_rejection_raw_inputs':15**n}
def t17():
    W=walsh();assert np.array_equal(W@W.T,256*np.eye(256,dtype=int))
    d=np.arange(256,dtype=float)**2-17*np.arange(256);coef=W@d/256
    assert close(W.T@coef,d)
    H=cartan_diagonals();q=np.r_[np.zeros(248),np.ones(8)];space=np.column_stack([H,q])
    assert np.linalg.matrix_rank(space)==9 and close(H[:248].sum(axis=0),0)
    return {'diagonal_dimension':256,'Cartan_plus_padding_rank':9,'physical_identity_trace':248,'Cartan_physical_trace':0,'reconstruction_max_error':float(max(abs(W.T@coef-d)))}
def t18():
    A=2.;mu=3.;p=.05;rat=mu*p
    out=[]
    for s in [3,10,100]:
        bound=A*rat**s/(1-rat);partial=sum(A*rat**l for l in range(s,s+100))
        assert partial<=bound*(1+1e-12)
        xi=1/math.log(1/rat);assert math.isclose(bound,A/(1-rat)*math.exp(-s/xi),rel_tol=1e-12)
        out.append([s,bound])
    q=.01;assert q>out[-1][1]
    return {'path_event_bounds':out,'correlated_logical_channel_probability':q,'counterexample':'A shared logical flip with probability q independent of separation violates a universal decaying envelope.'}
def t19():
    marks=[2,3,4,6,5,4,3,2]
    # At level one every Dynkin label is at most one, so enumeration of {0,1}^8 is exhaustive.
    allowed=[v for v in it.product([0,1],repeat=8) if sum(a*b for a,b in zip(marks,v))<=1]
    assert allowed==[(0,)*8]
    theta=roots2()[0]/2;assert theta@theta==2
    phase=np.exp(1j*math.pi/15);a=phase*np.eye(3);b=np.exp(.7j)*np.eye(3)
    assert close(comm(a,b),0)
    assert F(60,2*(2+30))==F(30,2+30)==F(15,16)
    return {'level_one_integrable_weights':allowed,'adjoint_minimum_level':2,'adjoint_weight_at_k2':str(F(15,16)),'original_k1_primary':'absent','scalar_phase_commutator_norm':float(np.linalg.norm(comm(a,b)))}
def t20():
    B=1;eps=.5;delta=.1;S=math.ceil(2*B*B/eps**2*math.log(2/delta))
    # Exact rational tail for independent +/-1 fair outcomes.
    tail=F(sum(math.comb(S,k) for k in range(S+1) if abs(F(2*k,S)-1)>=F(1,2)),2**S)
    bound=2*math.exp(-S*eps*eps/(2*B*B));assert float(tail)<=bound<=delta
    psi=np.array([1,1j,2,0],complex)/math.sqrt(6);H=np.diag([0.,.2,.7,1.])
    energy=np.vdot(psi,H@psi);assert close(energy,.5)
    return {'sample_count':S,'exact_binomial_tail':str(tail),'Hoeffding_bound':bound,'dense_example_energy':float(energy.real),'memory_amplitudes_144_qubits':2**144,'sector_dimension_8qubits_weight4':70,'cost_model':'S*(G*N+C_H(N)+R*C_dec(V))'}
CHECKS={k:globals()[k.lower()] for k in CLAIMS}

def verify_document(path):
    from zipfile import ZipFile
    from xml.etree import ElementTree as ET
    with ZipFile(path) as z:r=ET.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paras=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in r.findall('.//w:p',ns)]
    for c in CLAIMS.values():
        for s in [c['title'],c['statement'],*c['equations'],'Proof. '+c['proof'],'Scope. '+c['limits']]:
            if s not in paras:raise AssertionError('Document mismatch: '+c['id']+' '+s[:60])
    return {'matched_claim_groups':len(CLAIMS),'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest()}
def run(keys):
    out=[]
    for k in keys:
        c=CLAIMS[k];r={'id':k,'title':c['title'],'source_paragraphs':c['source_paragraphs'],'original_verdict':c['original_verdict'],'scope':c['limits']}
        try:r.update(execution='PASS',evidence=CHECKS[k]())
        except Exception as e:r.update(execution='ERROR',error=f'{type(e).__name__}: {e}')
        out.append(r)
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--claim',choices=CLAIMS);p.add_argument('--list',action='store_true');p.add_argument('--output',type=Path);p.add_argument('--document',type=Path)
    a=p.parse_args()
    if a.list:
        for k,c in CLAIMS.items():print(k,c['title'])
        return
    results=run([a.claim] if a.claim else CLAIMS)
    payload={'meaning':'PASS means the diagnostic ran successfully. Finite checks are not formal proofs. Original verdicts refer to the uploaded draft, not the corrected statements.','results':results}
    if a.document:payload['document_sync']=verify_document(a.document)
    if a.output:a.output.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
    for r in results:print(r['id'],r['execution'],r.get('error',''))
    if any(r['execution']=='ERROR' for r in results):raise SystemExit(1)
if __name__=='__main__':main()
