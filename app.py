# Core packages
# Security
# Custom-made functions
import nltk
import pandas as pd
import streamlit as st
from PIL import Image 

from signup import *
from scrapper import create_df
from keywords import *
from scrapper1 import create_df1

from tf_idf import run_summarization


#set up the UI
PAGE_CONFIG = {"page_title":"StColab.io","page_icon":":smiley:"} #,"layout":"centered"
st.set_page_config(**PAGE_CONFIG)
# page_bg_img = '''
# <style>
# body {
# background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
# background-size: cover;
# }
# </style>
# '''

# st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    # temp = """
    # <img src="https://rapidapi.com/blog/wp-content/uploads/2018/05/summary-1280x720.jpg" alt="summerize" style="width:698px; border-radius:10 10px;"/>

    # """
    # st.markdown(temp,unsafe_allow_html=True)
    html_temp = """ 
    <div style ="background-color:#310203;padding:3px"> 
    <h1 style ="color:gold;text-align:center;"> Text Summarization</h1> 
    </div> 
    """
    st.markdown(html_temp, unsafe_allow_html = True) 
    
    st.markdown(""" <style> body {     color: #fff;     background-color: #F7D263; } </style>     """, unsafe_allow_html=True)
    
    image = Image.open('img/new.jpeg')
    
    st.image(image,use_column_width=True,use_column_height=0.1, output_format='auto')   


    #st.markdown(html_temp, unsafe_allow_html = True) 
    html_temp1 = """ 
    <div style ="background-color:#9999FF;padding:53px"> 
    <p style ="color:yellow;text-align:left;">This User Interface is meant to summaraize of words\
    </p> 
    </div> 
    """

    keyword = st.text_input(f'Please enter keyword here')
    menu = ["Home", "Database", "Summarize Arxiv", "Summarize GoogleScholar"]
    #If one chooces to proceed with the Home Button --->
    choice = st.sidebar.selectbox('Menu',menu)
    if choice == 'Home':
        #st.subheader("Let's Summarize")
        st.markdown(html_temp1, unsafe_allow_html=True)

    #If interested to see the Dataframe ---->
    elif choice == 'Database':
        st.subheader('The databases created are based on key-word counts')


    #if choice made is to see visualizations --->
    elif choice == 'Summarize Arxiv':
        # Request user for keyword
        st.subheader("Enter the text you'd like to analyze")
        try:
            create_df(keyword)
        except Exception as e:
            raise e

        
        df = pd.read_csv(f"{keyword}.csv")
        df_new = df[['arxiv_ids','abstract','arxiv_links']]
        sumwords = df_new['abstract'].apply(lambda x: run_summarization(x))
        

        # Display results of the NLP task
        st.header('Results')
        st.write('Top 3 Results are:')
        st.write(sumwords[0])
        st.write(f'Find this piece at {df_new.iloc[0,2]}.')
        st.write(sumwords[1])
        st.write(f'Find this piece at {df_new.iloc[1,2]}.')
        st.write(sumwords[2])
        st.write(f'Find this piece at {df_new.iloc[2,2]}.')

    elif choice == 'Summarize GoogleScholar':
        # Request user for keyword
        st.subheader("Enter the text you'd like to analyze.")
        try:
            create_df1(keyword)
        except Exception as e:
            raise e

        
        df = pd.read_csv(f"{keyword}.csv")
        df_new = df[['abstract','url']]
        sumwords = df_new['abstract']
        

        # Display results of the NLP task
        st.header('Results')
        st.write('Top 3 Results are:')
        st.write(sumwords[0])
        st.write(f'Find this piece at {df_new.iloc[0,1]}.')
        st.write(sumwords[1])
        st.write(f'Find this piece at {df_new.iloc[1,1]}.')
        st.write(sumwords[2])
        st.write(f'Find this piece at {df_new.iloc[2,1]}.')
    #elif choice == "Keywords":
    #    st.subheader('Top 3 Keywords')

        #df = pd.read_csv(f"{keyword}.csv")
        #st.write(generate_keys(df))
    #if choice made is to Login for more user or admin priviledges --->
    #elif choice == "Login":
        #st.subheader("Login Section")

        #username = st.sidebar.text_input("User Name")
        #password = st.sidebar.text_input("Password",type='password')
        #if st.sidebar.checkbox("Login"):
            # if password == '12345':
            #create_usertable()
            #hashed_pswd = make_hashes(password)

            #result = login_user(username,check_hashes(password,hashed_pswd))
            #if result:

                #st.success("Logged In as {}".format(username))

                #task = st.selectbox("Task",["Add Post","Profiles"])
                #if task == "Add Post":
                    #st.subheader("Add Your Post")
                #elif task == "Profiles":
                    #st.subheader("User Profiles")
                    #user_result = view_all_users()
                    #clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                    #st.dataframe(clean_db)
            #else:
                #st.warning("Incorrect Username/Password")
    #if choice made is to Create a new account/sign-up --->
    #elif choice == "SignUp":
    #    st.subheader("Create New Account")
    #    new_user = st.text_input("Username")
    #    new_password = st.text_input("Password",type='password')

        #if st.button("Signup"):
        #    create_usertable()
        #    add_userdata(new_user,make_hashes(new_password))
        #    st.success("You have successfully created a valid Account")
        #    st.info("Go to Login Menu to login")


if __name__ == '__main__':
    # nltk.download('punkt')
    # nltk.download('stopwords')
    main()