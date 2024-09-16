import streamlit as st
import streamlit as st
import os
import tempfile
import datetime
from aadhar import process_aadhar
from income import process_income
from gate import process_gate
import Levenshtein

# Streamlit Form
st.title("  DRDO - Registration Form")
if "name" not in st.session_state:
        st.session_state["name"] = ""
if "an" not in st.session_state:
        st.session_state["an"] = ""
if "adob" not in st.session_state:
        st.session_state["adob"] = ''
if "dob" not in st.session_state:
        st.session_state["dob"] = ""
if "aadhar" not in st.session_state:
        st.session_state["aadhar"] = ""
if "f" not in st.session_state:
        st.session_state["f"] = "" 
if "af" not in st.session_state:
        st.session_state["af"] = "" 
if "mob" not in st.session_state:
        st.session_state["mob"] = ""
if "gen" not in st.session_state:
        st.session_state["gen"] = ""
if "agen" not in st.session_state:
        st.session_state["agen"] = ""
if "income" not in st.session_state:
        st.session_state["income"] = ""
if "inc_number" not in st.session_state:
        st.session_state["inc_number"] = ""
if "previous_file" not in st.session_state:
    st.session_state["previous_file"] = None
if "income_file" not in st.session_state:
    st.session_state["income_file"] = None
if "gate_file" not in st.session_state:
    st.session_state["gate_file"] = None
if "gate" not in st.session_state:
    st.session_state["gate"] = ''
if "gate_mark" not in st.session_state:
    st.session_state["gate_mark"] = ''
if "age" not in st.session_state:
    st.session_state["age"] = ''
if "nv" not in st.session_state:
    st.session_state["nv"] = ''
if "nv" not in st.session_state:
    st.session_state["nv"] = ''
# Name
name = st.text_input("Full Name:",value=st.session_state["name"])
if st.session_state['an'] !='':
     st.warning(st.session_state['an'])
# Date of Birth

dob = st.date_input("Date of Birth:",min_value=datetime.date(1900,1,1))
if st.session_state['adob'] !='':
     st.warning(st.session_state['adob'])
age=st.text_input("Age:", value=st.session_state['age'], disabled=True)
# Gender
gender = st.text_input("Gender:",value=st.session_state['gen'] )
if st.session_state['agen'] !='':
     st.warning(st.session_state['agen'])
# Father Name
father = st.text_input("Father:",value=st.session_state["f"])
if st.session_state['af'] !='':
     st.warning(st.session_state['af'])

# State (readonly, but you can add logic to populate it)
state = st.text_input("State:", value="", disabled=True)

# District (readonly, but you can add logic to populate it)
district = st.text_input("District:", value="", disabled=True)

# Caste
caste = st.selectbox("Caste:", ["Select Caste", "General", "OBC", "SC", "ST"])

# Religion
religion = st.selectbox("Religion:", ["Select Religion", "Hindu", "Muslim", "Christian", "Sikh", "Buddhist", "Other"])

# Blood Group
blood_group = st.selectbox("Blood Group:", ["Select Blood Group", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

# Phone Number
phone = st.text_input("Phone Number:",value=st.session_state['mob'])


# Higher Education Qualification
education = st.selectbox("Higher Education Qualification:", ["Select Qualification", "B.E", "M.E", "Other"])

# 10th Marks and Upload Marksheet
tenth_mark = st.text_input("10th Marks (%):")
tenth_certificate = st.file_uploader("Upload 10th Marksheet:", type=["pdf", "png", "jpg"])

# 12th Marks and Upload Marksheet
twelfth_mark = st.text_input("12th Marks (%):")
twelfth_certificate = st.file_uploader("Upload 12th Marksheet:", type=["pdf", "png", "jpg"])

# Disability
disability = st.selectbox("Disability:", ["Select", "Yes", "No"])

# Conditional Upload for Disability Certificate
if disability == "Yes":
    disability_certificate = st.file_uploader("Upload Disability Certificate:", type=["pdf", "png", "jpg"])

# GATE/NET Marks and Certificate
gate_net = st.text_input("GATE/NET Marks:",value=st.session_state['gate_mark'])
gate_year = st.text_input("GATE/NET Year :",value=st.session_state['gate'])
gate_net_certificate = st.file_uploader("Upload GATE/NET Marksheet:", type=["pdf", "png", "jpg"])

# Income Certificate
income = st.text_input("Annual income : ",value=st.session_state['income'])
inc_number = st.text_input("Income certificate number : ",value=st.session_state['inc_number'])
income_certificate = st.file_uploader("Upload Income Certificate (for PWD):", type=["pdf", "png", "jpg"])

# Aadhar Number and Upload Aadhar Certificate
aadhar_number = st.text_input("Aadhar Number:",value=st.session_state['aadhar'])


aadhar_certificate = st.file_uploader("Upload Aadhar Certificate:", type=["pdf", "png", "jpg"])
if st.session_state['nv'] !='':
     st.warning(st.session_state['nv'])


def match(str1, str2, threshold=0.8):
    # Get Levenshtein ratio (similarity score between 0 and 1)
    similarity = Levenshtein.ratio(str1, str2)
    return similarity >= threshold,str(similarity)
    
# Community Certificate
community_certificate = st.file_uploader("Upload Community Certificate:", type=["pdf", "png", "jpg"])


if st.button('Submit'):
     if st.session_state['an'] ==''and st.session_state['nv']=='' and st.session_state['adob']=='' and st.session_state['af']=='' :
          st.popover('SUCCESS')
     else:
          st.popover('Insufficiant data !')
if aadhar_certificate is not None and aadhar_certificate != st.session_state["previous_file"]:
    # Create a temporary file in the system's temp directory
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(aadhar_certificate.getbuffer())  # Save uploaded file to disk
        file_path = temp_file.name
    n,dobb,gen,f,mob,aadhar = process_aadhar(file_path).split(',')
    print('{'+n+'}')

    if (n!=''and dobb!='') or (gen!='' and aadhar!=''):
        st.session_state['nv']=''
        ni,s=match(n,name)
        if not ni :
            st.session_state['an']='** NAME mismatch [aadhar name : '+n+'] [ similarity : '+s+' ]'
            if s==0.0:
                 st.session_state['name']=n

        else:
            st.session_state['an']=''
        d=datetime.datetime(int(dobb.split('/')[2]),int(dobb.split('/')[1]),int(dobb.split('/')[0]))
        if (d.year-dob.year)!=0 or (d.month-dob.month)!=0 or (d.day-dob.day)!=0 :
            print(str(dob))
            st.session_state['adob']='** DOB mismatch [aadhar Dob : '+dobb+'] '
        else:
            st.session_state['adob']=''
            st.session_state['age']= str(datetime.datetime.today().year - d.year)
        print('['+gen+"]")
        print('['+gender+']')
        if gender!=gen: 
            st.session_state['agen']='** GENDER mismatch [aadhar gender : '+gen+'] '
            if(s==0.0):
                st.session_state['gen']=gen
        else:
             st.session_state['agen']=''
        ni,s=match(father,f)
        if not ni :
            st.session_state['af']='** FATHER mismatch [aadhar] [ similarity : '+f+' ]'
        else:
             st.session_state['af']=''
    else:
        st.session_state['nv']='** invalid aadhar'
    st.session_state['aadhar']=aadhar
    st.session_state['dob']=dob
    st.session_state['mob']=mob
    st.session_state['f']=f
    st.session_state["previous_file"] = aadhar_certificate
    if(n!=name):
         st.rerun()
if income_certificate is not None and  st.session_state["income_file"] != income_certificate:
    # Create a temporary file in the system's temp directory
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(income_certificate.getbuffer())  # Save uploaded file to disk
        file_path = temp_file.name
    n,income,inc_no = process_income(file_path).split(',')
    st.session_state["income_file"] = income_certificate
    st.session_state['income']=income
    st.session_state['inc_number']=inc_no
    if not match(name,n) and not match(father,n):
        print('MISMATCH')
        st.session_state['inc_number']='** NAME-MISMATCH**'
    if(inc_number!=inc_no):
         st.rerun()
if gate_net_certificate is not None and  st.session_state["gate_file"] != gate_net_certificate:
    # Create a temporary file in the system's temp directory
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(gate_net_certificate.getbuffer())  # Save uploaded file to disk
        file_path = temp_file.name
    n,income,inc_no = process_gate(file_path).split(',')
    st.session_state["gate_file"] = gate_net_certificate
    st.session_state['gate']=income
    st.session_state['gate_mark']=inc_no
    if not match(name,n):
         st.session_state['gate']='** NAME-MISMATCH**'
    if(gate_year!=income):
         st.rerun()
        
def update_text_inputs(name):
    # Update session state for the "Full Name" field
    st.session_state["full_name"] = name

