# Privacy Roadmap App

**A prototype streamlit web application that serves as a privacy management portal to support small organizations in cost-effective data-privacy management, particularly suited for companies preparing for SOC2 privacy criteria audits.**

## Features
- **Onboarding questionnaire to define privacy goals, understand current privacy situation and identify gaps**
- **Tier-based privacy task list that supports role-based filtering and real-time progress tracking**
- **Automatic generated privacy reports**
  
## File Structure

```
privacy-roadmap-app/
├── Pages/
│   ├── 1_Onboarding.py                 # Onboarding form and initial questions
│   ├── 2_Tier_Profile_and_Questions.py # Tier assessment and definitions
│   ├── 3_Roadmap.py                    # Privacy task checklist
│   └── 4_Profile.py                    # Privacy report with PDF export option
├── roadmap_data.json                   # JSON version of roadmap
├── SOC 2 to NIST Privacy Framework - MileStone Descriptions.csv   # Tier descriptions per category
├── SOC 2 to NIST Privacy Framework - Roadmap.csv        # Raw roadmap used for JSON generation
├── convert_to_json.py                  # Script to convert CSV roadmap to JSON
├── main.py                             # Entry point and landing page
└── README.md                           # You’re here!
```


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


