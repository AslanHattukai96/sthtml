import streamlit as st

@st.cache_data(show_spinner=False)
def append_list(num_iterations):
    with st.spinner('This might take awhile...'):
        mylist = []
        with st.empty():
            for i in range(num_iterations):
                st.write(f"Iteration number is {i}")
                mylist.append(i)
    return mylist

output = append_list(10000)
selection = st.selectbox('Make a selection', ['Good','Bad'])
if selection == 'Good':
    st.write('You selected Good')
else:
    st.write('You selected Bad')