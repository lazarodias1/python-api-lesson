import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variáveis que guardam os resultados durante a sessão
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iterations', 'mean']
    )

st.header('Jogando uma moeda')

chart_placeholder = st.empty()

def toss_coin(n):

    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0
    means = [0.5]

    for r in trial_outcomes:
        outcome_no += 1

        if r == 1:
            outcome_1_count += 1

        mean = outcome_1_count / outcome_no
        means.append(mean)

        chart_placeholder.line_chart(pd.DataFrame({'mean': means}))
        time.sleep(0.05)

    return mean

chart_placeholder.line_chart(pd.DataFrame({'mean': [0.5]}))

number_of_trials = st.slider('Número de tentativas?', 1, 1000, 10)
start_button = st.button('Executar')

if start_button:
    st.write(f'Executando o experimento de {number_of_trials} tentativas.')

    st.session_state['experiment_no'] += 1

    mean = toss_coin(number_of_trials)

    new_result = pd.DataFrame(
        data=[[
            st.session_state['experiment_no'],
            number_of_trials,
            mean
        ]],
        columns=['no', 'iterations', 'mean']
    )

    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], new_result],
        ignore_index=True
    )

st.write(st.session_state['df_experiment_results'])