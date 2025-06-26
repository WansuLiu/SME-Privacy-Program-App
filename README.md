## Privacy Roadmap App

A prototype streamlit web application that serves as a privacy management portal to support small organizations in cost-effective data-privacy management, particularly suited for companies preparing for SOC2 privacy criteria audits.

# Features
**Onboarding questionnaire to define privacy goals, understand current privacy situation and identify gaps**
**Tier-based privacy task list that supports role-based filtering and real-time progress tracking**
**Automatic generated privacy reports**

## File Structure
privacy-roadmap-app/
├── Pages/
│   ├── 1_Onboarding.py                
│   ├── 2_Tier_Profile_and_Questions.py 
│   ├── 3_Roadmap.py                  
│   └── 4_Profile.py                  
├── roadmap_data.json                  
├── SOC 2 to NIST Privacy Framework - Milestone Descriptions.csv 
├── SOC 2 to NIST Privacy Framework-Roadmap.csv       
├── convert_to_json.py               
├── main.py                           
└── README.md                        

## Set Up Instructions
1. Clone the Repository 
git clone https://github.com/your-username/privacy-roadmap-app.git
cd privacy-roadmap-app
2. (optional) Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Intall Python Streamlit and other dependencies
pip install streamlit pandas
4. Run the Application
streamlit run main.py


