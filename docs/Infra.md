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
The Infrastructure Release Strategy is documented clearly in the Cloud Architect Section:
[Infrastructure Release Strategy ](./CloudArchitect.md#infrastructure-release-strategy)

---