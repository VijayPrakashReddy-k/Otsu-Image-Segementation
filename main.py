import os
import glob
import shutil
import base64
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import segmentation
from itertools import cycle
import matplotlib.pyplot as plt


# pandas display options
pd.set_option('display.max_colwidth', None)

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('background.jpeg')

### Function to save the uploaded files:
def save_uploaded_file(uploadedfile):
    try:
        shutil.rmtree("./tempDir")
    except Exception:
        pass
    try:
        os.makedirs("./tempDir")
        os.makedirs("./tempDir/binary")
        os.makedirs("./tempDir/ostu")   
    except Exception:
        pass
    with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
        #st.balloons()
    return st.success("Saved file : {} in tempDir folder".format(uploadedfile.name))

# Function to Read and Manupilate Images
def load_image(img):
    im = Image.open(img)
    image = np.array(im)
    return image

def side_show():
    """Shows the sidebar components for the Image Thresholding and returns user inputs as dict."""
    inputs = {}
    with st.sidebar:
        st.write("#### Thresholding based Techniques")
        option = st.selectbox("select techniques",('Image Binarization', 'Otsu Thresholding'))
        st.write('### You selected:', option)
        inputs['option'] = option
        if option == "Image Binarization":
            st.write("#### Threshold for Binarization")
            inputs["Threshold"] = st.number_input(
            "Threshold",min_value = 80, max_value = 200, value = 100, step = 10,
        )
    return inputs

def main():
    title = '<p style="background-color:rgb(200,100,100);color:rgb(255,255,255);text-align:center;font-size:30px;padding:10px 10px;font-weight:bold"> Computer Vision Class Implementations <p/>'
    st.markdown(title, unsafe_allow_html=True)

    # title = '<p style="font-family:Courier; color:Blue; font-size: 30px;">Computer Vision Class Implementations</p>'
    # st.markdown(title, unsafe_allow_html=True)
    menu = ["Home","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.title("🎮 Image segmentation Playground")
        
        thres = '<p style="background-color:rgb(0,0,0);color:rgb(255,255,255);text-align:center;font-size:30px;padding:10px 10px;font-weight:bold"> 🔥 Thresholding Based Techniques🔥<p/>'
        st.markdown(thres, unsafe_allow_html=True)

        # canny = '<p style="font-family:Courier; color:Red; font-size: 20px;"> Thresholding based </p>'
        # st.markdown(canny, unsafe_allow_html=True)
        hello = '<p style="font-family:Courier; color:Black; font-size: 20px;"><b>Hello, World! &#x1F981;<b></p>'
        st.markdown(hello, unsafe_allow_html=True)

        params = side_show()
        uploadFile = st.file_uploader("Upload File",type=['png','jpeg','jpg'])
        if st.button("Process"):
            # Checking the Format of the page
            if uploadFile is not None:
                file_details = {"Filename":uploadFile.name,"FileType":uploadFile.type,"FileSize":uploadFile.size}
                st.markdown(file_details, unsafe_allow_html=True)
                img = load_image(uploadFile)
                success = '<p style="font-family:Courier; color:Black; font-size: 20px;">Image Uploaded Successfully</p>'
                st.markdown(success, unsafe_allow_html=True)
                st.balloons()
                st.image(img)
                save_uploaded_file(uploadFile)
                image,image_mode_check = segmentation.load_data("tempDir")
                if image_mode_check:
                    #utils.visualize(image, 'gray')
                    st.image(image)
                else:
                    image = image.convert('L')
                    #gray_image = utils.rgb2gray(image)
                    st.write("Uploaded RGB into Gray scale")
                    st.image(image)
                    #utils.visualize(gray_image, 'gray')
                    path = os.path.join("tempDir",file_details["Filename"])
                    image.save(path, 'JPEG')
                
                img_path = os.getcwd() + "/tempDir/" + uploadFile.name

                if params['option'] == "Otsu Thresholding":
                    o_threshold = segmentation.threshold_otsu(img_path)
                    st.write("#### Least Variance can be achieved between object and background clases for given Image after Iterations at a threshold of : ",o_threshold)
                    path = os.getcwd() + "/tempDir/ostu" 
                    images = glob.glob(os.path.join(path, '*'))
                    #caption = ["Otsu Thresholding Image","Grey Scaled Image"] # your caption here
                    cols = cycle(st.columns(2)) # st.columns here since it is out of beta at the time I'm writing this
                    for idx, filteredImage in enumerate(images):
                        next(cols).image(filteredImage, width=380) #, caption=caption[idx])
                    #st.image(images, use_column_width=True, caption=["Otsu Thresholding Image","Grey Scaled Image"])
                elif params['option'] == "Image Binarization":
                    b_threshold = segmentation.threshold_binary(img_path,params['Threshold'])
                    st.write("##### Given Threshold for Image Binarization : ",params['Threshold'])
                    path = os.getcwd() + "/tempDir/binary" 
                    images = glob.glob(os.path.join(path, '*'))
                    #caption = ["Grey Scaled Image","Binary Thresholding Image","Histogram of Pixels for given Threshold Image"] # your caption here
                    cols = cycle(st.columns(2)) # st.columns here since it is out of beta at the time I'm writing this
                    for idx, filteredImage in enumerate(images):
                        next(cols).image(filteredImage, width=380)#, caption=caption[idx])
                    #st.image(images, use_column_width=True, caption=["Binary Thresholding Image","Grey Scaled Image"])
                    
            else:
                #st.write("Please Upload the Image and make sure your image is in JPG/PNG Format.")
                failed = '<p style="font-family:Courier; color:Black; font-size: 20px;">"Please Upload the Image and make sure your image is in JPG/PNG Format."</p>'
                st.markdown(failed, unsafe_allow_html=True)
    else:
        with st.sidebar:
            title = '<p style="font-family:Courier; color:Green; font-size: 18px;"> Otsu threshold :  Otsus method determines an optimal global threshold value from the image histogram.</p>'
            st.markdown(title, unsafe_allow_html=True)

        # title = '<p style="font-family:Courier; color:Red; font-size: 30px;"> Image segmentation </p>'
        # st.markdown(title, unsafe_allow_html=True)

        title = '<p style="background-color:rgb(0,0,0);color:rgb(255,255,255);text-align:center;font-size:30px;padding:10px 10px;font-weight:bold"> Image thresholding with Otsu method <p/>'
        st.markdown(title, unsafe_allow_html=True)

        sentence = '<p style="font-family:Courier; color:Black; font-size: 18px;"> ◉ Image thresholding is a process for separating the foreground and background of the image. There are lots of methods for image thresholding, Otsu method is one of the methods proposed by Nobuyuki Otsu. The Otsu algorithm is a variance-based way to automatically find a threshold value by which the weighted variance between foreground and background is the least. </p>'
        st.markdown(sentence, unsafe_allow_html=True)

        sentence1 = '<p style="font-family:Courier; color:Black; font-size: 18px;"> ◉ With different threshold value, the pixel values of foreground and background are various. Hence, both pixels have different variance for different thresholding. The key of Otsu algorithm is to calculate the total variance from the two variances of both distributions. The process needs to iterate through all the possible threshold vlaues and find a threshold that makes the total variance is smallest.</p>'
        st.markdown(sentence1, unsafe_allow_html=True)


        h1 = '<p style="background-color:rgb(106,90,205);color:rgb(255,255,255);text-align:center;font-size:20px;padding:10px 10px;font-weight:bold"> Image Binarization <p/>'
        st.markdown(h1, unsafe_allow_html=True)

        def1 = '<p style="font-family:Courier; color:Black; font-size: 18px;"><b>Definition :</b> Image binarization applies often just one global threshold T for mapping a scalar image I into a binary image.</p>'
        st.markdown(def1, unsafe_allow_html=True)

        sent1 = '<p style="font-family:Courier; color:Black; font-size: 18px;"> ◉ The global threshold can be identified by an optimization strategy aiming at creating "large" connected regions and at reducing the number of small-sized regions, called <b>"Artifacts"</b></p>'
        st.markdown(sent1, unsafe_allow_html=True)

        st.latex(r'''
        J(x,y) = \begin{cases}
        0 &\text{if } I(x,y) < T \\
        1 &\text Otherwise
        \end{cases}
        ''')


        #st.image("Images/AutoEncoder.png")
        h2 = '<p style="background-color:rgb(106,90,205);color:rgb(255,255,255);text-align:center;font-size:20px;padding:10px 10px;font-weight:bold"> Otsu Thresholding <p/>'
        st.markdown(h2, unsafe_allow_html=True)

        def2 = '<p style="font-family:Courier; color:Black; font-size: 18px;"> <b> Definition : </b> The method uses grey-value histogram of the given image I as input and aims at providing the best threshold </p>'
        st.markdown(def2, unsafe_allow_html=True)

        sent2 = '<p style="font-family:Courier; color:Black; font-size: 18px;"> ◉ Otsu’s algorithm selects a threshold that maximizes the between-class variance.  </p>'
        st.markdown(sent2, unsafe_allow_html=True)

        sent2 = '<p style="font-family:Courier; color:Black; font-size: 18px;"> ◉ In the case of two classes,   </p>'
        st.markdown(sent2, unsafe_allow_html=True)
        
        st.latex(r'''
        \sigma_{b}^2 = P_{1}(\mu_{1}-\mu)^2 + P_{2}(\mu_{2}-\mu)^2 = P_{1}P_{2}(\mu_{1}-\mu_{2})^2
        ''')

        sent3 = '<p style="font-family:Courier; color:Black; font-size: 18px;"> where P1 and P2 denote class probabilities, and μi the means of object and background classes.  </p>'
        st.markdown(sent3, unsafe_allow_html=True)

        #st.image("Images/encoder_decoder.png")

        

if __name__ == '__main__':
	main()
