from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

model = DiscreteBayesianNetwork([
    ('Disease', 'Fever'),
    ('Disease', 'Cough'),
    ('Disease', 'Fatigue'),
    ('Disease', 'Chills')  
])

cpd_disease = TabularCPD(variable='Disease', variable_card=2, 
                         values=[[0.6], [0.4]],
                         state_names={'Disease': ['Cold', 'Flu']})

cpd_fever = TabularCPD(variable='Fever', variable_card=2,
                       values=[[0.8, 0.3],
                               [0.2, 0.7]],
                       evidence=['Disease'], evidence_card=[2],
                       state_names={'Fever': ['No', 'Yes'], 'Disease': ['Cold', 'Flu']})

cpd_cough = TabularCPD(variable='Cough', variable_card=2,
                       values=[[0.3, 0.2],
                               [0.7, 0.8]],
                       evidence=['Disease'], evidence_card=[2],
                       state_names={'Cough': ['No', 'Yes'], 'Disease': ['Cold', 'Flu']})

cpd_fatigue = TabularCPD(variable='Fatigue', variable_card=2,
                         values=[[0.6, 0.3],
                                 [0.4, 0.7]],
                         evidence=['Disease'], evidence_card=[2],
                         state_names={'Fatigue': ['No', 'Yes'], 'Disease': ['Cold', 'Flu']})

cpd_chills = TabularCPD(variable='Chills', variable_card=2,
                        values=[[0.9, 0.4],
                                [0.1, 0.6]],
                        evidence=['Disease'], evidence_card=[2],
                        state_names={'Chills': ['No', 'Yes'], 'Disease': ['Cold', 'Flu']})

model.add_cpds(cpd_disease, cpd_fever, cpd_cough, cpd_fatigue, cpd_chills)

infer = VariableElimination(model)

posterior_1 = infer.query(variables=['Disease'], evidence={'Fever': 'Yes', 'Cough': 'Yes'})

print("Posterior with Fever and Cough:\n", posterior_1)

posterior_2 = infer.query(variables=['Disease'], evidence={'Fever': 'Yes', 'Cough': 'Yes', 'Chills': 'Yes'})

print("\nPosterior with Fever, Cough, and Chills:\n", posterior_2)

fatigue_given_flu = infer.query(variables=['Fatigue'], evidence={'Disease': 'Flu'})

print("\nP(Fatigue | Disease=Flu):\n", fatigue_given_flu)
