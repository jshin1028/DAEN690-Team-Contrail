# TERRESTRIAL SKY IMAGE CONTRAIL DASHBOARD (TSICD) #

Capstone Project (contrail detection and dashboard) <br>
DAEN 690-DL2 <br>
Team Contrail: Jordan Dutterer, Venkata Sai Ruthvik Pulipaka, Alyssa Soderlund, Jaeho Shin <br>

### Problem Description <br>
Aviation generates 4% of global warming. One half of the aviation contribution is from contrails. Contrails block the outgoing thermal radiation from escaping to space resulting in excess heating of the Earth. Contrails contribute 2% of the total anthropogenic global heating. Researchers have proposed “Navigation Avoidance” of contrails. To operationalize navigational avoidance the location of Ice Super Saturated Regions in the atmosphere, where contrails are generated, needs to be identified. One approach is through using satellite images. This project uses computer vision machine learning to identify contrails in satellite images. Previous research used Landsat images provided by Google. The computer vision machine learning algorithm applied was able to achieve an accuracy of about 50%. This is no better than flipping a coin. This project will use new approaches to computer vision machine learning to detect the presence of contrails in Terrestrial Sky Images and to create a dashboard of contrail statistics. 
  
![daen690 paper pic](https://user-images.githubusercontent.com/123881529/230802355-35e53630-f22b-4f2c-a283-6769ca961030.png)
<br><br>


  
### Project Goals <br>
The project goals are as follows. <br>
1. Create a contrail prediction engine that detects the presence of contrails in Terrestrial Sky Images. <br>
2. Create a dashboard of contrail statistics from the Terrestrial Sky Images. <br>
<br><br>

### About the Files Attached to the GitHub <br>
 - TensorFlow_Image_Classification.py: Python code that has the ML model for the image classification. <br>
 - Weather_Fairfax, VA 22030 2022-08-01 to 2022-12-31.csv: Hourly weather data from the beginning of August, 2022 to the end of December, 2022. <br>
 - Images with annotations: https://gmuedu-my.sharepoint.com/personal/jduttere_gmu_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fjduttere%5Fgmu%5Fedu%2FDocuments%2FCapstone&ga=1 (need to request the file access). <br>
<br><br>

### Tool/algorithm that We Use for the project
 - Roboflow
 - Power BI
<br><br>

### Cloud Platform (AWS)
 - Storage: EC2 instance built-in storage, S3
 - Computing: EC2 (Windows server)
 - Relational Database: RDS (MySQL)
<br><br>

### System Architecture
![daen690 system architecture2 drawio (2)](https://user-images.githubusercontent.com/123881529/235490310-9306ac0b-b5a6-4254-be0c-2100e4ef90d0.png)

In the system architecture, the first step is to transfer and store three datasets in RDS, which includes sky images, a spreadsheet with image labels, and ground weather data. Following this, the datasets undergo pre-processing and are divided into training and test datasets. The pre-processed datasets are then stored back in RDS, while the sky images are ingested directly into the storage in EC2. 

The model is trained and tested using Roboflow, Momentum AI, and Yolo-Poly algorithms in EC2, selected as suitable algorithms/tools through previous research. After the model training and testing, the model performance of each algorithm/tool is checked. If the performance is satisfactory, the model is used to produce results; otherwise, the model is re-tuned, and the training/test process is repeated. 

The well-trained model's results are saved to RDS, which contains information on detected contrails and annotated contrail images. The results are then displayed and organized in a dashboard using Power BI, which imports the results from RDS. The project also includes a Python GUI for users to run and view predictions using the model in EC2. 

Finally, the project utilizes AWS's storage service, S3, for data backup and large image uploading. The seamless integration of various AWS services, effective pre-processing of datasets, and selection of appropriate algorithms/tools contribute to the success of this project. 
<br><br>

### Annotations on the images
![rectangular annotation](https://user-images.githubusercontent.com/123881529/230802491-2334bfd2-6d9b-47e7-80ed-8258817be2b1.png)

The first way we annotated the images was by using rectangular annotations. We chose this because most of the models readily available are able to detect objects accurately if they are annotated in rectangles. With this annotation, the model will learn everything that is present in the rectangle and the accuracy should be relatively high because there is room for error (models developed using rectangular annotation are more generalized in nature and can detect objects that have slight variations with high accuracy).  
<br>
![polygon annotation](https://user-images.githubusercontent.com/123881529/230802541-ca004f6b-9313-49d3-8f77-e128aca35e30.png)

Another way we annotated the images was by using polygon annotations. The LongLived contrails are the green colored polygons and Cirrus contrails are colored in red. The main advantage of this annotation is that the machine learning model can detect contrails with more accuracy as these are custom annotations. Polygon Annotations are advantageous when there is no definite or rigid structure of the object that we are trying to predict. This will give us more room to fine tune the model and detect hidden structures present in the clouds. 
<br><br>
### Usage of Roboflow
The object detection model identifies where in the image the contrails are present and can identify if there are multiple contrails. The algorithm draws a bounding box around the contrails it identifies in the image.  
To generate the object detection model, the user can select how the train/validation/test split is performed and then choose pre-processing and augmentation steps. The pre-processing steps include auto-orienting, resizing, isolating objects, static cropping, implementing grayscale, auto-adjusting contrast, tiling, modifying the classes, and filtering nulls. Roboflow automatically applies auto-orienting and resizing to optimize model performance. Augmentation steps can be performed for the entire image or just for the bounding box identified in the annotations.

![roboflow preprocessing2](https://user-images.githubusercontent.com/123881529/230802898-905c833b-040b-4fca-b387-d804f2514853.png)

Once the pre-processing steps are completed, the user can choose how to train the model. Roboflow uses an AutoML product called Roboflow Train to create and train models, which are hosted at an API endpoint (Train - Roboflow). The user has several options to customize the object detection model. Users with the paid upgraded plan can choose a more accurate model that takes longer to train and deploy. For this project, the free version offers a faster but less accurate training model. This model can be trained from a previous project checkpoint, from a public checkpoint, or from scratch. Also, the user can see the heatmaps of the annotations.

![roboflow detection output2](https://user-images.githubusercontent.com/123881529/230802915-08ce9437-78f5-4dde-b312-1c567b3a30bb.png)
![roboflow heatmap](https://user-images.githubusercontent.com/123881529/230802786-742c2cf7-5627-4621-a124-5518ccbf137b.png)


<br><br>

### Examples of the Detection Model and the Dashboard
![roboflow trained model result](https://user-images.githubusercontent.com/123881529/235490376-f753562a-5117-4fd8-8c01-85230aa39149.png) <br>
This is an example of an object detection model output in Roboflow. It shows the detected contrails with the tags (Long Lived or Cirrus) and the confidence percentage for each detected contrail. In Roboflow, the user can control the confidence threshold to filter out the detection at a specific confidence level. When the user is done with the settings, the user can copy and paste the Python code to apply it to a Python system. <br>
<br><br>
![prediction tool gui](https://user-images.githubusercontent.com/123881529/235492898-4df28b2e-1e29-47d9-bcc6-ddcb58c80990.png) <br>
This is the GUI for the contrail prediction tool. It is used to Identify contrails in sky images using our Roboflow trained object-detection model. The user can set a confidence threshold for contrail detection (1-99%), and it automatically logs results in the database which sources the Power BI dashboard. Finally, it exports current predictions in the database as an Excel file.<br>
<br><br>
![contrail prediction result](https://user-images.githubusercontent.com/123881529/235490538-fa5b325e-e15e-4e49-af0b-69117b946632.png) <br>
This is an example of detection from the system through the contrail prediction GUI. It shows annotated contrails with the tags (the text is too small to see the tags in the screenshot, but the user can actually zoom in on the text to see it). <br>
<br><br>
![dashboard1](https://user-images.githubusercontent.com/123881529/235490587-1e1846fc-4ded-456d-9c0f-778cf3739d46.png) <br>
![dashboard2](https://user-images.githubusercontent.com/123881529/235490595-d3650fa4-f6df-4e8b-b1cc-59dcb017b729.png) <br>
![dashboard3](https://user-images.githubusercontent.com/123881529/235490604-20ef3288-7fc5-4993-8eec-0ed03ce79d5a.png) <br>
![dashboard4](https://user-images.githubusercontent.com/123881529/235490608-d6810539-f584-4ff7-9316-a73f15ca2d26.png) <br>
This is an example of the dashboard. Users can refresh the dashboard by clicking the "refresh" button. The dashboard has multiple pages to show different information. The first page is the overview page where users can filter the data by contrail type, time, and location. This page shows the statistics and graphics of the number of contrails over time and by location. The second page is the detail page where users can filter the data by weather phenomenon such as cloud coverage, precipitation, and humidity. The visualizations on this page show how the number of contrails changes with different weather phenomena. The last two pages show a key influencers visual for total contrails and individual types of contrails. These pages show which variables have the most correlation with the number of contrails. 


<br>
*If you have any questions, please contact us via email. <br>
jshin14@gmu.edu <br>
jduttere@gmu.edu <br>
vpulipak@gmu.edu <br>
asoderlu@gmu.edu <br>
