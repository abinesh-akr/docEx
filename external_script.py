''' PREPROCESSING '''
import cv2                                 # [Open-source] Image Processing s/w  
import numpy as np                         # Used for manipulating Images
from pdf2image import convert_from_path    # Convert the entire PDF to images

''' EXTRACTION '''
import pytesseract                     
import re
import sys

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path
custom_oem_psm_config = r'-l eng+hin+tam+tel  --psm 1 --oem 3'
# Global variables for ROI selection
roi_start = None
roi_end = None
roi_drawing = False
rois = []
labels = []
pdf_path = 'ABINESH.pdf'
cv_image = None


def standardize(img):
        if img is None:
            print("Image not found.")
        
        # Convert to Grayscale to simplify image processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        left_border = 0
        right_border = w - 1
        top_border = 0
        bottom_border = h - 1
        white_threshold = 85
        l=[]
        # Find left border
        for i in range(0,h,int(h/100)):
            for j in range(0,int(w/2),1) :
                if gray[i,j] < 200:
                    l.append(j)
                    break
        left_border=int(np.mean(l))
        
        l=[]
        # Find right border
        for i in range(0,h,int(h/100)):
            for j in range(w - 1, w-int(w/2) , -1):
                if gray[i,j] < 200 :
                    l.append(j)
                    break
        right_border=int(np.mean(l))

        l=[]
        # Find top border
        for i in range(0,w,int(w/100)):
             for j in range(0,int(h/2),1):
                if gray[j,i] < 200 :
                    l.append(j)
                    break
        top_border=int(np.mean(l))

        l=[]
        # Find bottom border
        for i in range(0,w,int(w/100)):
            for j in range(h - 1, h-int(h/2), -1):
               if gray[j,i] < 200:
                    l.append(j)
                    break
        bottom_border=int(np.mean(l))
            
        img=img[top_border:bottom_border,left_border: right_border]
        return img


def preprocess_image(image):
   # image.reshape(image.shape[1]*2,image.shape[0]*2)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    
    # Thresholding
    _, binary =cv2.threshold(gray, 97, 255, cv2.THRESH_BINARY)
    
    # Optional Morphological Operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    morphed = cv2.morphologyEx(morphed, cv2.MORPH_OPEN, kernel)
    
    
    return image

l=[]

def extract_text_from_roi(image, rois, labels):
    #reader = easyocr.Reader(['en'])
    extracted_data = {}
    #cv2.imshow("rr",image)
    for roi, label in zip(rois, labels):
        x1, y1, x2, y2 = roi
        y,x,z=image.shape
        print("[[[ "+str(image.shape)+ " ]]]")
        x1=int((x/573)*x1)
        y1=int((y/690)*y1)
        x2=int((x/573)*x2)
        y2=int((y/690)*y2)
        cropped_img = image[y1:y2, x1:x2]
        resized_img = cv2.resize(cropped_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        resized_img=preprocess_image(resized_img)
        text = pytesseract.image_to_string(resized_img,config=custom_oem_psm_config)
        #text =reader.readtext(resized_img, detail = 0)
        extracted_data[label] = ''.join(text)
       # print(label+" :\n"+extracted_data[label])
        l.append(label)
        
    return extracted_data

def pdf_to_image(pdf_path):
    # Convert the entire PDF to images
    images = convert_from_path(pdf_path, dpi=100)
    if images:
        # Show dimensions of the first page
        pdf_image = np.array(images[0])
        pdf_image=standardize(pdf_image)
        #Convert to BGR for OpenCV compatibility
        pdf_image = cv2.cvtColor(pdf_image, cv2.COLOR_RGB2BGR)
        return pdf_image
    else:
        print("No images found in the PDF.")
        return None



def process_pdf(pdf_path):

    rois=[]
    labels=[]
    l1=[[5,177,162,339,'u1'],[3,400,273,499,'n1'],[70,543,263,750,'u2']]
    for parts in l1:
        x1, y1, x2, y2, label = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]), parts[4]
        rois.append((x1, y1, x2, y2))
        labels.append(label)
    if not rois or not labels:
        print("ROIs and labels are not defined.")
        return

 
    if not pdf_path:
        print("No PDF file selected.")
        return

    image = pdf_to_image(pdf_path)
  

    if image is None:
        print("no image")
        return

    preprocessed_image = image

    extracted_data = extract_text_from_roi(preprocessed_image, rois, labels)
    print(extracted_data)
    print(l)
    result_str = "Extracted Data:\n"
    
    name_pattern = r"[.]*[\n][A-Za-z ]{3,50}[ \n]"
    date_pattern = r"[0-9][0-9][/][0-9][0-9][/][0-9][0-9][0-9][0-9]"
    fatherp = r"[CSD]/O[:\- ]*[A-Za-z0-9 ]{3,50}[ ]*[\n,]"
    nor= r"[0-9]{4}[ ][0-9]{4}[ ][0-9]{4}"
    mobr=r"[0-9]{10}"
    genr=r"MALE|FEMALE"
    
    certificate_name_pattern = r"AADHAAR"

    name_match = re.search(name_pattern, extracted_data[l[0]], re.IGNORECASE)
    date_match = re.search(date_pattern, extracted_data[l[2]], re.IGNORECASE)
    certificate_name_match = re.search(certificate_name_pattern, extracted_data[l[1]], re.IGNORECASE)
    father = re.search(fatherp, extracted_data[l[0]], re.IGNORECASE)
    no = re.search(nor, extracted_data[l[1]], re.IGNORECASE)
    gen = re.search(genr, extracted_data[l[2]], re.IGNORECASE)
    mob = re.search(mobr, extracted_data[l[0]], re.IGNORECASE)
    user_details={}
    if name_match:
        user_details['Name'] = name_match.group(0).strip().split("\n")[len(name_match.group(0).strip().split("\n"))-1]
       # print("has")
    else: 
        user_details['Name']=' '
    if date_match:
        user_details['Date'] = date_match.group(0).strip()
    else:
        user_details['Date']=' '
    if gen:
        user_details['gen'] = gen.group(0).strip()
        print(user_details['gen'])
    else:
        user_details['gen']= ' '
    if certificate_name_match:
        user_details['Certificate Name'] = certificate_name_match.group(0).strip()
    
    if father:
        user_details['Father'] = ' '.join([f for f in father.group(0).split()[1:]])
        user_details['Father']=user_details['Father'].replace(",",'')
        
    else:
        user_details['Father']= ' '
    if no:
        user_details['Number'] = no.group(0).strip()
    else:
        user_details['Number']=' '
    if mob:
        user_details['Mobile'] = mob.group(0).strip()
    else:
        user_details['Mobile']=' '
    for key,value in user_details.items():
        result_str += f"{key}: {value}\n"

    name,father,dob,aadhar,gen,mobile = user_details['Name'],user_details['Father'],user_details['Date'],user_details['Number'],user_details['gen'],user_details['Mobile']
    return f"{name},{dob},{gen},{father},{mobile},{aadhar}"

if __name__ == "__main__":
    print('maincalled')
    file_path = sys.argv[1]
    print(process_pdf(file_path))