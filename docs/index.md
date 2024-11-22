# BigDawg IE Bank Documentation

Welcome to the BigDawg IE Bank Application Documentation Page!  

---

## Project Description

The BigDawg IE Bank Application builds upon the success of the previous IE Bank Application developed during the first phase of the project. For the next phase, we aim to deliver a **Minimum Viable Product (MVP)** that includes additional features like: **Admin Portal**: A user management system enabling administrators to create, update, and delete users. **User Portal Enhancements**: Registration forms, bank account linking, and money transfer functionalities. **Secure Deployment**: Following DevOps best practices to automate CI/CD pipelines and ensure a robust DTAP (Development, Test, Acceptance, Production) workflow. This project emphasizes modularity, scalability, and security, ensuring compliance with financial industry standards and providing seamless user experiences.

---

## Role Documentation

This section serves to provide each role the ability to navigate to their specific page and document all of the information relevant to their tasks/work done for our Banking application. The documentation should be updated and maintained consistently throughout the project's lifecycle. This structure ensures that each individual team member can express their workings without interference and with ease.

### Product Owner
Defines the product backlog and ensures the product aligns with business needs.
- [Product Owner](./PO.md)

### Cloud Architect
Designs and implements scalable cloud solutions and CI/CD pipelines.
- [Cloud Architect](./CloudArchitect.md)

### Cloud Full Stack Developer
Develops frontend and backend features using Vue.js and Flask.
- [FullStack Developer](./Fullstack.md)

### Cloud Infrastructure Developer
Implements Infrastructure as Code using Bicep templates.
- [Infrastructure Developer](./Infra.md)

### Cybersecurity Engineer
Secures the application and ensures compliance with security standards.
- [Cybersecurity Engineer](./Cybersecuirty.md)

### Site Reliability Engineer
Monitors system performance and ensures application reliability.
- [Site Reliability Engineer](./Sitereliable.md)


## How to Edit GitHub Pages(Quick Guide)

Follow these steps to edit the GitHub Pages and maintain the documentation:

#### 1. Clone the Repository
1. Open your terminal or Git Bash.
2. Clone the repository using the command:
   `git clone <repository-url>`

#### 2. Navigate into the Repository Folder

Run the following command to navigate into the repository folder:
`cd <repository_name>`

#### 3. Switch to the `gh-pages` Branch

Ensure that you're working on the `gh-pages` branch to edit the documentation:

`git checkout gh-pages`

#### 4. Locate the Files

All the documentation files for the GitHub Pages are stored in the `docs/` folder. Inside this folder, you'll find:

-   `index.md`: The main landing page for the GitHub Pages.
-   Role-specific markdown files, such as `CloudArchitect.md`, `Fullstack.md`, etc.

#### 5. Edit the Markdown Files

1.  Open the file you wish to edit using a text editor (e.g., Visual Studio Code, Notepad++).

2.  Follow the Markdown syntax for formatting. For example:

3.  Save your changes.

#### 6. Commit and Push Changes
After editing, commit your changes to the `gh-pages` branch:

`git add .`
`git commit -m "Update documentation<Rolename>"`
`git push origin gh-pages`


### Aditional Resources for project:
