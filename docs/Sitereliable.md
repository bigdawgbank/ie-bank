# **Site Reliability Engineer Documentation**

The Site Reliability Engineer (SRE) ensures the reliability, efficiency, and scalability of software systems by applying engineering principles to IT operations. This includes defining SLAs, SLOs, and SLIs, designing monitoring strategies, and preparing incident response plans.

---

## **1. Service Level Agreement (SLA)**

### SLA Definition
The SLA defines the commitments to end-users regarding the application's performance, availability, and support.

**Commitments:**
- **Uptime Guarantee:** 99.9% availability per month, ensuring downtime does not exceed 43 minutes and 49 seconds monthly.
- **Response Time:** Backend API responses will maintain a maximum response time of less than 300ms for 95% of requests, measured monthly.
- **Support Availability:** High-priority incidents (e.g., service outages) will be resolved within 1 hour of detection.
- **Compensation Policy:** In case of SLA violations, service credits proportionate to downtime or degraded performance will be provided.

---

## **2. Service Level Objectives (SLOs)**

### SLO Definitions
SLOs are measurable targets to ensure the SLA commitments are achieved.

**Defined Objectives:**
1. **Application Availability:** Maintain 99.9% uptime on a monthly basis.
2. **Error Rate:** Keep system error rates below 1% for all user requests monthly.
3. **API Response Time:** Ensure average API response time is less than 200ms, measured hourly.
4. **HTTP 5xx Error Rate:** Maintain a maximum HTTP 5xx error rate of less than 0.5%, calculated daily.
5. **Critical Incident Resolution Time:** Resolve high-priority incidents within 1 hour of detection.

---

## **3. Service Level Indicators (SLIs)**

### SLI Definitions
SLIs are specific metrics to measure the achievement of SLOs.

**Defined SLIs:**
1. **Application Availability:**
   - **Indicator:** Percentage uptime, calculated as the ratio of successful requests (`requests.success == true`) to total requests, measured via Application Insights logs.
2. **Error Rate:**
   - **Indicator:** The percentage of failed requests (`requests.success == false`) to total requests, measured daily.
3. **API Response Time:**
   - **Indicator:** Average response time of all incoming requests (`requests.duration`), measured hourly.
4. **HTTP 5xx Error Rate:**
   - **Indicator:** Percentage of HTTP 5xx errors (`requests.resultCode startswith "5"`) to total requests, measured daily.
5. **Incident Resolution Time:**
   - **Indicator:** Time elapsed between incident detection and resolution, tracked via incident management tools.

---

## **4. Monitoring Strategy Design**

### Monitoring Strategy
A comprehensive monitoring strategy ensures the application meets SLAs and SLOs.

**Tools Used:**
- **Azure Application Insights:** For monitoring performance, requests, exceptions, and dependencies.
- **Azure Log Analytics Workspace:** Centralized log management and analysis.

**Metrics and Logs:**
- Key performance indicators like uptime, error rates, response times, and exception counts are visualized in **Azure Workbooks**.

**Alerts Configured:**
1. **Availability Alerts:** Triggered when uptime drops below 99.9%.
2. **Error Rate Alerts:** Triggered when error rates exceed 1%.
3. **Response Time Alerts:** Triggered when average response times exceed 200ms.

**Log Analysis:**
- Use **Kusto Query Language (KQL)** to query logs for trends and issues.

---

## **5. Incident Response Design**

### Incident Response Plan
The incident response plan outlines how we or I will handle failures efficiently, minimizing downtime and impact on users.

---

### **Incident Detection**

Detection begins with the monitoring tools configured in the Monitoring Strategy. Alerts are set up in **Azure Application Insights** to notify the team in real-time when predefined thresholds are breached.

- **How Notifications Work:**
  1. Alerts trigger when specific thresholds are violated (e.g., error rate > 1%, uptime < 99.9%).
  2. The alert system sends messages directly to the **team’s dedicated Slack channel** via the configured **Slack webhook URL**.
  3. Notifications include:
     - Name of the alert (e.g., `uptimeAlert-dev`).
     - The severity level (e.g., P1, P2).
     - A brief description of the issue.
     - A link to the relevant logs or metrics in Azure Application Insights for further investigation.

---

### **Incident Triage**

Once the alert is received in the Slack channel:
1. **Triage Process:**
   - Determine the severity level:
     - **P1 (Critical):** Complete outage or major failure impacting all users.
     - **P2 (High):** Significant degradation affecting multiple users.
     - **P3 (Medium):** Minor issues affecting a small subset of users.
   - Assign an incident lead who will coordinate the response efforts.

2. **Tools for Diagnosis:**
   - Use linked Azure Workbooks for visualizing the data.
   - Query detailed logs in **Azure Log Analytics Workspace** using KQL.
   - Examine metrics such as `requests.duration`, `requests.success`, and dependency failure rates.

---

### **Incident Resolution**

For P1 and P2 incidents:
1. **Immediate Actions:**
   - Notify the relevant stakeholders through Slack and email.
   - The incident lead coordinates with team members to:
     - Diagnose the root cause using metrics, logs, and dashboards.
     - Apply immediate fixes, such as:
       - Restarting services.
       - Scaling resources if under capacity.
       - Rolling back recent deployments if identified as the cause.
2. **Incident Timelines:**
   - **P1 incidents** are targeted for resolution within **1 hour**.
   - Detailed steps for resolution are logged in the incident management tool.

---

### **Post-Incident Review**

After resolution:
1. **Root Cause Analysis (RCA):**
   - Conduct RCA for all **P1 and P2** incidents to identify the root cause and contributing factors.
   - Document findings in a shared knowledge base for future reference.

2. **Preventive Measures:**
   - Implement permanent fixes to address root causes.
   - Update SLIs, SLOs, and monitoring alerts to prevent recurrence.

---

### **Communication Plan**

During and after incidents:
1. **Stakeholder Updates:**
   - The SRE team provides regular updates in the Slack channel for ongoing incidents.
   - After resolution, a summary is shared, including:
     - Incident details (what happened and when).
     - Resolution steps taken.
     - Impact on users.
     - Measures to prevent recurrence.

2. **End-User Communication:**
   - For major incidents, inform end-users via the application’s status page or email notifications.

**[Incident Response Design in Design Document](#incident-response-design)**

---

## **6. Site Reliability Engineering Design**

### SRE Design Principles
**Automation:**
- **Infrastructure as Code (IaC):** Use Bicep templates for repeatable deployments.
- **CI/CD Pipelines:** Automate build, test, and deployment processes using GitHub Actions.

**Resilience:**
- Fault-tolerant architecture with retry logic and fallback mechanisms.
- Redundant services deployed across Azure availability zones.

**Scalability:**
- Auto-scaling rules for Azure App Services and databases.
- Monitor CPU and memory usage to adjust capacity proactively.

**Collaboration:**
- Work closely with development and operations teams to integrate SRE practices.

**Continuous Improvement:**
- Use monitoring data and incident insights to refine SLAs, SLOs, and SLIs
