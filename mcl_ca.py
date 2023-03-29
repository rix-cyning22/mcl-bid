# -*- coding: utf-8 -*-
"""mcl-ca.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pEPodtUKMgzMdepDYfTPDBlum6TkyuTy
"""

# installing the libraries required
# colab supports pip. but it may not run in your system
# you have to install these libraries in your system, else the code will not work

# we are converting each page of the scanned pdf into an image (jpeg or png) using pdf2img()
# then extracting the text from each image using extract_text()
# then, we are finding the pan number by checking for the format using getPAN()

import mcl_utils as mclu

import re
import pandas as pd

def extract_from_CA(filepath):
  filetext = mclu.extract_text(filepath, endpg=1)
  ca = mclu.get_answer(filetext, "name of the CA firm")
  ca = re.findall(r'"([^"]*)"', ca)[0]

  udin = re.findall(r"UDIN[:; -]*([0-9A-Z ]*)", filetext)[0].replace(" ", "")
  
  audited = mclu.get_answer(filetext, "name of the company audited")
  audited = re.findall(r'"([^"]*)"', audited)[0]

  turnover = re.findall(r"20[\d][\d][ ]*-[ ]*20[\d][\d][ ]*([0-9.]+[,]?[0-9.]*)[ ]*", filetext)
  year = re.findall(r"(20[\d][\d][ ]*-[ ]*20[\d][\d])[ ]*[0-9.]+[ ]*", filetext)
  relevant_work = pd.DataFrame({"Financial Year": year,
                                "Gross Turn Over": turnover})
  relevant_work["Gross Turn Over"] = relevant_work["Gross Turn Over"].str.replace(",", "")
  relevant_work["Gross Turn Over"] = relevant_work["Gross Turn Over"].astype("float64")
  work_type = mclu.get_answer(filetext, "type of work done by the company audited by " + ca)
  work_type = re.findall(r'"([^"]*)"', work_type)[0]
  info_extracted = {
      "CA Name": ca,
      "UDIN No.": udin,
      "Company audited": audited,
      "Relevant Work Experience": relevant_work,
      "Type of work done": work_type
  }
  return info_extracted

filepath = "D:\\CV\\Project\\MCL\\Govind Files\\civil data1\\CACERTIFICATE1920.pdf"

info = extract_from_CA(filepath)
print(info)