import streamlit as st
from router import Router as r

def sideBar():
    with st.sidebar:
        _access_to_upload()
        if st.session_state.accessOk is True :
            _upload_form()

def _access_to_upload() :
    if st.session_state.accessOk is True :
        return
    access = st.empty()
    with access.form('access_form'):
        st.subheader("Enter to upload Form")
        psw = st.text_input('password')
        enter = st.form_submit_button('Submit')
    if enter :
        if psw is not None and psw == '1234' :
            st.session_state.accessOk = True
            access.empty()
        else:
            st.error('Wrong password! Try again..')

def _upload_form():
    st.subheader("documents")
    pdf = st.file_uploader("upload your pdf and click on 'Process'", type="pdf")
    col1, col2 = st.columns(2)

    if col1.button("Check") :
        if pdf is None:
            return st.warning('plz add Pdf')
        with st.spinner("Processing"):
            try:
                files = {"file_pdf": pdf}
                data = {"source" : pdf.name}
                result = r.extract_pdf(file=files, data=data)
                st.write(result)
                st.session_state.checked = True
            except Exception as e:
                st.error('Something went wrong..')
                print(e)

    if col2.button("Save"):
        if st.session_state.checked is False:
            st.warning('Plz check first before save')
            return
        else:
            with st.spinner("Processing"):
                files = {"file_pdf": pdf}
                data = {"source" : pdf.name, "index_name" : "test"}

                result = r.create_pdf(file=files, data=data)
                print(result)
                if result['ok'] == True :
                    st.success('Saved!')
                    st.snow()
                else :
                    st.error('Failed to save :/')