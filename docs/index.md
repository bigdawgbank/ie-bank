# BigDawg IE Bank Documentation

Welcome to the BigDawg IE Bank Application Documentation Page!  

---

## Project Full Design Document
Please click here to view the full Design Document covering every aspect of our application:
- [Design Document](./Design_Doc.md)

---

## Role Documentation

Here is where you can find more role specific documentation rather than searching through our design document. This section also serves to provide each role the ability to navigate to their specific page and document all of the information relevant to their tasks/work done for our Banking application. The documentation should be updated and maintained consistently throughout the project's lifecycle along with the main design document. This structure ensures that each individual team member can express their workings without interference and with ease, with the Cloud architect documenting their changes in the main doc. A large majority of the documentation can be found in the [Cloud Architect](./CloudArchitect.md) page , with more specific role-based documentation residing within the role pages. 


### Cloud Architect
Designs and implements scalable cloud solutions and ensures best pracitces.
- [Cloud Architect](./CloudArchitect.md)

### Product Owner
Defines the product backlog and ensures the product aligns with business needs.
- [Product Owner](./PO.md)

### Cloud Full Stack Developer
Develops frontend and backend features using Vue.js and Flask.
- [FullStack Developer](./Fullstack.md)

### Cloud Infrastructure Developer
Implements Infrastructure as Code using Bicep templates.
- [Infrastructure Developer](./Infra.md)

### Cybersecurity Engineer
Secures the application and ensures compliance with security standards.
- [Cybersecurity Engineer](./Cybersecurity.md)

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
