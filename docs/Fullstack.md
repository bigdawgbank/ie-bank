# Full Stack Engineer Documentation Template

The Full Stack Engineer is responsible for designing and implementing cloud solutions for both the frontend and backend of the application. This role requires skills in various platforms, languages, and frameworks to ensure the application is scalable, reliable, and cost-effective.

---

## Git Feature Branch Strategy

### 1. Description of Git Feature Branch Strategy
- **Description**: Document the Git feature branch strategy implemented for the project. Include the configuration applied to GitHub to enforce this strategy and explain how it aligns with the DevOps principles of the project.

---

## Continuous Integration (CI) Workflows

### 1. CI Workflow for Frontend

**Description**  
The CI workflow for the frontend application automates the validation of code changes, ensuring any new features or updates are tested before being merged into the main branch.

**Workflow Steps**  

1. **Trigger**  
   - The workflow is triggered on:
     - Push events to the `frontend/**` directory across all branches.
     - Pull requests targeting the `main` branch.  
   - This ensures that changes to the frontend are validated at key integration points.
   ```yml
      on:
      push:
      paths:
         - "frontend/**"
      branches:
         - "*"
         - "!refs/pull/*"
   pull_request:
      branches:
         - main
      paths:
         - "frontend/**"
   ```
2. **Checkout Code**  
   - The `actions/checkout@v3` action is used to retrieve the latest codebase, ensuring that subsequent steps operate on the most recent changes.
   ```yml
     - uses: actions/checkout@v3
   ```
3. **Set Up Node.js**  
   - The workflow sets up the Node.js environment using the `actions/setup-node@v3` action.  
   - Ensures compatibility by specifying `NODE_VERSION` as `18.x`.
   ```yml
      - name: Set up Node.js
         uses: actions/setup-node@v3
         with:
         node-version: ${{ env.NODE_VERSION }}
   ```
4. **Install Dependencies**  
   - Dependencies are installed via `npm install` to ensure all required packages are available for testing and building.
```yml
     - name: Install Dependencies
      working-directory: ${{ env.APP_LOCATION }}
      run: npm install
   ```
5. **Run Tests**  
   - Frontend tests are executed to verify the integrity and functionality of changes.
```yml
      - name: Run Tests
      working-directory: ${{ env.APP_LOCATION }}
      run: npm test
   ```
6. **Build Application**  
   - The application is built using `npm run build`, creating an optimized production build ready for deployment.
```yml
      - name: Build Application
      working-directory: ${{ env.APP_LOCATION }}
      run: npm run build
   ```
---

### 2. CI Workflow for Backend

**Description**  
The backend CI workflow validates changes to backend services by running tests and static analysis, ensuring that the API and business logic remain stable.

**Workflow Steps**  

1. **Trigger**  
   - The workflow runs on:
     - Push events to the `backend/**` directory across all branches.
     - Pull requests targeting the `main` branch.
   ```yml
   on:
   push:
      paths: 
         - "backend/**"
      branches:
         - "*"
   pull_request:
      branches: [ "main" ]
      paths:
         - "backend/**"
   ```
2. **Checkout Code**  
   - Similar to the frontend workflow, this retrieves the latest code for validation.
   ```yml
      - uses: actions/checkout@v3
   ```
3. **Set Up Python Environment**  
   - Python 3.11 is configured using `actions/setup-python@v3`.  
   - Compatibility with the application is maintained.
   ```yml
   - name: Set up Python 3.11
     uses: actions/setup-python@v3
     with:
      python-version: "3.11"
   ```
4. **Install Dependencies**  
   - Backend dependencies are installed using `pip install -r backend/requirements.txt`.
   ```yml
   - name: Install dependencies
   run: pip install -r backend/requirements.txt
   ```
5. **Run Linting and Tests**  
   - `flake8` is used for code linting, ensuring adherence to Python coding standards.  
   - `pytest` runs backend unit tests to validate API routes and business logic.
   ```yml
   - name: Lint with flake8
   run: |
      pip install flake8 pytest
      flake8 backend/ --count --select=E9,F63,F7,F82 --show-source --statistics
      flake8 backend/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

   - name: Test with pytest
   run: python -m pytest -v
   ```
---

## Test/Behavior-Driven Development Strategy
A Precise Description of this can be found in the Cloud Architect Page:
- [TTD](./CloudArchitect.md#test-driven-designtdd)

---

## Inner Loop and Outer Loop

### 1. Definition of Inner and Outer Loop
- **Description**: Define and document the inner loop (developer’s local development workflow) and outer loop (integration, testing, and deployment workflow).

---

## Release Strategy
Please refer to the Cloud Architect Release Strategy Section:
- [Release Strategy](./CloudArchitect.md#release-strategy)

---

## Continuous Delivery (CD) Workflows

### 1. CD Workflow for Frontend

**Description**  
This workflow automates the deployment of the frontend application to the **Development**, **UAT**, and **Production** environments.

**Workflow Steps**  

#### Build and Deploy to Development  

1. **Setup Node.js and Build**  
   - Configures Node.js and builds the application using `npm run build`.

2. **Login to Azure and Deploy**  
   - Authenticates with Azure using `azure/login@v2`.  
   - Retrieves a static web app deployment token using `az staticwebapp secrets list`.  
   - Deploys the application to the development static web app using `Azure/static-web-apps-deploy@v1`.

#### Build and Deploy to UAT  

1. **Prerequisites**  
   - Deployment only occurs for:
     - Pull requests.
     - Workflow dispatch events.
     - Pushes to the `main` branch.

2. **Process**  
   - Follows the same build and deployment steps as the development environment but targets the UAT static web app.

#### Build and Deploy to Production  

1. **Trigger**  
   - Occurs when:
     - A pull request is merged to `main`.
     - Manual workflow dispatch events.  
   - Ensures that only thoroughly tested code reaches production.

2. **Deployment**  
   - Similar to UAT deployment, but targeting the production static web app.

---

### 2. CD Workflow for Backend

**Description**  
The backend CD workflow handles automated deployments to the **Development**, **UAT**, and **Production** environments for the backend services.

**Workflow Steps**  

#### Build and Deploy to Development  

1. **Docker Image Build and Push**  
   - Builds a Docker image for the backend service using `docker build`.  
   - Pushes the image to the Azure Container Registry (ACR) for development.

2. **Deploy to Azure App Service**  
   - Deploys the Docker container to the development App Service using `azure/webapps-deploy@v2`.

#### Build and Deploy to UAT  

1. **Image Creation and Deployment**  
   - Similar to the development deployment, but with:
     - Credentials and registry specific to the UAT environment.
     - Deployment to the UAT App Service.

2. **Requirements for UAT**  
   - Deployment is dependent on:
     - Successful image creation.
     - Triggered workflow dispatch or PR events.

#### Build and Deploy to Production  

1. **Controlled Deployment**  
   - Triggers include:
     - Push to `main` branch.
     - Manual workflow dispatch.  
   - Ensures that only stable, thoroughly tested versions are deployed.

2. **Fault Tolerance and Rollback**  
   - Ensures deployment rollback capabilities by maintaining multiple image versions in the ACR.

---

## Key Features and Benefits of BigDawgBanks CI/CD

- **End-to-End Automation**  
  Both frontend and backend CI/CD pipelines are fully automated, reducing manual intervention and ensuring consistency.

- **Multi-Environment Support**  
  Separate workflows for development, UAT, and production environments ensure thorough testing before production deployment.

- **Azure Integration**  
  Leveraging Azure services (App Service, Static Web Apps, Key Vault, and Container Registry) ensures secure and scalable deployment.

- **Error Detection**  
  Early-stage testing with `flake8` and `pytest` helps identify and resolve issues before deployment.

- **Version Control**  
  Docker image tagging and ACR usage maintain clear version history for rollbacks and debugging.

By combining CI/CD best practices with Azure services, **BigDawgBank** ensures a robust and efficient software delivery process.