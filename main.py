import streamlit as st
import pandas as pd
import utils
from st_aggrid import AgGrid, GridOptionsBuilder
navec = utils.load_navec('navec_hudlit_v1_12B_500K_300d_100q.tar')
words = utils.load_words('words.txt')
masked_text = '████████████████'

if 'distances' not in st.session_state:
  st.session_state.distances = None
if 'keyword' not in st.session_state:
  st.session_state.keyword = None
if 'data' not in st.session_state:
  st.session_state.data = []
if 'text_visible' not in st.session_state:
    st.session_state.text_visible = False

# Define a function to apply colors based on distance
def color_row(row):
    distance = row['Расстояние']
    if distance < 1000:
        return ['background-color: green'] * len(row)
    elif 1000 <= distance < 5000:
        return ['background-color: yellow'] * len(row)
    else:
        return ['background-color: red'] * len(row)


def add_data(text):
    
    index = utils.check_number(text, st.session_state.distances)
    if index==-1:
        st.warning('Этого слова нет в словаре')
    elif index==0:
        st.success('Поздравляю, вы угадали слово')
    else:
        st.session_state.data.append({"Слово": text, "Расстояние": index})


if st.sidebar.button("Сгенерировать слово"):
    st.session_state.data = []
    st.session_state.keyword = utils.sample_word(words)
    st.session_state.distances = utils.get_distances(st.session_state.keyword,words,navec)
    
st.title("Угадай Слово!")

text_input = st.text_input("Введите слово", key="text_input")

if st.button("Отправить"):
    if text_input:
        add_data(text_input)
    else:
        st.warning("Пожалуйста, введите слово.")

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    df = df.sort_values(by='Расстояние')
    #df = df.set_index('Слово')
    df = df.style.apply(color_row, axis=1)
    st.table(df)

if st.sidebar.button("Показать/Скрыть текст"):
    st.session_state.text_visible = not st.session_state.text_visible

if st.session_state.text_visible:
    st.sidebar.write(st.session_state.keyword)
else:
    st.sidebar.write(masked_text)