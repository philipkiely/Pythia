# Pythia Camera

Bogdan Abaev && Philip Kiely 

PennApps Fall 2019


Check out the [devpost](https://devpost.com/software/pythia-camera).

![Pythia Diagram](https://raw.githubusercontent.com/philipkiely/Pythia/master/images/PythiaCamera.jpg)

## Inspiration

#### Original Idea: 

Deepfakes and more standard edits are a difficult threat to detect. Rather than reactively analyzing footage to attempt to find the marks of digital editing, we sign footage on the camera itself to allow the detection of edited footage.

#### Final Idea:

Using the same technology, but with a more limited threat model allowing for a narrower scope, we can create the world's most secure and intelligent home security camera. 

## What it does

Pythia combines robust cryptography with AI video processing to bring you a unique home security camera. The system notifies you in near-real-time of potential incidents and lets you verify by viewing the video. Videos are signed by the camera and the server to prove their authenticity in courts and other legal matters. Improvements of the same technology have potential uses in social media, broadcasting, political advertising, and police body cameras.

## How we built it

* Records video and audio on a camera connected to a basic WIFI-enabled board, in our case a Raspberry Pi 4

At regular intervals:
* Combines video and audio into .mp4 file
* Signs combined file
* Sends file and metadata to AWS

![Signing](https://raw.githubusercontent.com/philipkiely/Pythia/master/images/ChainedRSASignature.jpg)

On AWS:
* Verifies signature and adds server signature
* Uses Rekognition to detect violence or other suspicious behavior
* Uses Rekognition to detect the presence of people
* If there are people with detectable faces, uses Rekognition to 
* Uses SMS to notify the property owner about the suspicious activity and links a video clip
![AWS](https://raw.githubusercontent.com/philipkiely/Pythia/master/images/AWSArchitecture.jpg)


## Challenges we ran into

None.

Just Kidding:

#### Hardware

* Raspberry Pi
* Hardware lab

#### Software

* File Encoding

#### Web Services

* Several Issues

## Accomplishments that we're proud of

* Complex AWS deployment
* Chained RSA Signature
* Proper video encoding and processing, combining separate frame and audio streams into a single .mp4

## What we learned

#### Bogdan
* Gained experience designing and implementing a complex, asynchronous AWS Architecture
* Practiced with several different Rekognition functions to generate useful results

#### Philip
* Video and audio encoding is complicated but fortunately we have great command-line tools like `ffmpeg`
* Watchdog is a Python library for watching folders for a variety fo events and changes. I'm excited to use it for future automation projects.
* Raspberry Pi never works right the first time

## What's next for Pythia Camera
A lot of work is required to fully realize our vision for Pythia Camera as a whole solution that resists a wide variety of much stronger threat models including state actors. Here are a few areas of interest:

#### Black-box resistance:
* A camera pointed at a screen will record and verify the video from the screen
* Solution: Capture IR footage to create a heat map of the video and compare the heat map against rekognition's object analysis (people should be hot, objects should be cold, etc.
* Solution: Use a laser dot projector like the iPhone's faceID sensor to measure distance and compare to machine learning models using Rekognition

#### Flexible Cryptography:
* Upgrade Chained RSA Signature to Chained RSA Additive Map Signature to allow for combining videos
* Allow for basic edits like cuts and filters while recording a signed record of changes

#### More Robust Server Architecture:
* Better RBAC for online assets
* Multi-region failover for constant operation
