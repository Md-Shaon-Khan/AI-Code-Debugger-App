import streamlit as st 
import pandas as pd
import numpy as np
from PIL import Image
from solution import solution_master

st.title("Shaon Code Debugger App")
st.divider()

with st.sidebar.container():
  # st.markdown("Upload Code images")
  images = st.file_uploader("Upload your error's code...",type=['png','jpg','jpeg'],accept_multiple_files=True)
  
  pil_images = []
  
  for img in images:
    pil_img = Image.open(img)
    pil_images.append(pil_img)
    
  length = len(images)
  if images:
    if length > 2:
       st.error("Shaon can accept maximum 2 images only.")
    else:
      cols = st.columns(length)
      
      for i in range(length):
        with cols[i]:
          st.image(images[i])
    
  selected_option = st.selectbox("What you want...",('Hints','Solution'),index=None)
  
  
  pressed = st.button("Submit",type="secondary")
  

if pressed:
  if not images:
    st.error("You have to upload at least one image")
  if not selected_option:
    st.error("You have to select either Hints or Solution")
  
  if images and selected_option:
    with st.container(border=True):
      st.header(f"Your {selected_option} provided by Shaon Sir")
      
    with st.spinner("Shaon is following your command, please wait..."):
      generate_solution = solution_master(pil_images,selected_option)
      
      st.markdown(generate_solution)