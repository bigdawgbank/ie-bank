# Cloud Infrastructure Developer Documentation Template

The Cloud Infrastructure Developer is responsible for designing and implementing cloud infrastructure using Infrastructure as Code (IaC). This includes provisioning and managing Azure services to ensure speed, consistency, scalability, reliability, and security.

---

## Modularization Strategy

### Description
Our modularization strategy focuses on isolating resources that do not have a parent-child relationship into separate module files within a directory named `modules`. This approach ensures simplicity and ease of interaction for team members working with the infrastructure. The main file, `main.bicep`, triggers the deployment of resources defined in the modules folder.

### Key Decisions
1. **Single Repository**:
   - We decided to keep all infrastructure code in a single repository rather than splitting it into separate repositories for Azure components, Backend, and Frontend. This decision simplifies the process for team members who need to interact with the infrastructure.

2. **Small Number of Modules**:
   - Given the relatively small number of modules, we maintained a flat structure with standardized and coherent file naming. This organization keeps the structure easy to navigate and manage.

3. **Future Scalability**:
   - If the project grows significantly in terms of resources and modules, we will consider classifying the modules one layer deeper under categories like Azure components, Backend, and Frontend.

### Naming Conventions
To ensure clarity and consistency, we standardized the naming conventions for project files:
- **Lowercase Letters with Hyphens**:
  - All file names use lowercase letters with hyphens (-) to separate words for readability.
- **Bicep Suffix**:
  - File names end with the `.bicep` suffix to indicate Bicep templates.
- **Descriptive Names**:
  - Each name starts with a descriptor that identifies the resource or functionality (e.g., `app-service-plan.bicep` for the service plan).
  - Related resources are grouped with shared prefixes (e.g., `app-service-be.bicep` for backend and `app-service-fe.bicep` for frontend).
  - Specific distinctions are made where necessary, such as between `postgre-sql-db.bicep` and `postgre-sql-server.bicep`, ensuring compact yet informative naming across the project.

### Implementation
- **Main File**:
  - The `main.bicep` file serves as the entry point, orchestrating the deployment of various resources by referencing the module files.
- **Modules Directory**:
  - The `modules` directory contains individual Bicep files for each resource, such as `app-service-plan.bicep`, `app-service-be.bicep`, `app-service-fe.bicep`, `postgre-sql-server.bicep`, and `postgre-sql-db.bicep`.

### Team Collaboration
This decision was made after discussions with the cloud architect and the full-stack developer, who emphasized the importance of keeping the structure straightforward and avoiding unnecessary organizational complexity. This approach aligns with our decision to merge all three repositories into one, ensuring consistency across the project.

### Conclusion
Although there were initial disagreements, the rationale behind this approach became clear, highlighting its potential to improve team members' understanding of the infrastructure repository. Ultimately, this was a team decision, prioritizing clarity and simplicity, especially since this exercise was conducted during a sprint.

---

## Employed Azure Services
The employed azure services are all documented in the Cloud Architect Section:
[Employed Services](./CloudArchitect.md#app-service-for-containers)

---

## Infrastructure Release Strategy

The infrastructure release strategy for the BigDawgBank application ensures a structured and secure deployment process across different environments. This strategy leverages Infrastructure as Code (IaC) tools such as Bicep templates and GitHub Actions workflows to automate the provisioning and updating of infrastructure. Our CI/CD strategy for managing Azure infrastructure as code follows a structured pipeline to ensure quality, consistency, and reliability across Development, UAT (User Acceptance Testing), and Production environments. This strategy is implemented using GitHub Actions, with workflows designed for both Continuous Integration (CI) and Continuous Delivery (CD), ensuring seamless infrastructure deployment while maintaining code quality and security standards.

### Continuous Integration (CI) Process
- **Check for Changes**: 
  - The process begins with a `check-changes` job that identifies modifications to infrastructure files in the `infra` directory. 
  - If changes are detected, the pipeline triggers a build job.

- **Validation Steps**: 
  - **Bicep Linter (`az bicep build`)**:
    - Validates the syntax of the templates to ensure adherence to best practices and syntax rules.
  - **Security Analysis (Checkov)**:
    - Scans templates for vulnerabilities, providing early feedback to developers.
  - These tasks help maintain a high standard of quality in the infrastructure code.

### Continuous Delivery (CD) Process
- **Validation Steps**:
  - Each environment (Development, UAT, and Production) has a dedicated validation step (`validate_X_template`, where X refers to the step in question).
  - Uses **Azure Resource Manager (ARM) templates** in Validate mode to simulate deployments without applying changes.
  - **Resource Drift Detection (`az deployment group what-if`)**:
    - Ensures alignment between the desired and actual resource states.

### Development Environment
The development environment is used for experimental deployments and testing infrastructure configurations.
- **Environment**: Development
- Changes are applied directly after a successful validation or push.

### User Acceptance Testing (UAT) Environment
The UAT environment is used for stakeholder testing and validation of infrastructure changes before they are released to production.
- **Environment**: UAT
- Deployments are triggered by pull requests to the `main` branch or manually initiated workflows.

### Production Environment
The production environment is used for the live application, serving end-users.
- **Environment**: Production
- Deployments proceed only after successful UAT testing and require either a pull request merge to the `main` branch or manual approval.

### Challenges in Implementation
- **Validation Process**:
  - Initial attempts to use `az deployment sub validate` for subscription-level validation did not suit the resource group-based deployment model.
  - Switching to `az deployment group validate` also posed challenges with parameter handling.
  - Solution:
    - Discovered a method from an article ([source](https://www.tpeczek.com/2023/06/devops-practices-for-azure.html)) using `deploymentMode: Validate` to simulate deployments without changes.
    - Enabled error detection before real deployments, streamlining the validation process and ensuring error-free deployments.

- **Resource Drift Detection**:
  - Introduced the use of `az deployment group what-if` to detect discrepancies between the actual and desired infrastructure states.
  - This step ensures the infrastructure remains consistent with Bicep templates, avoiding errors or conflicts caused by manual changes or untracked updates ([source](https://learn.microsoft.com/en-us/cli/azure/deployment/group?view=azure-cli-latest)).

### Collaboration and Alignment
- **Team Collaboration**:
  - Developed in collaboration with the cloud architect to align with release and repository management practices.
- **Key Features**:
  - Single repository structure.
  - Clear job definitions.
  - Automation tools for validation and security checks.
- **Outcome**:
  - Enhanced reliability, simplified infrastructure management, and improved team collaboration.

### Rollback Mechanisms and Disaster Recovery
To ensure the reliability and stability of the infrastructure, the following mechanisms are in place:
- **Rollback Mechanisms**: In case of deployment failures, the infrastructure can be rolled back to the previous stable state using the versioned Bicep templates and GitHub Actions workflows.
- **Disaster Recovery**: Regular backups and point-in-time restore capabilities are implemented for critical resources such as the PostgreSQL database to ensure data integrity and availability in case of failures.

By following this release strategy, the BigDawgBank application ensures a structured and secure deployment process, minimizing the risk of errors and ensuring that only thoroughly tested infrastructure changes reach the production environment. This strategy also aligns with GitHub Security best practices by preventing direct pushes to the `main` branch and enforcing code reviews through pull requests.

---