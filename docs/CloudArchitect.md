# Cloud Architect Documentation 

The Cloud Architect is responsible for designing and implementing scalable, reliable, and cost-effective cloud solutions that align with business and user needs. The role encompasses architecture design, infrastructure setup, collaboration with the team on implementation plans, and ensuring proper documentation throughout the project lifecycle.

---

## Functional and Non-Functional requirements

### Functional Requirements (FR)

The following functional requirements outline the behavior and features of the IE Bank Application. Each requirement is linked to the respective user story and will have associated test cases defined.

#### FR01: Default Admin Account
**Requirement:** The application must provide a default administrator account (username and password) upon system setup.  
**User Story:** As an admin, I want a default admin account to be created during system setup so that I can log in and start managing the system immediately.  
**Test Link:** _[To be added]_  

---

#### FR02: Admin User Management
**Requirement:** The admin portal must allow administrators to create, update, delete, and list user accounts.  
**User Story:** As an admin, I want to create, update, and delete user accounts so that I can manage access to the system.  
**Test Link:** _[To be added]_  

---

#### FR03: Password Reset for Users
**Requirement:** Administrators must be able to reset user passwords to assist users who cannot log in.  
**User Story:** As an admin, I want to reset user passwords so that I can assist users who cannot log in.  
**Test Link:** _[To be added]_  

---

#### FR04: Role and Permissions Management
**Requirement:** Administrators must be able to assign roles and permissions to users to control access to specific system parts.  
**User Story:** As an admin, I want to assign roles and permissions to users so that I can control their access to different parts of the system.  
**Test Link:** _[To be added]_  

---

#### FR05: New User Registration
**Requirement:** New bank users must be able to register using a registration form (username, password, and password confirmation). A default account with a random account number must be created upon successful registration.  
**User Story:** As a new user, I want to register for an account so that I can access the system.  
**Test Link:** _[To be added]_  

---

#### FR06: Automatic Account Provisioning
**Requirement:** The system must automatically provision a default account upon new user registration.  
**User Story:** As a user, I want my account to be provisioned immediately after registration so that I can start using the services.  
**Test Link:** _[To be added]_  

---

#### FR07: Secure User Login
**Requirement:** Bank users must log in securely using their username and password to access their accounts.  
**User Story:** As a user, I want to log in securely so that I can access my account.  
**Test Link:** _[To be added]_  

---

#### FR08: View Account and Transactions
**Requirement:** Bank users must view their accounts and associated transactions after logging in.  
**User Story:** As a user, I want to view my account details and recent transactions so that I can manage my finances effectively.  
**Test Link:** _[To be added]_  

---

#### FR09: Money Transfer
**Requirement:** Bank users must be able to transfer money to other accounts by entering the recipient’s account number and transfer amount. The transfer amount must not exceed the available balance.  
**User Story:** As a user, I want to transfer money to other accounts so that I can make payments easily.  
**Test Link:** _[To be added]_  

---

#### FR10: Secure Password Handling
**Requirement:** All user passwords must be hashed and stored securely to prevent data breaches.  
**User Story:** As a developer, I want all passwords to be securely hashed so that user data is protected from breaches.  
**Test Link:** _[To be added]_  

---

#### FR11: Session Management
**Requirement:** User sessions must expire after inactivity to ensure account security.  
**User Story:** As a user, I want my session to expire after inactivity so that my account remains secure.  
**Test Link:** _[To be added]_  

---

#### FR12: Intuitive Admin UI
**Requirement:** The admin portal must have an intuitive UI for efficient user and permission management.  
**User Story:** As an admin, I want a clean and intuitive UI for the portal so that I can efficiently manage users and permissions.  
**Test Link:** _[To be added]_  

---

### Non-Functional Requirements (NFR)

The following non-functional requirements define the performance, security, and usability standards for the IE Bank Application.

#### NFR01: Basic Authentication
**Requirement:** The web application must implement a basic authentication system requiring username and password login. Credentials must be hashed and encrypted in the database.  
**Test Link:** _[To be added]_  

---

#### NFR02: Simple Frontend Interface
**Requirement:** The web application must have a simple and functional frontend UI without requiring advanced aesthetics or responsiveness.  
**Test Link:** _[To be added]_  

---

#### NFR03: System Availability
**Requirement:** The system must achieve 99.95% uptime in the production environment. Downtime should be limited to scheduled maintenance outside peak hours.  
**Test Link:** _[To be added]_  

---

#### NFR04: Cost Optimization
**Requirement:** Azure resources must be provisioned with cost-effective configurations, leveraging reserved instances and auto-scaling to manage resource costs.  
**Test Link:** _[To be added]_  

---

#### NFR05: Handling Peak Loads
**Requirement:** The system must support up to 500 concurrent users in the production environment without performance degradation.  
**Test Link:** _[To be added]_  

---

#### NFR06: Secure Secrets Management
**Requirement:** Secrets such as database connection strings and API keys must be stored securely using Azure Key Vault.  
**Test Link:** _[To be added]_  

---

#### NFR07: Logging and Monitoring
**Requirement:** The application must implement robust logging and monitoring through Azure Application Insights, ensuring errors and performance metrics are captured.  
**Test Link:** _[To be added]_  

---

#### NFR08: Compliance
**Requirement:** The application must comply with GDPR and other relevant data protection regulations to ensure user data privacy.  
**Test Link:** _[To be added]_  

---

#### NFR09: Scalability
**Requirement:** The application must support horizontal scaling for the frontend and backend to accommodate increased user demand.  
**Test Link:** _[To be added]_  

---

#### NFR10: Backup and Recovery
**Requirement:** The system must include point-in-time restore for the database and deployment rollback capabilities in case of failure.  
**Test Link:** _[To be added]_  

---

## Infrastructure Architecture Design

### GitHub
### App Service for Containers
### App Service Plan
### PostgreSQL Database
### Static Website
### Azure Container Registry
### Key Vault
### Log Analytics Workspace
### Application Insights
### Other services as needed

---

## 3. Environment Design
- **Description**: Collaborate with the Infrastructure Developer and Full Stack Developer to document and update the environments required for development, UAT, and production. Include the configuration for each Azure service in each environment.

---

## Well-Architected Framework Design

### 1. Reliability Pillar
- **Description**: Collaborate with the Site Reliability Engineer to document decisions related to system reliability.

### 2. Security Pillar
- **Description**: Collaborate with the Cybersecurity Engineer to document security decisions.

### 3. Cost Optimization Pillar
- **Description**: Collaborate with the Infrastructure Developer to document cost optimization strategies.

### 4. Operational Excellence Pillar
- **Description**: Collaborate with the Full Stack Developer to document operational excellence strategies.

### 5. Performance Efficiency Pillar
- **Description**: Collaborate with the Infrastructure Developer and Site Reliability Engineer to document performance efficiency decisions.

---

## Testing

### Functional
### Non-Functional

---

## 1. Release Strategy
- **Description**: Document the release strategy, including environment design, and ensure alignment with the DevOps checklist and GitHub Security best practices.

## 2. Use Case and Sequential Model Design
- **Description**: Update the use case and sequential model diagrams for each use case in the application.

## 3. Entity Relationship Diagram
- **Description**: Update and document the Entity Relationship Diagram for the database.

## 4. Data Flow Diagram
- **Description**: Update and document the Data Flow Diagram for the application.

## 5. Twelve-Factor App Design
- **Description**: Document how the Twelve-Factor App principles are applied to the project.

---