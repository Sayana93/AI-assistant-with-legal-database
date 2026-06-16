import streamlit as st
from gigachat import GigaChat
import PyPDF2
AUTH_DATA = "MDE5ZDk0ZDgtZTg2Yy03MmM0LTg5M2EtZTQzZDFjYmU1NmE0OmFmMDlkNTNlLWUwMWQtNGEyZS05NDEwLTcwODhiODA4M2Y5OQ=="

st.set_page_config(page_title="ИИ-Помощник Служащего", page_icon="📝")
st.title("🤖 Ассистент муниципального служащего")
st.write("Генерация официальных ответов на базе GigaChat")

# Интерфейс в сайдбаре
with st.sidebar:
    st.header("Настройки")
    doc_type = st.selectbox("Тип документа", 
                            ["Заявление гражданина", "Ответ на требование прокуратуры", "Служебная записка", "Ходатайство"])
    #ДОБАВЛЕНИЕ: Загрузка файла
    uploaded_file = st.file_uploader("+", "pdf")
user_text = st.text_area("Введите краткую суть дела:", 
                         placeholder="Например: Прокурорская проверка по факту нарушения сроков...")

if st.button("Сгенерировать ответ"):
    if user_text:
        with st.spinner('ИИ-юрист составляет документ...'):
            try:
                # Используем правильную переменную AUTH_DATA
                with GigaChat(credentials=AUTH_DATA, verify_ssl_certs=False, timeout=60) as giga:
                    system_role = "Вы — опытный юрист и муниципальный служащий. Пишете в строгом официально-деловом стиле."
                    
                    # Формируем запрос
                    prompt = (f"Напиши проект официального документа: {doc_type}.\n"
                              f"Суть дела: {user_text}.\n"
                              f"Обязательно используй обороты: 'согласно постановлению и распоряжению', "
                              f"'в установленный срок', 'доводы приняты'.")
                    
                    # Отправляем как единый запрос (или используйте структуру ролей)
                    response = giga.chat(f"{system_role}\n\n{prompt}")
           
                    st.subheader("Результат:")
                    st.write(response.choices[0].message.content)
                    st.success("Готово!")
            except Exception as e:
                st.error(f"Ошибка подключения: {e}")
    else:
        st.warning("Пожалуйста, введите суть дела.")
# Добавляем обработку загруженного файла
if uploaded_file is not None:
    try:
        # 1. Читаем текст из PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        # 2. Кнопка для анализа
        if st.button("Проанализировать загруженный PDF"):
            with st.spinner("ИИ изучает документ..."):
                # Формируем запрос к нейросети на основе текста из файла
                file_prompt = f"Проанализируй этот документ и напиши проект официального ответа: {pdf_text}"
               
                # Используем вашу функцию или прямой вызов GigaChat
                with GigaChat(credentials=AUTH_DATA, verify_ssl_certs=False) as giga:
                    res = giga.chat(file_prompt)
                    st.subheader("Проект ответа по файлу:")
                    st.write(res.choices[0].message.content)
                    st.success("Готово!")
    except Exception as e:
        st.error(f"Не удалось прочитать PDF: {e}")
    