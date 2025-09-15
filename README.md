
# TiDB_Hackathon_MedMatch_AI
=======
# MedMatch AI Fusion 🌍💡

![MedMatch Thumbnail](https://github.com/Aryaman-Pandey187/TiDB_Hackathon_MedMatch_AI/blob/main/MedMatch%20-%20thumbnail.jpg)  
*Igniting AI to Guide You to Life-Changing Trials!*

## Overview 🎉
Welcome to *MedMatch*, an innovative AI-powered tool built for the TiDB AgentX Hackathon 2025! This project connects patients worldwide to tailored clinical trials based on their symptoms, potentially saving up to 1.2 million lives annually by accelerating drug approvals. With a vibrant interface, live updates, and global impact, it’s your gateway to hope!

## Features ✨
- **Smart Trial Matching**: Uses TiDB vector search to find relevant trials.
- **AI-Powered Insights**: Kimi AI ranks trials, enriched with PubMed, RxNorm, MeSH, and OpenFDA data.
- **User-Friendly Design**: Streamlit UI with live logs, maps via OpenStreetMap, and email reports via AWS.
- **Global Reach**: Supports underserved populations, aligning with UN SDGs (3, 9, 10, 17).

## How It Works 🚀
1. Enter symptoms (e.g., "diabetes fatigue").
2. Select age/sex, click "Find Trials."
3. Watch live logs, get ranked trials, maps, and emails!

## Tech Stack 🛠️
- **TiDB**: Vector database for trial queries.
- **Kimi AI**: LLM for ranking and tool-calling.
- **AWS**: Lambda/EC2 for emails and deployment.
- **OpenStreetMap**: Interactive location maps.
- **PubMed, RxNorm, MeSH, OpenFDA**: API enrichments.
- **Streamlit, Python, OpenAI, Sentence Transformers, Folium, Boto3**: UI and integrations.

## What’s Next 🌐
- Expand trial data and languages.
- **Integrate Blockchain for Secure Sharing**: Implement blockchain to securely store user-provided health details (e.g., symptoms, age, consent, in-depth User details), ensuring privacy and immutability. Researchers can access anonymized profiles to identify potential participants, contact them directly, and highlight study benefits, encouraging informed participation while maintaining data security.
- Pilot with health groups to maximize impact.
- Live Streamed Data: Integrate real-time updates from ClinicalTrials.gov to keep trial data current, ensuring users always access the latest opportunities.

## Installation & Usage 📥
1. Clone repo: `git clone https://github.com/Aryaman-Pandey187/TiDB_Hackathon_MedMatch_AI.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Add respective API keys and DB connector details
4. Get the CSV data to be ingested from `[ClinicalTrails.gov](https://clinicaltrials.gov/)`
5. Run `clean_trials_data.py`
6. Run `data_ingestion_to_TiDB.py`
7. Run: `streamlit run app.py`
8. Access at `http://localhost:8501`.

## License 📜
This project is available under the **GNU General Public License v3.0 (GPL-3.0)**. Feel free to use, modify, and distribute, but share improvements back with the community!

## Contact 📧
- **LinkedIn**: [Let's Connect](https://www.linkedin.com/in/aryaman-pandey/)
- **GitHub**: [View my work](https://github.com/Aryaman-Pandey187)
- **Email**: pandeyaryaman187@gmail.com

## Acknowledgments 🙏
Thanks to TiDB, Moonshot AI, AWS, and the hackathon community for this journey!

---

*Star this repo if you love it! ⭐*  
*Share the love: [Devpost Submission](https://devpost.com/software/medmatch-an-ai-to-connect-you-with-life-changing-trials)*
