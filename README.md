# Introduction to Computer Science and Programming  
### (Cohort 2020)

---
#### *Name*: Nguyen Minh Hieu  
#### *Student ID*: 20040008  
#### *Class*: 20DS  
#### *Email*: hieu.nguyen200408@vnuk.edu.vn

---
## Final Project: Identify alphanumeric characters on cars' license plates.

### 1. Choose input data:  
Dataset contains images of the back of a car, or the license plate of a car.  
License plates are in European or Indian format: 1 line, long rectangle, width/height ~ [4, 5].
   > Folder: dataset
   
### 2. Problem statement and 10 questions
**Problem statement:** Identify the car license plate ***(CLP)*** and its alphanumeric characters in an image for different purposes.  

**10 questions for the input data:**
   - ***Question 1:*** List all filenames of the dataset into files_list.csv.
     > files_list.csv
   - ***Question 2:*** From the original images, create a new image with highlighted license plate's characters and save into a folder.
     > Folder: blackhat_morph
   - ***Question 3:*** Locate potential regions (white regions) of the license plate in the image and save into a folder.
     > Folder: potential_regions
   - ***Question 4:*** Identify the region that contain the license plate by applying aspect ratio (width/height) of each region. Draw contours on that region in the original image and save into a folder.
     > Folder: drawn_CLP_cnts
   - ***Question 5:*** Crop the license plate (binary format for tesseracts reading) from the original image and save into a folder.
     > Folder: cropped_CLP
   - ***Question 6:*** Read the characters from cropped_CLP using Tesseracts-OCR (Optical Character Recognition) and save Filename - LicenseChars into a csv file.
     > result_1.csv
   - ***Question 7:*** From result_1.csv, add 1 new column "Letters-Only" to check if the license plate contain letters only or both letters and digits. Save this into a new csv file.
     > result_2.csv
   - ***Question 8:*** Create a new column called "points" with the unit digit of sum of the all digits.
     > result_3.csv
   - ***Question 9:*** How many "9 points" plates?
   - ***Question 10:*** User enters a desired point. Randomly give the user 1 license plate with that point. 
    
### 3. Solve 10 questions:  
- Functions:
  > functions.ipynb
- Main program file (code):
  > main_final_project.ipynb