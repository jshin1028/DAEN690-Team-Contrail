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
1. Detect the presence of contrails in Terrestrial Sky Images. <br>
2. Create a dashboard of contrail statistics from the Terrestrial Sky Images. <br>
3. Contrail prediction engine. <br>
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
 - Storage: S3
 - Computing: EC2
 - Relational Database: RDS
<br><br>

### System Architecture
![daen690 system architecture2 drawio](https://user-images.githubusercontent.com/123881529/230801903-1e667235-0b70-40bc-a3b4-3ab3eebad30d.png)
<br><br>

### Annotations on the images
![rectangular annotation](https://user-images.githubusercontent.com/123881529/230802491-2334bfd2-6d9b-47e7-80ed-8258817be2b1.png)

The first way we annotated the images was by using rectangular annotations. We chose this because most of the models readily available are able to detect objects accurately if they are annotated in rectangles. With this annotation, the model will learn everything that is present in the rectangle and the accuracy should be relatively high because there is room for error (models developed using rectangular annotation are more generalized in nature and can detect objects that have slight variations with high accuracy).  
<br>
![polygon annotation](https://user-images.githubusercontent.com/123881529/230802541-ca004f6b-9313-49d3-8f77-e128aca35e30.png)

The LongLived contrails are the green colored polygons and Cirrus contrails are colored in red. The main advantage of this annotation is that the machine learning model can detect contrails with more accuracy as these are custom annotations. Polygon Annotations are advantageous when there is no definite or rigid structure of the object that we are trying to predict. This will give us more room to fine tune the model and detect hidden structures present in the clouds. 
<br><br>
### Usage of Roboflow
The object detection model identifies where in the image the contrails are present and can identify if there are multiple contrails. The algorithm draws a bounding box around the contrails it identifies in the image.  
To generate the object detection model, the user can select how the train/validation/test split is performed and then choose pre-processing and augmentation steps. The pre-processing steps include auto-orienting, resizing, isolating objects, static cropping, implementing grayscale, auto-adjusting contrast, tiling, modifying the classes, and filtering nulls. Roboflow automatically applies auto-orienting and resizing to optimize model performance. Augmentation steps can be performed for the entire image or just for the bounding box identified in the annotations.

![roboflow preprocessing2](https://user-images.githubusercontent.com/123881529/230802898-905c833b-040b-4fca-b387-d804f2514853.png)

Once the pre-processing steps are completed, the user can choose how to train the model. Roboflow uses an AutoML product called Roboflow Train to create and train models, which are hosted at an API endpoint (Train - Roboflow). The user has several options to customize the object detection model. Users with the paid upgraded plan can choose a more accurate model that takes longer to train and deploy. For this project, the free version offers a faster but less accurate training model. This model can be trained from a previous project checkpoint, from a public checkpoint, or from scratch. 

![roboflow detection output2](https://user-images.githubusercontent.com/123881529/230802915-08ce9437-78f5-4dde-b312-1c567b3a30bb.png)
![roboflow heatmap](https://user-images.githubusercontent.com/123881529/230802786-742c2cf7-5627-4621-a124-5518ccbf137b.png)


<br><br>
 *Content will be updated as the project progresses.
