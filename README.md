
<img src="https://i.imgur.com/qyeC8s6.png" width="250" height="100" alt="FEMA Report">

# FEMA Damage Assessment Web App
Project by <a href="https://www.linkedin.com/in/eileen-palmer-b8bb5626/" rel="nofollow">Eileen Palmer</a>, <a href="https://www.linkedin.com/in/eddie-reed-628893/" rel="nofollow">Eddie Reed</a> and <a href="https://www.linkedin.com/in/jurgen-arias-02371117/" rel="nofollow">Jurgen Arias</a>.

<br></br>

## Contents

- [Problem Statement](#Problem-Statement)
- [Functionality of the Web App](#Functionality-of-the-Web-App)
- [Usage of the Web App](#Usage-of-the-Web-App)
- [Building the Web App](#Building-the-Web-App)
- [Limitations](#Limitations)
- [Future Explorations](#Future-Explorations)
- [Acknowledgements](#Acknowledgements)

<br></br>

## Problem Statement

During the recovery phase immediately following a disaster, FEMA performs damage assessment “on the ground” to assess the level of damage caused to residential parcels and to critical infrastructure. To assure an accurate estimation of the damage, it is important to understand the condition of the structures prior to the event. To help and guide the damage assessment efforts following a disaster and to assist the surveyors identify the structures of interest, this tool (a web-app or a mobile app) will expect to get, as an input, a picture of the structure taken at its location. It will retrieve a screen shot of the structure from Google Street View. The students will design a damage assessment form, which, in addition to relevant information about the level of damage to the structures, will also provide a pre-event photo of the assessed structure.

<br></br>

## Functionality of the Web App

This web app is designed to streamline the damage assessment process for FEMA employees. There are two major functionalities:
Retrieve Satellite Imagery
File a Damage Assessment Report
The satellite imagery tool helps FEMA employees in the office. From a dropdown menu, the user can select one of several neighborhoods within the region, and then the app will return a near-real-time satellite image of the neighborhood. This tool can help FEMA visually assess the safety, accessibility, and priority of each neighborhood.
The damage assessment form tool helps FEMA employees in the field. To file a damage assessment report, the FEMA damage assessor first uploads a photo of the damaged property, then verifies the address. An automatic report will be generated containing the user's photo alongside the Google Streetview of the same property, for an easy visual comparison of before and after the event. The report also includes basic property information from Zillow, including the estimated value of the property. The damage assessor will record additional information about the damages to the property. Upon submitting the report, all the information will be sent to a database and can be accessed at headquarters.

<br></br>

## Usage of the Web App:

#### Satellite Imagery
We used the sentinelAPI to obtain satellite images from the sentinel  2 satellite.  The API allows a user to obtain near real-time images from the sentinel satellite.  The user can specify a date and time of interest, provide the necessary coordinates and API returns from the satellite.  This feature is very valuable to FEMA because it allows them to do an initial assessment of a given area from an aerial perspective and to perform an initial triage of the area to assign it an assessment priority before sending out an assessment agent.  This would save the agency time and money by not wasting resources on lower priority areas.    

<br></br>
<img src="https://i.imgur.com/Dgr7rVC.jpg" width="500" height="350" alt="FEMA Report">
<br></br>


#### Filing a Damage Assessment Report
The app works best with a picture taken at the property site. That will be the input for our web based app. Behind the scenes, our python code will read the exif information of the picture which is the metadata that contains information including (but not limited to) the make and model of the phone used to take the picture, the date and time of when the picture was taken, GPS location, etc. We then use the GPS location to pinpoint the coordinates of where the photo was taken. Having the coordinates, we are able to output four possible addresses which are the closest to where the picture was taken. We also generate a Google Street image of the location. We did this by using the Google Geocoding API and the Google Street View Static API (Google provides a $300 credit to use their APIs for the first year). Once we select the correct address from our 4 four options, our code will get the Zillow information for the property and populate the report with the available features using the Zillow API (the Zillow API is free). If no picture is provided, we have the option to type in an address which will pull the Zillow information. We will also select from a dropdown, some considerations about the damaged property. Finally, all these will be shown in a report.
<br></br>
<img src="https://i.imgur.com/J5zvyqU.jpg" width="500" height="350" alt="FEMA Report">
<br></br>

#### Database
For the database, we utilized the Relational Database Service (RDS) of AWS and used the MySQL database engine.  The advantage of leveraging the RDS service in AWS is that it provides the developer with a preconfigured database without having to worry about manually setting up a server to host the database engine and installing and configuring the database software.  The developer gets to select which database he/she wants to run (e.g. MySQL, MS SQLServer, Oracle, etc) all from the AWS console.  Setting up both EC2 and RDS instances can all be done in a matter of about 45 minutes.  For a developer that wants to test out these services, AWS offers a free tier of both services for 12 months and you can have both services running at the same time without being charged.  By hosting this application in the AWS cloud, it provides several advantages:

- 1.Very cost effective.
- 2.Can be deployed very quickly.
- 3.Can be setup to run “On Demand” (meaning only having to pay for services when they are being used).
- 4.Very secure.
- 5.Easy of database administration via a GUI like MySQL Workbench.
- 6.Web server and database instance backups are performed and can be configured by the developer via AWS console.
<br></br>

## Building the Web App:

The front-in web application is written in Flask. Flask is a micro web framework for Python code which renders web pages to the end user from code that was originally written in Python.  The micro web framework is suitable for development purposes but is not designed to run as a fulltime webserver. Once the application is ready to be deployed in production, we would need to setup a more robust web server like Apache to serve as a proxy for the Flask application.
We created an EC2 instance in Amazon Web Services (AWS) to run our web application and it is currently live.  
<br></br>



## Limitations:
- Pulling close to real time satellite imagery proved to be challenging.
- Building a Web App with flask was very time consuming and due to time constraints we were not able to develop a fully working web app.
- Connecting to a database that can store our images and reports was not an option since Zillow does not allow their information to be stored.
- Not all properties have Google Street View photos, some properties have pictures that are not too helpful.
- Zillow does not provide information about commercial properties.
- Our reports only include one photo per report.
<br></br>


## Future Explorations:
- We would like to apply machine learning on the satellite images to classify the nature of the disaster.
- We would like to have multiple photos per report.
- We would like to have information about non-residential properties.
- We would like to increase the breadth of data sources.
<br></br>


## Acknowledgements
Thank you to the previous DC groups for their guidance and counseling.
<a href="https://github.com/opacichjj/FEMA-PDA-and-Route-Optimizer" rel="nofollow">Github Link for DSI-DC (3) students' past work.</a> <br>
Thank you to the DSI-LA for Flask framework assistance.
<a href="https://github.com/valarn/FEMA-Damage-Assessment-API-Python" rel="nofollow">Github Link for DSI-LA students' past work.</a> <br>
Thank you to the DSI-SF for initial functions.
<a href="https://github.com/miecky/project-client_project" rel="nofollow">Github Link for DSI-SF students' past work.</a><br>

<br></br>
