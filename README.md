# SAP_TechAssessment

[Program Introduction](./documents/AssessmentIntroduction.md)

## Usage

1.   Download this repo’s zip file to local, unzip.
2.   Fill your openai api key `OPENAI_API_KEY=''` and gpt model `GPT_MODEL=''` in [.env](./.env) file.
3.   Open the repo’s folder in terminal，type `pip install -r requirements.txt` to install packages.
4.   Type `python ./Self_Intro_Prototype.py` to run the program
5.   For specific demands, check the file [instructions.json](./instructions.json) for the prompt.

![image-20240112140708703](https://images.wu.engineer/images/2024/01/12/202401121407725.png)

For additional function of this program：

1.   Cancel the selecting resume window to enter the cmd window. In this window, press “ENTER” or type “HELP” to show the help page.
2.   Type the additional command.
3.   For example, after type the command “SELECT”, the program will list all conversations stored in local. Type number will enter the conversation context and continue asking.

![image-20240112142429752](https://images.wu.engineer/images/2024/01/12/202401121424773.png)

