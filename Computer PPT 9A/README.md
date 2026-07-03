# Analysis [ **[Download](https://www.mediafire.com/file/jrk5uhkhhs0kk05/AI_Pt-1_Proj.pptx/file)** ]

### 1. WHO (2.5 Marks) – The Stakeholders & Target Users
- **Primary Users**: Security Operations Center (SOC) Analysts and Incident Responders who are overwhelmed by alert fatigue and need intelligent prioritization of threats.
- **Affected Entities**: **Employees** across all departments whose digital behavior (login times, data access, file transfers) will be monitored to establish a "normal" baseline.
- **Stakeholders**: The Chief Information Security Officer (CISO) for policy compliance, the IT Infrastructure team who manages the network, and external regulatory bodies (e.g., GDPR, HIPAA) requiring data breach prevention.

---

### 2. WHAT (2.5 Marks) – The Core Problem & Objective
- **The Problem**: Traditional firewalls and rule-based Intrusion Detection Systems (IDS) operate on static signatures. They fail to detect **zero-day threats** and subtle **insider threats**, because they cannot distinguish between legitimate admin access and a hacker using stolen credentials moving data laterally across the network.
- **The AI Objective**: To build an **Unsupervised Anomaly Detection System** that continuously scrapes and ingests massive volumes of raw network logs (syslogs, VPN logs, authentication logs) to learn individual user behavior patterns and flag statistically significant deviations (e.g., a user downloading 10GB at 3 AM from an unfamiliar IP).

---

### 3. WHERE (5 Marks) – Data Sources & Deployment Scope
This is worth 5 marks, so be detailed about the *data pipeline and deployment environment*:

- **Data Sources (Where the logs come from)**: 
  - **Perimeter Logs**: Firewalls, Proxy servers, and VPN gateways (ingress/egress traffic).
  - **Authentication Logs**: Active Directory (AD) and LDAP servers (tracking failed logins, unusual access times).
  - **Endpoint Logs**: EDR (Endpoint Detection and Response) tools and system event logs from employee workstations and servers.
  - **Data Movement Logs**: Database access logs and cloud storage (OneDrive/SharePoint) audit trails to track the *movement of data*.
- **Deployment Scope (Where the AI runs)**: The AI model will be deployed on a **secure, isolated GPU cluster** within the organization’s private cloud (not public internet) to avoid exposing sensitive log data. It sits **between the data lake** (where logs are aggregated) and the **SIEM (Security Information and Event Management)** dashboard, acting as an intelligent filtering layer before alerts reach the human analyst.

---

### 4. WHY (5 Marks) – Justification, Modeling, & Evaluation Parameters
This requires the most detail, covering *why AI* and *how you measure success*:

- **Why AI over Traditional Firewalls**: Firewalls inspect *packet headers* and ports. They cannot read *user intent*. AI is required because the **Volume, Velocity, and Variety** of log data make rule-writing impossible. AI dynamically adapts—if an employee works night shifts for a week, the model updates its baseline, unlike a static rule which would falsely flag them daily.
- **Modeling Approach (The AI Cycle)**:
  - *Data Preprocessing*: Parse raw semi-structured logs (JSON/Syslog) into structured features: `[User_ID, Timestamp, Source_IP, Data_Volume_Transferred, Access_Resource, Login_Success/Fail]`.
  - *Model Selection*: Use **Isolation Forest** or **Autoencoders (Neural Networks)** for unsupervised learning. These do not require pre-labeled attack data. The Autoencoder reconstructs "normal" behavior; a high reconstruction error means the user's current behavior is anomalous (susceptible/compromised).
- **Evaluation Parameters (Crucial for your 5 marks)**:
  - **Recall (Sensitivity)** - *Highest Priority*: Must be > 98%. In cybersecurity, missing a real attack (False Negative) is catastrophic. We prioritize catching every potential breach.
  - **Precision**: Must be balanced. Too many False Positives cause analyst burnout. Target > 85%.
  - **F1-Score**: The harmonic mean of Precision and Recall—used as the primary overall metric.
  - **Time-to-Detect (TTD)**: Measured in **milliseconds**. The model must scrape and score logs in near-real-time (under 500ms per batch) before the data exfiltration finishes.
  - **Risk Scoring Calibration**: Evaluating the model's Mean Squared Error (MSE) on reconstruction—quantifying how far a user's current session deviates from their historical 30-day rolling average.
