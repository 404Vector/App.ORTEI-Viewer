from io import BytesIO
from typing import Any
import streamlit as st
import pandas as pd
import numpy as np
import json

def convert_jsonbuffer2dict(json_buffer:BytesIO | None) -> dict | None:
    if json_buffer == None:
        return None
    buffer:bytes = json_buffer.getvalue()
    return json.loads(buffer)

def render_content_text(key, text):
    columns = st.columns(2)
    with columns[0]:
        st.markdown(f"***{key}***")
    with columns[1]:
        st.markdown(f"{text}")
    return None

def render_content_listdict(key, listdict):
    df = pd.DataFrame(listdict)
    st.markdown(f"***{key}***")
    state_key = f"_{key}_selectbox_"
    st.selectbox("Select the display item", ["summary", "sheet", *listdict[0]], index=0, key=state_key, label_visibility="visible")
    display = st.session_state[state_key]
    if display == "summary":
        summary = df.describe(percentiles=[0.5])
        cols = [c for c in summary.columns]
        indexs = [i for i in summary.index if i is not 'count']
        values = summary.values
        is_render_each = st.checkbox("show each graph", False)
        if is_render_each:
            for idx_key in indexs:
                st.text(idx_key)
                st.area_chart(summary.T.get(idx_key))
        else:
            st.line_chart(summary.T.get(indexs))
            st.dataframe(summary)

    elif display == "sheet":
        st.dataframe(df)
    else:
        st.area_chart(df[display])

def render_content(key:str, item:Any):
    item_type = type(item)
    if item_type is str:
        return render_content_text(key, item)
    if item_type is int:
        return render_content_text(key, item)
    if item_type is float:
        return render_content_text(key, item)
    if item_type is list:
        if len(item) > 0 and type(item[0]) is dict:
            return render_content_listdict(key, item)
        
    return st.text(f"Error::Not supported Object | key = {key} | type = {item_type} | obj = {item}")
    

def render():
    st.set_page_config(
        page_title="ORTEI - Viewer", 
        page_icon="🧊", 
        layout="centered", 
        initial_sidebar_state="auto", 
        menu_items=None)
    st.file_uploader("Upload evaluation result(json)", type='.json', accept_multiple_files=False, key="json_file")
    if st.session_state["json_file"] is not None:
        st.divider()
        context_data = convert_jsonbuffer2dict(st.session_state["json_file"])
        for key in context_data:
            render_content(key, context_data[key])
    
if __name__ == "__main__":
    render()