import pgmpy
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianModel
from pgmpy.readwrite import BIFWriter
import os


def create_bayes_net():
    model = BayesianModel([('os','ttl'),('os','winsize'),('os','nop'),('os','mss'),('mss','wsc')])
    os_cpd = TabularCPD(variable = 'os', variable_card =3, values = [[0.47],[0.41],[0.12]])
    ttl_cpd = TabularCPD(variable = 'ttl', variable_card =3, \
                                values= [[0.010,0.97,0.83],
                                        [0.99,0,0], 
                                        [0,0.03,0.17]], 
                                        evidence = ['os'], evidence_card=[3])
    win_cpd = TabularCPD(variable = 'winsize', variable_card =4, \
                                values= [[.09,.2,0.48],[0.30,0.13,0],
                                        [0.45,0.47,0], 
                                        [0.16,0.2,0.52]], 
                                        evidence = ['os'], evidence_card=[3])
    mss_cpd = TabularCPD(variable = 'mss', variable_card =2, \
                                values= [[0.053,0.04,0.03],
                                        [0.947,0.96,0.97]],
                                        evidence = ['os'], evidence_card=[3])
    nop_cpd = TabularCPD(variable = 'nop', variable_card =2, \
                                values= [[0.17,0.68,0.46],
                                        [0.83,0.32,0.54]],
                                        evidence = ['os'], evidence_card=[3])
    wsc_cpd = TabularCPD(variable = 'wsc', variable_card =2, 
                                values= [[0.99,0.01],
                                        [0.01,0.99]],
                                        evidence = ['mss'], evidence_card=[2])

    model.add_cpds(os_cpd, ttl_cpd, win_cpd, mss_cpd, wsc_cpd, nop_cpd)
    return model


if __name__ == "__main__":
    cwd = os.getcwd()
    path = os.path.dirname(cwd)
    db_path = 'bayes_model_KB'
    filename = "bayes_net_KB.bif"
    target = os.path.join(os.path.join(path, db_path), filename)
    model = create_bayes_net()
    model_data = BIFWriter(model)
    model_data.write_bif(target)
