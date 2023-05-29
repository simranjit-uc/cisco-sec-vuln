# Cisco PSIRT Vulnerability API & Service Now Integration
This API can be used to identify security vulnerabilities on Cisco products. This program written in Python accomplishes two tasks
- Grab vulnerability details on Cisco's CUCM Product and format them in an Excel spreadsheet
- Integrate those identified vulnerabilities with Service Now.

## Prerequisites/Instructions
- Python 3.x
- Client ID and Password for the App registered on Cisco's API Console
- Libraries like Requests and Openpyxl
- Service Now instance and access to its REST APIs
- Use your own API Client ID/Password and Service Now API access credentials

## Cloning the App
You can simply issue the following command from the command prompt on your computer to clone this app to your local directory
```
git clone https://github.com/simranjit-uc/cisco-sec-vuln
```

## Running the App
You can run the app directly from the command prompt or any other program like PyCharm which is what I use.

## Output
You should see two outputs as shown below. 
- The first one will be available at the first stage where the program downloads vulnerability details from the API and puts them in a spreadsheet.
![Output](https://i0.wp.com/learnuccollab.com/wp-content/uploads/2023/05/image-5.png)
- The second output will be available the completion of the second stage where the program creates an incident ticket in Service Now with the above prepared file as an attachment.
![Output](https://i0.wp.com/learnuccollab.com/wp-content/uploads/2023/05/image-15.png)

## More details
For more details on what this code means, you can check out the following links
- Part 1 : https://learnuccollab.com/2023/05/07/automate-cisco-cucm-security-vulnerability-workflow-identification-collection/
- Part 2 : https://learnuccollab.com/2023/05/28/integrate-cisco-cucm-security-vulnerability-workflow-with-service-now/
