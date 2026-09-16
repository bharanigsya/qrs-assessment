// Question Bank - Role + Level based
// EVERY role + level totals exactly 100 marks
// Voice questions ONLY for HR and PC roles
// salesforce/testing/database/integration/infra/wordpress/data_analytics:
//   fresher & experienced = 10 MCQ + 2 basic coding questions (100 marks)
//   intern = 25 MCQ only, no coding (100 marks)
// hr, pc, finance are unchanged from before.

const QUESTION_BANK = {
  salesforce: {
    fresher: {
      duration: 45,
      questions: [
        { id: "sf_f1", type: "mcq", marks: 5, question: "What is a Salesforce Object?", options: ["A database table", "A UI component", "A workflow", "An Apex class"], correct: 0 },
        { id: "sf_f2", type: "mcq", marks: 5, question: "Which of the following is used for automation in Salesforce?", options: ["Flow", "HTML", "CSS", "JavaScript only"], correct: 0 },
        { id: "sf_f3", type: "mcq", marks: 5, question: "What does SOQL stand for?", options: ["Salesforce Object Query Language", "Simple Object Query Language", "Structured Object Query Language", "Salesforce Online Query Language"], correct: 0 },
        { id: "sf_f4", type: "mcq", marks: 5, question: "Profiles control:", options: ["Object & Field level security", "Only page layouts", "Only reports", "Only dashboards"], correct: 0 },
        { id: "sf_f5", type: "mcq", marks: 5, question: "Which relationship allows a child record to exist without a parent?", options: ["Lookup", "Master-Detail", "Hierarchical", "Self"], correct: 0 },
        { id: "sf_f6", type: "mcq", marks: 5, question: "What is a Salesforce App?", options: ["A collection of tabs that work together for a business need", "A mobile phone only", "A type of report", "A database backup"], correct: 0 },
        { id: "sf_f7", type: "mcq", marks: 5, question: "What is a Custom Object used for?", options: ["Storing information unique to your organization", "Only for admins to log in", "Styling the page", "Sending emails"], correct: 0 },
        { id: "sf_f8", type: "mcq", marks: 5, question: "What is a Validation Rule used for?", options: ["Ensuring data entered meets certain criteria before saving", "Deleting bad data automatically", "Only for reports", "Styling fields"], correct: 0 },
        { id: "sf_f9", type: "mcq", marks: 5, question: "What is a Report used for in Salesforce?", options: ["Displaying and analyzing data in rows and summaries", "Sending automatic emails only", "Creating new users", "Changing field types"], correct: 0 },
        { id: "sf_f10", type: "mcq", marks: 5, question: "Which of these is a Salesforce cloud product?", options: ["Sales Cloud", "Docker Cloud", "React Cloud", "SQL Cloud"], correct: 0 },
        { id: "sf_f11", type: "coding", marks: 25, question: "Write a simple Apex trigger that updates a checkbox field 'Is_Active__c' to true when a Contact is created. (Minimum 50 characters)", language: "apex", minLength: 50 },
        { id: "sf_f12", type: "coding", marks: 25, question: "Write a SOQL query to fetch all Accounts where Industry = 'Technology' and limit the results to 10 records. (Minimum 50 characters)", language: "soql", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "sf_i1", type: "mcq", marks: 4, question: "What is Salesforce?", options: ["CRM Platform", "Database only", "Programming language", "Operating System"], correct: 0 },
        { id: "sf_i2", type: "mcq", marks: 4, question: "Which cloud is used for sales processes?", options: ["Sales Cloud", "Service Cloud", "Marketing Cloud", "Commerce Cloud"], correct: 0 },
        { id: "sf_i3", type: "mcq", marks: 4, question: "What is a Lead in Salesforce?", options: ["Potential customer", "Existing customer", "Product", "Invoice"], correct: 0 },
        { id: "sf_i4", type: "mcq", marks: 4, question: "What does CRM stand for?", options: ["Customer Relationship Management", "Customer Resource Management", "Company Resource Management", "Client Relationship Module"], correct: 0 },
        { id: "sf_i5", type: "mcq", marks: 4, question: "What is a Report in Salesforce used for?", options: ["Analyzing data", "Sending emails only", "Creating users", "Changing page layouts"], correct: 0 },
        { id: "sf_i6", type: "mcq", marks: 4, question: "What is an Account in Salesforce?", options: ["A company or organization you do business with", "A user login", "A report type", "A field type"], correct: 0 },
        { id: "sf_i7", type: "mcq", marks: 4, question: "What is a Contact in Salesforce?", options: ["An individual person, usually linked to an Account", "A company", "A workflow", "A dashboard"], correct: 0 },
        { id: "sf_i8", type: "mcq", marks: 4, question: "What is an Opportunity in Salesforce?", options: ["A potential sale or deal being tracked", "A support ticket", "A user profile", "A page layout"], correct: 0 },
        { id: "sf_i9", type: "mcq", marks: 4, question: "What is a Tab in Salesforce used for?", options: ["Navigating to a specific object's data", "Formatting text", "Deleting records", "Sending emails"], correct: 0 },
        { id: "sf_i10", type: "mcq", marks: 4, question: "What is the App Launcher used for?", options: ["Switching between different Salesforce apps", "Deleting apps", "Installing themes", "Backing up data"], correct: 0 },
        { id: "sf_i11", type: "mcq", marks: 4, question: "What is a List View?", options: ["A filtered list of records shown on an object tab", "A type of chart", "A user permission", "A backup file"], correct: 0 },
        { id: "sf_i12", type: "mcq", marks: 4, question: "What is the Setup menu used for?", options: ["Configuring and customizing your Salesforce org", "Logging out", "Creating reports only", "Sending bulk emails"], correct: 0 },
        { id: "sf_i13", type: "mcq", marks: 4, question: "Which license type lets a person log in to Salesforce?", options: ["User License", "Report License", "Field License", "Tab License"], correct: 0 },
        { id: "sf_i14", type: "mcq", marks: 4, question: "What is a Sandbox used for?", options: ["A copy of your org for testing without affecting real data", "Permanent storage of production data", "A type of report", "A mobile app"], correct: 0 },
        { id: "sf_i15", type: "mcq", marks: 4, question: "What is Chatter in Salesforce?", options: ["A collaboration tool for sharing updates within the org", "A reporting tool", "A billing feature", "A security setting"], correct: 0 },
        { id: "sf_i16", type: "mcq", marks: 4, question: "What is a Dashboard used for?", options: ["Visual summary of report data", "Storing files", "Sending SMS", "Creating users"], correct: 0 },
        { id: "sf_i17", type: "mcq", marks: 4, question: "What is the difference between a Standard and Custom field?", options: ["Standard fields come built-in; custom fields are created by users", "They are identical", "Custom fields cannot be required", "Standard fields cannot be edited"], correct: 0 },
        { id: "sf_i18", type: "mcq", marks: 4, question: "What is Data Loader used for?", options: ["Bulk import/export of data into/out of Salesforce", "Designing page layouts", "Writing Apex code", "Creating flows"], correct: 0 },
        { id: "sf_i19", type: "mcq", marks: 4, question: "What is a Formula Field?", options: ["A read-only field that automatically calculates a value", "A field that stores files", "A required text field", "A login field"], correct: 0 },
        { id: "sf_i20", type: "mcq", marks: 4, question: "What is the AppExchange?", options: ["A marketplace for Salesforce apps and add-ons", "A type of report", "A field type", "A user role"], correct: 0 },
        { id: "sf_i21", type: "mcq", marks: 4, question: "What is Salesforce Lightning?", options: ["The modern user interface and framework for Salesforce", "A database engine", "A type of email", "A billing plan"], correct: 0 },
        { id: "sf_i22", type: "mcq", marks: 4, question: "What is a Case used for?", options: ["Tracking a customer's issue or support request", "Tracking a sale", "Tracking an employee", "Tracking a login"], correct: 0 },
        { id: "sf_i23", type: "mcq", marks: 4, question: "What is a Campaign in Salesforce?", options: ["A marketing initiative used to track outreach and its results", "A security policy", "A backup schedule", "A user group"], correct: 0 },
        { id: "sf_i24", type: "mcq", marks: 4, question: "What is the purpose of Duplicate Rules?", options: ["Prevent or warn about duplicate records being created", "Speed up reports", "Encrypt data", "Send notifications only"], correct: 0 },
        { id: "sf_i25", type: "mcq", marks: 4, question: "What is a Queue used for in Salesforce?", options: ["A holding area where records wait to be assigned to users", "A type of report", "A backup location", "A field type"], correct: 0 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "sf_e1", type: "mcq", marks: 5, question: "What is the governor limit for SOQL queries in a synchronous transaction?", options: ["100", "50", "200", "150"], correct: 0 },
        { id: "sf_e2", type: "mcq", marks: 5, question: "Which design pattern is commonly used in Apex triggers?", options: ["Trigger Handler / Helper", "Singleton only", "MVC only", "Factory only"], correct: 0 },
        { id: "sf_e3", type: "mcq", marks: 5, question: "What is the purpose of Platform Cache?", options: ["Store frequently accessed data to reduce SOQL/API calls", "Store user sessions only", "Replace custom settings", "Only for Visualforce"], correct: 0 },
        { id: "sf_e4", type: "mcq", marks: 5, question: "In a master-detail relationship, what happens when the master is deleted?", options: ["All detail records are deleted", "Detail records become orphans", "Detail records are reparented automatically", "Nothing"], correct: 0 },
        { id: "sf_e5", type: "mcq", marks: 5, question: "What is a Record Type used for?", options: ["Offering different business processes/picklist values on the same object", "Renaming an object", "Changing field data types", "Backing up records"], correct: 0 },
        { id: "sf_e6", type: "mcq", marks: 5, question: "What is the purpose of Apex Governor Limits?", options: ["Ensure no single execution monopolizes shared platform resources", "Slow down bad code", "Limit the number of users", "Restrict login hours"], correct: 0 },
        { id: "sf_e7", type: "mcq", marks: 5, question: "What does the Trigger.new context variable represent?", options: ["The list of new versions of records being inserted or updated", "The old version of records before update", "The current logged in user", "The org's field metadata"], correct: 0 },
        { id: "sf_e8", type: "mcq", marks: 5, question: "What is the key difference between Workflow Rules and Process Builder?", options: ["Process Builder can do more actions (like creating records) and supports more complex logic", "They are exactly identical", "Workflow Rules are newer", "Process Builder cannot send emails"], correct: 0 },
        { id: "sf_e9", type: "mcq", marks: 5, question: "What is SOSL primarily used for?", options: ["Searching text across multiple objects and fields at once", "Deleting multiple records", "Creating page layouts", "Managing user permissions"], correct: 0 },
        { id: "sf_e10", type: "mcq", marks: 5, question: "What is a Change Set used for?", options: ["Deploying metadata changes between related Salesforce orgs", "Backing up data records", "Creating reports", "Managing user passwords"], correct: 0 },
        { id: "sf_e11", type: "coding", marks: 25, question: "Write a simple Apex class with one method that takes an Account Id and returns the count of related Contacts. (Minimum 50 characters)", language: "apex", minLength: 50 },
        { id: "sf_e12", type: "coding", marks: 25, question: "Write a basic Lightning Web Component (LWC) that displays a list of Account names (mock data is fine). (Minimum 50 characters)", language: "javascript", minLength: 50 }
      ]
    }
  },

  testing: {
    fresher: {
      duration: 45,
      questions: [
        { id: "t_f1", type: "mcq", marks: 5, question: "What is the difference between Verification and Validation?", options: ["Verification: are we building the product right? Validation: are we building the right product?", "They are the same", "Verification is only manual", "Validation is only automated"], correct: 0 },
        { id: "t_f2", type: "mcq", marks: 5, question: "Which is a black-box testing technique?", options: ["Equivalence Partitioning", "Statement Coverage", "Path Coverage", "Mutation Testing"], correct: 0 },
        { id: "t_f3", type: "mcq", marks: 5, question: "What does STLC stand for?", options: ["Software Testing Life Cycle", "System Testing Life Cycle", "Software Test Logic Cycle", "Standard Testing Life Cycle"], correct: 0 },
        { id: "t_f4", type: "mcq", marks: 5, question: "What is a Test Case?", options: ["A set of conditions to verify a feature", "A bug report", "A requirement document", "A code module"], correct: 0 },
        { id: "t_f5", type: "mcq", marks: 5, question: "Which tool is commonly used for API testing?", options: ["Postman", "Photoshop", "Excel only", "Word"], correct: 0 },
        { id: "t_f6", type: "mcq", marks: 5, question: "What is Regression Testing?", options: ["Testing to ensure new changes don't break existing functionality", "Testing only new features", "Performance testing", "Security testing only"], correct: 0 },
        { id: "t_f7", type: "mcq", marks: 5, question: "What is a Test Plan?", options: ["A document describing scope, approach and schedule of testing", "A single test case", "A bug report", "Source code"], correct: 0 },
        { id: "t_f8", type: "mcq", marks: 5, question: "What is Smoke Testing?", options: ["A quick check that the build is stable enough for further testing", "Full regression testing", "Only security testing", "Only load testing"], correct: 0 },
        { id: "t_f9", type: "mcq", marks: 5, question: "What is the purpose of a Bug Report?", options: ["Document a defect so it can be reproduced and fixed", "Track employee attendance", "Track project budget", "Design the UI"], correct: 0 },
        { id: "t_f10", type: "mcq", marks: 5, question: "Which of the following is a type of Functional Testing?", options: ["Unit Testing", "Load Testing", "Stress Testing", "Volume Testing"], correct: 0 },
        { id: "t_f11", type: "coding", marks: 25, question: "Write a simple Selenium (Python or Java) code snippet to open Google and search for 'Software Testing'. (Minimum 50 characters)", language: "python", minLength: 50 },
        { id: "t_f12", type: "coding", marks: 25, question: "Write step-by-step manual test cases for testing a Login page (username, password, submit, error messages). (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "t_i1", type: "mcq", marks: 4, question: "What is Software Testing?", options: ["Process of evaluating software to find defects", "Writing code", "Designing UI", "Deploying software"], correct: 0 },
        { id: "t_i2", type: "mcq", marks: 4, question: "What is a Bug?", options: ["A defect in the software", "A feature", "A requirement", "A test case"], correct: 0 },
        { id: "t_i3", type: "mcq", marks: 4, question: "Which is functional testing?", options: ["Unit Testing", "Load Testing", "Stress Testing", "Volume Testing"], correct: 0 },
        { id: "t_i4", type: "mcq", marks: 4, question: "What is Smoke Testing?", options: ["Basic testing to check if build is stable", "Full regression", "Performance testing", "Security testing"], correct: 0 },
        { id: "t_i5", type: "mcq", marks: 4, question: "What is Manual Testing?", options: ["Testing software by hand without automation tools", "Testing done only by machines", "Only reading documentation", "Only writing code"], correct: 0 },
        { id: "t_i6", type: "mcq", marks: 4, question: "What is a Test Scenario?", options: ["A high-level idea of what to test", "A bug fix", "A line of code", "A database table"], correct: 0 },
        { id: "t_i7", type: "mcq", marks: 4, question: "What is the purpose of Test Data?", options: ["Input values used to execute a test case", "The final report", "A type of bug", "A tool name"], correct: 0 },
        { id: "t_i8", type: "mcq", marks: 4, question: "What does UAT stand for?", options: ["User Acceptance Testing", "Unit Application Testing", "Universal Automated Testing", "User Automated Testing"], correct: 0 },
        { id: "t_i9", type: "mcq", marks: 4, question: "What is a Test Environment?", options: ["A setup of hardware/software where testing is performed", "The developer's laptop only", "A type of bug", "A design document"], correct: 0 },
        { id: "t_i10", type: "mcq", marks: 4, question: "What is Exploratory Testing?", options: ["Testing without predefined test cases, based on exploration", "Only automated testing", "Testing only the database", "Testing only performance"], correct: 0 },
        { id: "t_i11", type: "mcq", marks: 4, question: "What is a Defect Life Cycle?", options: ["The stages a bug goes through from reporting to closure", "The stages of software development", "The stages of a project", "The stages of an interview"], correct: 0 },
        { id: "t_i12", type: "mcq", marks: 4, question: "What does the term 'Sanity Testing' mean?", options: ["A quick check that a specific function works after a minor change", "A full regression cycle", "Only load testing", "Only UI testing"], correct: 0 },
        { id: "t_i13", type: "mcq", marks: 4, question: "What is the difference between Severity and Priority?", options: ["Severity is the impact of a bug; Priority is the order in which it should be fixed", "They mean the same thing", "Severity is set by testers only", "Priority is set by testers only"], correct: 0 },
        { id: "t_i14", type: "mcq", marks: 4, question: "What is a Test Suite?", options: ["A collection of test cases grouped together", "A single test case", "A bug tracking tool", "A programming language"], correct: 0 },
        { id: "t_i15", type: "mcq", marks: 4, question: "What is White Box Testing?", options: ["Testing based on internal code structure", "Testing based only on requirements", "Testing only the UI", "Testing only performance"], correct: 0 },
        { id: "t_i16", type: "mcq", marks: 4, question: "What is Black Box Testing?", options: ["Testing without knowledge of internal code, based on inputs/outputs", "Testing only the source code", "Testing only databases", "Testing only APIs"], correct: 0 },
        { id: "t_i17", type: "mcq", marks: 4, question: "Which of these is an automation testing tool?", options: ["Selenium", "MS Paint", "Notepad", "Calculator"], correct: 0 },
        { id: "t_i18", type: "mcq", marks: 4, question: "What is a Test Script?", options: ["A set of instructions to be performed on the system to test a function", "A bug", "A requirement", "A meeting note"], correct: 0 },
        { id: "t_i19", type: "mcq", marks: 4, question: "What is Boundary Value Analysis?", options: ["Testing at the edges of valid input ranges", "Testing only positive numbers", "Testing only the UI colors", "Testing only during release"], correct: 0 },
        { id: "t_i20", type: "mcq", marks: 4, question: "What is a Checklist in testing?", options: ["A list of items to verify without detailed steps", "A bug tracker", "A programming tool", "A type of database"], correct: 0 },
        { id: "t_i21", type: "mcq", marks: 4, question: "What does API stand for (in the context of API testing)?", options: ["Application Programming Interface", "Automated Program Inspection", "Application Process Instruction", "None of these"], correct: 0 },
        { id: "t_i22", type: "mcq", marks: 4, question: "What is Retesting?", options: ["Verifying that a specific reported bug has been fixed", "Testing a brand-new feature only", "Testing performance only", "Testing security only"], correct: 0 },
        { id: "t_i23", type: "mcq", marks: 4, question: "What is a Traceability Matrix used for?", options: ["Mapping requirements to test cases to ensure coverage", "Tracking employee hours", "Tracking server uptime", "Tracking code commits"], correct: 0 },
        { id: "t_i24", type: "mcq", marks: 4, question: "What is Usability Testing?", options: ["Testing how easy and user-friendly the application is", "Testing server load", "Testing database backups", "Testing network speed"], correct: 0 },
        { id: "t_i25", type: "mcq", marks: 4, question: "What is the main goal of Software Testing overall?", options: ["Finding defects and ensuring quality before release", "Writing new features", "Designing the database", "Managing the budget"], correct: 0 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "t_e1", type: "mcq", marks: 5, question: "What is the difference between Severity and Priority?", options: ["Severity: impact on system, Priority: order of fixing", "They are the same", "Severity is only for critical bugs", "Priority is decided by developers only"], correct: 0 },
        { id: "t_e2", type: "mcq", marks: 5, question: "Which framework is commonly used with Selenium?", options: ["TestNG / JUnit / PyTest", "Only React", "Only Spring", "Only Django"], correct: 0 },
        { id: "t_e3", type: "mcq", marks: 5, question: "What is Shift-Left Testing?", options: ["Testing early in the development cycle", "Testing only at the end", "Only performance testing", "Only security testing"], correct: 0 },
        { id: "t_e4", type: "mcq", marks: 5, question: "What is the purpose of a Test Plan?", options: ["Document scope, approach, resources and schedule of testing", "Only list test cases", "Only bug reports", "Code documentation"], correct: 0 },
        { id: "t_e5", type: "mcq", marks: 5, question: "What is a Page Object Model (POM)?", options: ["A design pattern that separates page structure from test logic", "A database schema", "A type of bug", "A CI/CD tool"], correct: 0 },
        { id: "t_e6", type: "mcq", marks: 5, question: "What is Data-Driven Testing?", options: ["Running the same test with multiple sets of input data", "Testing only the database", "Testing without any data", "Manual testing only"], correct: 0 },
        { id: "t_e7", type: "mcq", marks: 5, question: "What is Continuous Testing?", options: ["Running automated tests as part of the CI/CD pipeline", "Testing manually every day", "Testing only before release", "Testing only the UI"], correct: 0 },
        { id: "t_e8", type: "mcq", marks: 5, question: "What is the purpose of a CI/CD pipeline in testing?", options: ["Automatically build, test and deploy code changes", "Only to write documentation", "Only for design reviews", "Only for hiring"], correct: 0 },
        { id: "t_e9", type: "mcq", marks: 5, question: "What is Load Testing used for?", options: ["Checking system behavior under expected user load", "Checking UI colors", "Checking spelling errors", "Checking database backups only"], correct: 0 },
        { id: "t_e10", type: "mcq", marks: 5, question: "What is Mocking in test automation?", options: ["Simulating a dependency's behavior for isolated testing", "Deleting test data", "Writing manual test cases", "Designing the UI"], correct: 0 },
        { id: "t_e11", type: "coding", marks: 25, question: "Write a simple Page Object Model example for a Login page in Selenium (any language), including one locator and one method. (Minimum 50 characters)", language: "java", minLength: 50 },
        { id: "t_e12", type: "coding", marks: 25, question: "Write a simple API test (using RestAssured or Python requests) to check that a GET request returns status code 200. (Minimum 50 characters)", language: "java", minLength: 50 }
      ]
    }
  },

  database: {
    fresher: {
      duration: 45,
      questions: [
        { id: "db_f1", type: "mcq", marks: 5, question: "What does ACID stand for in databases?", options: ["Atomicity, Consistency, Isolation, Durability", "Availability, Consistency, Integrity, Durability", "Atomicity, Concurrency, Isolation, Durability", "None"], correct: 0 },
        { id: "db_f2", type: "mcq", marks: 5, question: "Which SQL command is used to retrieve data?", options: ["SELECT", "INSERT", "UPDATE", "DELETE"], correct: 0 },
        { id: "db_f3", type: "mcq", marks: 5, question: "What is a Primary Key?", options: ["Unique identifier for a record", "Foreign key", "Index only", "View"], correct: 0 },
        { id: "db_f4", type: "mcq", marks: 5, question: "What is Normalization?", options: ["Process of organizing data to reduce redundancy", "Adding more tables", "Denormalization", "Indexing only"], correct: 0 },
        { id: "db_f5", type: "mcq", marks: 5, question: "Which join returns only matching records from both tables?", options: ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"], correct: 0 },
        { id: "db_f6", type: "mcq", marks: 5, question: "What is an Index used for?", options: ["Speed up data retrieval", "Store data", "Delete data", "Backup"], correct: 0 },
        { id: "db_f7", type: "mcq", marks: 5, question: "What is a Foreign Key?", options: ["A field that links to the Primary Key of another table", "A key that is never used", "A type of index", "A backup file"], correct: 0 },
        { id: "db_f8", type: "mcq", marks: 5, question: "What does DDL stand for?", options: ["Data Definition Language", "Data Digging Language", "Data Design Language", "Data Development Language"], correct: 0 },
        { id: "db_f9", type: "mcq", marks: 5, question: "What does DML stand for?", options: ["Data Manipulation Language", "Data Modeling Language", "Data Migration Language", "Database Management Language"], correct: 0 },
        { id: "db_f10", type: "mcq", marks: 5, question: "Which of these is a relational database?", options: ["MySQL", "MongoDB", "Redis", "Cassandra"], correct: 0 },
        { id: "db_f11", type: "coding", marks: 25, question: "Write a SQL query to find the second highest salary from an Employee table (assume columns: id, name, salary). (Minimum 50 characters)", language: "sql", minLength: 50 },
        { id: "db_f12", type: "coding", marks: 25, question: "Write SQL to create a table Employees with columns id (PK), name, department, salary and insert 2 sample rows. (Minimum 50 characters)", language: "sql", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "db_i1", type: "mcq", marks: 4, question: "What is a Database?", options: ["Organized collection of data", "A programming language", "An operating system", "A web server"], correct: 0 },
        { id: "db_i2", type: "mcq", marks: 4, question: "Which is a relational database?", options: ["MySQL", "MongoDB", "Redis", "Cassandra"], correct: 0 },
        { id: "db_i3", type: "mcq", marks: 4, question: "What does DDL stand for?", options: ["Data Definition Language", "Data Digging Language", "Data Design Language", "Data Development Language"], correct: 0 },
        { id: "db_i4", type: "mcq", marks: 4, question: "What is a Foreign Key?", options: ["A key that links two tables", "Primary key of same table", "An index", "A view"], correct: 0 },
        { id: "db_i5", type: "mcq", marks: 4, question: "What is a Table in a database?", options: ["A structure that organizes data into rows and columns", "A type of chart", "A backup file", "A user account"], correct: 0 },
        { id: "db_i6", type: "mcq", marks: 4, question: "What is a Row (Record) in a table?", options: ["A single entry of data in a table", "A column name", "A database itself", "An index"], correct: 0 },
        { id: "db_i7", type: "mcq", marks: 4, question: "What is a Column (Field) in a table?", options: ["An attribute that stores a specific type of data", "A single record", "A database backup", "A user permission"], correct: 0 },
        { id: "db_i8", type: "mcq", marks: 4, question: "What is the WHERE clause used for?", options: ["Filtering rows based on a condition", "Sorting results", "Creating a table", "Deleting a database"], correct: 0 },
        { id: "db_i9", type: "mcq", marks: 4, question: "What is the ORDER BY clause used for?", options: ["Sorting the result set", "Filtering rows", "Joining tables", "Creating an index"], correct: 0 },
        { id: "db_i10", type: "mcq", marks: 4, question: "What does SQL stand for?", options: ["Structured Query Language", "Structured Question Language", "Simple Query Language", "System Query Language"], correct: 0 },
        { id: "db_i11", type: "mcq", marks: 4, question: "What is a Primary Key used for?", options: ["Uniquely identifying each row in a table", "Storing large text", "Formatting output", "Connecting to the internet"], correct: 0 },
        { id: "db_i12", type: "mcq", marks: 4, question: "What is a View in SQL?", options: ["A virtual table based on the result of a query", "A physical backup", "A user login", "A type of index"], correct: 0 },
        { id: "db_i13", type: "mcq", marks: 4, question: "What command is used to add a new row to a table?", options: ["INSERT", "SELECT", "UPDATE", "DROP"], correct: 0 },
        { id: "db_i14", type: "mcq", marks: 4, question: "What command is used to remove a table entirely?", options: ["DROP TABLE", "DELETE TABLE", "REMOVE TABLE", "CLEAR TABLE"], correct: 0 },
        { id: "db_i15", type: "mcq", marks: 4, question: "What is the difference between DELETE and TRUNCATE?", options: ["DELETE removes rows one by one and can be rolled back; TRUNCATE removes all rows quickly", "They are exactly the same", "TRUNCATE only works on views", "DELETE cannot use a WHERE clause"], correct: 0 },
        { id: "db_i16", type: "mcq", marks: 4, question: "What is a Composite Key?", options: ["A primary key made of two or more columns", "A key with no value", "A type of index only", "A backup key"], correct: 0 },
        { id: "db_i17", type: "mcq", marks: 4, question: "What does NULL represent in a database?", options: ["An unknown or missing value", "The number zero", "An empty string always", "A deleted row"], correct: 0 },
        { id: "db_i18", type: "mcq", marks: 4, question: "What is a Constraint in SQL?", options: ["A rule enforced on data columns (e.g. NOT NULL, UNIQUE)", "A type of report", "A backup schedule", "A user role"], correct: 0 },
        { id: "db_i19", type: "mcq", marks: 4, question: "What is the purpose of the GROUP BY clause?", options: ["Grouping rows that share a value to apply aggregate functions", "Sorting rows alphabetically", "Filtering duplicate tables", "Creating a new database"], correct: 0 },
        { id: "db_i20", type: "mcq", marks: 4, question: "Which aggregate function returns the number of rows?", options: ["COUNT()", "SUM()", "AVG()", "MAX()"], correct: 0 },
        { id: "db_i21", type: "mcq", marks: 4, question: "What is a Schema in a database?", options: ["The structure/blueprint that defines tables and relationships", "A single row of data", "A backup file", "A user password"], correct: 0 },
        { id: "db_i22", type: "mcq", marks: 4, question: "What is Denormalization?", options: ["Combining tables to improve read performance, allowing some redundancy", "Removing all data", "Encrypting a database", "Deleting indexes"], correct: 0 },
        { id: "db_i23", type: "mcq", marks: 4, question: "What is a Transaction in a database?", options: ["A sequence of operations performed as a single logical unit of work", "A single SELECT statement only", "A type of index", "A user login session"], correct: 0 },
        { id: "db_i24", type: "mcq", marks: 4, question: "What is Backup used for in databases?", options: ["Creating a copy of data to restore in case of loss", "Speeding up queries", "Formatting tables", "Creating users"], correct: 0 },
        { id: "db_i25", type: "mcq", marks: 4, question: "What is the difference between CHAR and VARCHAR data types?", options: ["CHAR is fixed-length, VARCHAR is variable-length", "They are identical", "VARCHAR only stores numbers", "CHAR only stores dates"], correct: 0 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "db_e1", type: "mcq", marks: 5, question: "What is the difference between Clustered and Non-Clustered Index?", options: ["Clustered determines physical order of data, Non-clustered is separate structure", "They are the same", "Non-clustered is always faster", "Clustered can be multiple"], correct: 0 },
        { id: "db_e2", type: "mcq", marks: 5, question: "What is a Deadlock?", options: ["Two transactions waiting for each other to release locks", "A crashed database", "Slow query", "Missing index"], correct: 0 },
        { id: "db_e3", type: "mcq", marks: 5, question: "What is CAP Theorem?", options: ["Consistency, Availability, Partition tolerance", "Concurrency, Atomicity, Performance", "Cache, API, Performance", "None"], correct: 0 },
        { id: "db_e4", type: "mcq", marks: 5, question: "In PostgreSQL/MySQL, what is EXPLAIN used for?", options: ["Show query execution plan", "Execute the query", "Delete data", "Create index"], correct: 0 },
        { id: "db_e5", type: "mcq", marks: 5, question: "What is a Stored Procedure?", options: ["A precompiled set of SQL statements stored in the database", "A backup file", "A type of index", "A user role"], correct: 0 },
        { id: "db_e6", type: "mcq", marks: 5, question: "What is Database Sharding?", options: ["Splitting a database into smaller pieces spread across multiple servers", "Backing up a database", "Deleting old data", "Encrypting passwords"], correct: 0 },
        { id: "db_e7", type: "mcq", marks: 5, question: "What is Database Replication?", options: ["Copying and maintaining data across multiple database servers", "Deleting duplicate rows", "Compressing a table", "Creating an index"], correct: 0 },
        { id: "db_e8", type: "mcq", marks: 5, question: "What is the purpose of Database Isolation Levels?", options: ["Control how transaction changes are visible to other transactions", "Control who can log in", "Control table names", "Control backup schedules"], correct: 0 },
        { id: "db_e9", type: "mcq", marks: 5, question: "What is a Materialized View?", options: ["A view whose results are physically stored and periodically refreshed", "A view that is never stored", "A type of index only", "A backup command"], correct: 0 },
        { id: "db_e10", type: "mcq", marks: 5, question: "What is Query Optimization?", options: ["The process of improving a query's performance", "Renaming tables", "Deleting all indexes", "Encrypting data"], correct: 0 },
        { id: "db_e11", type: "coding", marks: 25, question: "Write a query to find employees who earn more than their managers using a self-join. (Minimum 50 characters)", language: "sql", minLength: 50 },
        { id: "db_e12", type: "coding", marks: 25, question: "Write an example using a window function (ROW_NUMBER or RANK) to rank employees by salary within each department. (Minimum 50 characters)", language: "sql", minLength: 50 }
      ]
    }
  },

  integration: {
    fresher: {
      duration: 45,
      questions: [
        { id: "int_f1", type: "mcq", marks: 5, question: "What is an API?", options: ["Application Programming Interface", "Application Process Integration", "Automated Program Interface", "None"], correct: 0 },
        { id: "int_f2", type: "mcq", marks: 5, question: "Which protocol is commonly used for web APIs?", options: ["HTTP/HTTPS", "FTP only", "SMTP", "SSH"], correct: 0 },
        { id: "int_f3", type: "mcq", marks: 5, question: "What does REST stand for?", options: ["Representational State Transfer", "Remote Execution State Transfer", "Relational State Transfer", "None"], correct: 0 },
        { id: "int_f4", type: "mcq", marks: 5, question: "What is JSON commonly used for?", options: ["Data exchange format", "Database only", "Styling pages", "Compiling code"], correct: 0 },
        { id: "int_f5", type: "mcq", marks: 5, question: "What is Middleware in integration?", options: ["Software that connects different applications", "A database", "A frontend framework", "An operating system"], correct: 0 },
        { id: "int_f6", type: "mcq", marks: 5, question: "What is an API Endpoint?", options: ["A specific URL where an API can be accessed", "A database table", "A UI button", "A server room"], correct: 0 },
        { id: "int_f7", type: "mcq", marks: 5, question: "Which HTTP method is typically used to retrieve data?", options: ["GET", "DELETE", "PATCH", "PUT"], correct: 0 },
        { id: "int_f8", type: "mcq", marks: 5, question: "Which HTTP status code generally means success?", options: ["200", "404", "500", "301"], correct: 0 },
        { id: "int_f9", type: "mcq", marks: 5, question: "What is Authentication in the context of APIs?", options: ["Verifying the identity of the caller before granting access", "Formatting the response", "Compressing data", "Logging errors only"], correct: 0 },
        { id: "int_f10", type: "mcq", marks: 5, question: "What is an API Key used for?", options: ["Identifying and authorizing the calling application", "Styling a webpage", "Storing files", "Creating a database"], correct: 0 },
        { id: "int_f11", type: "coding", marks: 25, question: "Write a simple REST API call (using fetch, axios or curl) to GET data from an endpoint and log the response. (Minimum 50 characters)", language: "javascript", minLength: 50 },
        { id: "int_f12", type: "coding", marks: 25, question: "Explain the difference between SOAP and REST with one example each. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "int_i1", type: "mcq", marks: 4, question: "What is Integration in software?", options: ["Connecting different systems to work together", "Writing UI", "Database design", "Testing only"], correct: 0 },
        { id: "int_i2", type: "mcq", marks: 4, question: "What is an API endpoint?", options: ["A specific URL where an API can be accessed", "A database table", "A UI button", "A server room"], correct: 0 },
        { id: "int_i3", type: "mcq", marks: 4, question: "Which status code means success?", options: ["200", "404", "500", "301"], correct: 0 },
        { id: "int_i4", type: "mcq", marks: 4, question: "What does HTTP POST typically do?", options: ["Create or submit data", "Only read data", "Delete data", "Update only"], correct: 0 },
        { id: "int_i5", type: "mcq", marks: 4, question: "What does HTTP GET typically do?", options: ["Retrieve data from a server", "Delete data", "Create new data only", "Change server settings"], correct: 0 },
        { id: "int_i6", type: "mcq", marks: 4, question: "What does HTTP DELETE typically do?", options: ["Remove a resource from the server", "Retrieve data", "Create a new resource", "Update partially"], correct: 0 },
        { id: "int_i7", type: "mcq", marks: 4, question: "What is a Request Header used for?", options: ["Sending metadata like content type or authentication with a request", "Storing the response body", "Displaying the UI", "Compiling code"], correct: 0 },
        { id: "int_i8", type: "mcq", marks: 4, question: "What does XML stand for?", options: ["eXtensible Markup Language", "eXtra Modern Language", "eXecutable Markup Language", "None"], correct: 0 },
        { id: "int_i9", type: "mcq", marks: 4, question: "What is a Webhook?", options: ["A callback URL that receives data when an event happens", "A type of database", "A programming language", "A firewall rule"], correct: 0 },
        { id: "int_i10", type: "mcq", marks: 4, question: "What is API Rate Limiting?", options: ["Restricting the number of requests a client can make in a period", "Increasing server speed", "Formatting JSON", "Encrypting passwords"], correct: 0 },
        { id: "int_i11", type: "mcq", marks: 4, question: "What is the purpose of an API Gateway?", options: ["A single entry point that manages and routes API requests", "A database backup tool", "A CSS framework", "A code editor"], correct: 0 },
        { id: "int_i12", type: "mcq", marks: 4, question: "What does CRUD stand for?", options: ["Create, Read, Update, Delete", "Create, Run, Undo, Delete", "Copy, Read, Update, Duplicate", "None"], correct: 0 },
        { id: "int_i13", type: "mcq", marks: 4, question: "What is a Payload in an API request?", options: ["The actual data sent in the body of the request", "The URL only", "The response time", "The server name"], correct: 0 },
        { id: "int_i14", type: "mcq", marks: 4, question: "What is the purpose of an API Key?", options: ["Identify and authorize the application making the request", "Style the webpage", "Store user passwords in plain text", "Create backups"], correct: 0 },
        { id: "int_i15", type: "mcq", marks: 4, question: "What does OAuth provide?", options: ["A standard for authorization and secure access delegation", "A database engine", "A CSS library", "A testing tool"], correct: 0 },
        { id: "int_i16", type: "mcq", marks: 4, question: "What is a Timeout in an API call?", options: ["The maximum time to wait for a response before giving up", "The time a server has been running", "The time zone setting", "A type of error only in databases"], correct: 0 },
        { id: "int_i17", type: "mcq", marks: 4, question: "What is Data Mapping in integration?", options: ["Matching fields from one system's format to another's", "Deleting unused fields", "Designing the UI", "Compressing files"], correct: 0 },
        { id: "int_i18", type: "mcq", marks: 4, question: "What is a Flat File in integration contexts?", options: ["A plain text file (like CSV) used to exchange data", "A 3D file format", "A type of database index", "A compiled program"], correct: 0 },
        { id: "int_i19", type: "mcq", marks: 4, question: "What is Polling in integration?", options: ["Repeatedly checking a system for new data at intervals", "Sending one request and never checking again", "A type of encryption", "A database backup method"], correct: 0 },
        { id: "int_i20", type: "mcq", marks: 4, question: "What is the purpose of API versioning?", options: ["Allow changes to an API without breaking existing consumers", "Make APIs slower", "Remove authentication", "Delete old data automatically"], correct: 0 },
        { id: "int_i21", type: "mcq", marks: 4, question: "What is a Response Body?", options: ["The data returned by the server after a request", "The URL of the request", "The request headers only", "The client's IP address"], correct: 0 },
        { id: "int_i22", type: "mcq", marks: 4, question: "What is meant by 'stateless' in REST APIs?", options: ["Each request contains all information needed; the server stores no client session", "The server remembers every past request", "The API never returns errors", "The API has no endpoints"], correct: 0 },
        { id: "int_i23", type: "mcq", marks: 4, question: "What is a Sandbox environment used for in integration testing?", options: ["A safe test environment that mimics production without affecting real data", "The live production system", "A type of firewall", "A reporting dashboard"], correct: 0 },
        { id: "int_i24", type: "mcq", marks: 4, question: "What is Basic Authentication?", options: ["Sending a username and password with each request to authenticate", "A type of database index", "A CSS layout method", "A file compression technique"], correct: 0 },
        { id: "int_i25", type: "mcq", marks: 4, question: "What does 'idempotent' mean for an HTTP method like GET or PUT?", options: ["Making the same request multiple times has the same effect as making it once", "The request always fails the second time", "The request changes data every time", "The request requires no authentication"], correct: 0 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "int_e1", type: "mcq", marks: 5, question: "What is the difference between Synchronous and Asynchronous integration?", options: ["Sync waits for response, Async does not", "They are same", "Async is always slower", "Sync is only for batch"], correct: 0 },
        { id: "int_e2", type: "mcq", marks: 5, question: "What is an ESB?", options: ["Enterprise Service Bus", "Enterprise System Bridge", "External Service Broker", "None"], correct: 0 },
        { id: "int_e3", type: "mcq", marks: 5, question: "What is Idempotency in APIs?", options: ["Same request can be made multiple times without different effects", "Request can be made only once", "Only for GET", "Only for POST"], correct: 0 },
        { id: "int_e4", type: "mcq", marks: 5, question: "What is a Message Queue used for?", options: ["Decoupling systems and handling async communication", "Storing user sessions", "Rendering UI", "Compiling code"], correct: 0 },
        { id: "int_e5", type: "mcq", marks: 5, question: "What is Event-Driven Architecture?", options: ["A design where systems communicate by producing and consuming events", "A design with no communication between systems", "A UI design pattern only", "A database backup method"], correct: 0 },
        { id: "int_e6", type: "mcq", marks: 5, question: "What is the Circuit Breaker pattern used for?", options: ["Preventing repeated calls to a failing service to avoid cascading failures", "Speeding up successful requests", "Formatting JSON responses", "Encrypting data at rest"], correct: 0 },
        { id: "int_e7", type: "mcq", marks: 5, question: "What is API Throttling?", options: ["Limiting the rate of requests to protect backend systems", "Increasing server memory", "A type of database join", "A CSS technique"], correct: 0 },
        { id: "int_e8", type: "mcq", marks: 5, question: "What is the purpose of a Dead Letter Queue?", options: ["Storing messages that failed processing for later investigation", "Storing successful messages only", "Speeding up the main queue", "Encrypting queue messages"], correct: 0 },
        { id: "int_e9", type: "mcq", marks: 5, question: "What is the difference between Point-to-Point and Publish-Subscribe messaging?", options: ["Point-to-Point sends to one consumer; Pub-Sub broadcasts to many subscribers", "They are identical", "Pub-Sub only works with databases", "Point-to-Point cannot use queues"], correct: 0 },
        { id: "int_e10", type: "mcq", marks: 5, question: "What is API Orchestration?", options: ["Coordinating multiple API calls to complete a business process", "Deleting unused APIs", "A type of database index", "A CSS grid system"], correct: 0 },
        { id: "int_e11", type: "coding", marks: 25, question: "Design a simple message flow using a queue for order processing. Describe the producer and consumer, and include a short code snippet. (Minimum 50 characters)", language: "javascript", minLength: 50 },
        { id: "int_e12", type: "coding", marks: 25, question: "Explain how you would handle retries and error handling when one system calls another over an API. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    }
  },

  infra: {
    fresher: {
      duration: 45,
      questions: [
        { id: "inf_f1", type: "mcq", marks: 5, question: "What is a Virtual Machine?", options: ["Emulation of a computer system", "A physical server", "A programming language", "A database"], correct: 0 },
        { id: "inf_f2", type: "mcq", marks: 5, question: "What does CI/CD stand for?", options: ["Continuous Integration / Continuous Deployment", "Code Integration / Code Deployment", "Continuous Inspection / Continuous Delivery", "None"], correct: 0 },
        { id: "inf_f3", type: "mcq", marks: 5, question: "What is Kubernetes used for?", options: ["Container orchestration", "Database management", "Frontend framework", "Version control"], correct: 0 },
        { id: "inf_f4", type: "mcq", marks: 5, question: "What is Docker?", options: ["Containerization platform", "A programming language", "A database", "A cloud provider only"], correct: 0 },
        { id: "inf_f5", type: "mcq", marks: 5, question: "Which of the following is a cloud provider?", options: ["AWS", "MySQL", "React", "Git"], correct: 0 },
        { id: "inf_f6", type: "mcq", marks: 5, question: "What is a Firewall used for?", options: ["Controlling incoming and outgoing network traffic based on rules", "Speeding up a website", "Storing files", "Writing code"], correct: 0 },
        { id: "inf_f7", type: "mcq", marks: 5, question: "What is an Operating System?", options: ["Software that manages hardware and software resources of a computer", "A programming language", "A type of database", "A web browser"], correct: 0 },
        { id: "inf_f8", type: "mcq", marks: 5, question: "What is Git primarily used for?", options: ["Version control of source code", "Sending emails", "Managing servers only", "Designing UI"], correct: 0 },
        { id: "inf_f9", type: "mcq", marks: 5, question: "What does DNS stand for?", options: ["Domain Name System", "Data Network Service", "Digital Naming Standard", "None"], correct: 0 },
        { id: "inf_f10", type: "mcq", marks: 5, question: "What is the purpose of a Backup?", options: ["A copy of data kept to restore it in case of loss", "Speeding up a server", "Deleting old files", "Compiling code"], correct: 0 },
        { id: "inf_f11", type: "coding", marks: 25, question: "Write a simple Dockerfile for a Node.js application (FROM, WORKDIR, COPY, RUN, CMD). (Minimum 50 characters)", language: "dockerfile", minLength: 50 },
        { id: "inf_f12", type: "coding", marks: 25, question: "Explain the difference between a container and a virtual machine. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "inf_i1", type: "mcq", marks: 4, question: "What is Linux?", options: ["Open-source operating system", "A database", "A programming language", "A cloud provider"], correct: 0 },
        { id: "inf_i2", type: "mcq", marks: 4, question: "What is a Server?", options: ["A computer that provides services to other computers", "Only a desktop", "A mobile phone", "A browser"], correct: 0 },
        { id: "inf_i3", type: "mcq", marks: 4, question: "What does IP stand for?", options: ["Internet Protocol", "Internal Process", "Internet Provider", "Input Port"], correct: 0 },
        { id: "inf_i4", type: "mcq", marks: 4, question: "What is SSH used for?", options: ["Secure remote login", "Sending emails", "Browsing websites", "Playing videos"], correct: 0 },
        { id: "inf_i5", type: "mcq", marks: 4, question: "What command lists files in a Linux directory?", options: ["ls", "dir only", "list", "show"], correct: 0 },
        { id: "inf_i6", type: "mcq", marks: 4, question: "What command is used to change directories in Linux?", options: ["cd", "chdir only", "move", "goto"], correct: 0 },
        { id: "inf_i7", type: "mcq", marks: 4, question: "What is a Port in networking?", options: ["A numbered endpoint used to route network traffic to the right service", "A type of cable", "A backup file", "A programming keyword"], correct: 0 },
        { id: "inf_i8", type: "mcq", marks: 4, question: "What is the purpose of a Load Balancer?", options: ["Distributing traffic across multiple servers", "Storing data permanently", "Compiling code", "Formatting a disk"], correct: 0 },
        { id: "inf_i9", type: "mcq", marks: 4, question: "What is Cloud Computing?", options: ["Delivering computing resources (servers, storage) over the internet", "Only local storage on your PC", "A programming language", "A type of firewall"], correct: 0 },
        { id: "inf_i10", type: "mcq", marks: 4, question: "What is SaaS?", options: ["Software as a Service — using software hosted by a provider", "Server as a Service", "Storage as a Server", "None"], correct: 0 },
        { id: "inf_i11", type: "mcq", marks: 4, question: "What is PaaS?", options: ["Platform as a Service — a managed environment to build/run apps", "Personal as a Service", "Page as a Service", "None"], correct: 0 },
        { id: "inf_i12", type: "mcq", marks: 4, question: "What is IaaS?", options: ["Infrastructure as a Service — renting virtualized computing resources", "Internet as a Service", "Interface as a Service", "None"], correct: 0 },
        { id: "inf_i13", type: "mcq", marks: 4, question: "What is a Repository (repo) in Git?", options: ["A storage location for a project's code and history", "A type of server", "A firewall rule", "A backup schedule"], correct: 0 },
        { id: "inf_i14", type: "mcq", marks: 4, question: "What does 'git commit' do?", options: ["Saves a snapshot of changes to the local repository", "Deletes the repository", "Uploads a file to the cloud", "Creates a new server"], correct: 0 },
        { id: "inf_i15", type: "mcq", marks: 4, question: "What is Monitoring in infrastructure?", options: ["Continuously checking system health and performance", "Writing new features", "Designing the UI", "Testing only the database"], correct: 0 },
        { id: "inf_i16", type: "mcq", marks: 4, question: "What is Uptime?", options: ["The amount of time a system has been running without failure", "The time to boot a computer", "The speed of internet", "A type of backup"], correct: 0 },
        { id: "inf_i17", type: "mcq", marks: 4, question: "What is a Firewall?", options: ["A security system that controls network traffic based on rules", "A type of database", "A programming language", "A cloud storage service"], correct: 0 },
        { id: "inf_i18", type: "mcq", marks: 4, question: "What does 'sudo' do in Linux?", options: ["Run a command with elevated (administrator) privileges", "Delete a file permanently", "Shut down the system", "List running processes"], correct: 0 },
        { id: "inf_i19", type: "mcq", marks: 4, question: "What is a Package Manager (like apt or yum) used for?", options: ["Installing, updating and removing software packages", "Managing user passwords", "Designing web pages", "Writing test cases"], correct: 0 },
        { id: "inf_i20", type: "mcq", marks: 4, question: "What is Version Control used for?", options: ["Tracking and managing changes to code over time", "Formatting hard drives", "Sending emails", "Creating firewalls"], correct: 0 },
        { id: "inf_i21", type: "mcq", marks: 4, question: "What is a Log File?", options: ["A record of events generated by a system or application", "A type of database index", "A user password store", "A network cable type"], correct: 0 },
        { id: "inf_i22", type: "mcq", marks: 4, question: "What does 'ping' command check?", options: ["Whether a host is reachable over the network", "CPU temperature", "Disk space", "Installed software list"], correct: 0 },
        { id: "inf_i23", type: "mcq", marks: 4, question: "What is a Subnet?", options: ["A smaller, segmented portion of a larger network", "A type of server", "A programming loop", "A backup method"], correct: 0 },
        { id: "inf_i24", type: "mcq", marks: 4, question: "What is the purpose of an SSL/TLS certificate?", options: ["Encrypting data transmitted between a client and server", "Speeding up a CPU", "Formatting a disk", "Managing user roles only"], correct: 0 },
        { id: "inf_i25", type: "mcq", marks: 4, question: "What does 'automation' mean in an infra/DevOps context?", options: ["Using scripts/tools to perform repetitive tasks without manual effort", "Only using a mouse and keyboard", "Writing documentation only", "Manually configuring every server"], correct: 0 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "inf_e1", type: "mcq", marks: 5, question: "What is Infrastructure as Code (IaC)?", options: ["Managing infrastructure through code (Terraform, CloudFormation etc.)", "Manual server setup", "Only Docker", "Only monitoring"], correct: 0 },
        { id: "inf_e2", type: "mcq", marks: 5, question: "What is the difference between Horizontal and Vertical scaling?", options: ["Horizontal: add more machines, Vertical: increase resources of existing", "They are same", "Vertical is always better", "Horizontal only for databases"], correct: 0 },
        { id: "inf_e3", type: "mcq", marks: 5, question: "What is a Load Balancer?", options: ["Distributes incoming traffic across multiple servers", "A type of database", "A firewall only", "A monitoring tool"], correct: 0 },
        { id: "inf_e4", type: "mcq", marks: 5, question: "What is High Availability?", options: ["System designed to be operational continuously with minimal downtime", "Only fast performance", "Cheap infrastructure", "Single server setup"], correct: 0 },
        { id: "inf_e5", type: "mcq", marks: 5, question: "What is a Blue-Green Deployment?", options: ["Running two identical environments and switching traffic to the new one", "Deleting the old server immediately", "A type of database backup", "A firewall configuration"], correct: 0 },
        { id: "inf_e6", type: "mcq", marks: 5, question: "What is a Canary Release?", options: ["Rolling out a change to a small subset of users before full release", "Releasing to everyone at once", "A type of database index", "A backup strategy only"], correct: 0 },
        { id: "inf_e7", type: "mcq", marks: 5, question: "What is Configuration Management (e.g. Ansible/Chef/Puppet) used for?", options: ["Automating the setup and maintenance of server configurations", "Only writing frontend code", "Only designing databases", "Only for billing"], correct: 0 },
        { id: "inf_e8", type: "mcq", marks: 5, question: "What is the purpose of Container Orchestration?", options: ["Automating deployment, scaling and management of containers", "Manually starting each container one by one", "Formatting hard drives", "Writing unit tests"], correct: 0 },
        { id: "inf_e9", type: "mcq", marks: 5, question: "What is a Rollback in deployment?", options: ["Reverting to a previous stable version after a failed deployment", "Deleting all servers", "Creating a new feature", "Upgrading the database only"], correct: 0 },
        { id: "inf_e10", type: "mcq", marks: 5, question: "What is the main benefit of Auto Scaling?", options: ["Automatically adjusting resources based on current demand", "Reducing code quality", "Removing the need for monitoring", "Disabling load balancers"], correct: 0 },
        { id: "inf_e11", type: "coding", marks: 25, question: "Write a basic Terraform configuration to create a simple cloud resource (such as an AWS EC2 instance). (Minimum 50 characters)", language: "hcl", minLength: 50 },
        { id: "inf_e12", type: "coding", marks: 25, question: "Briefly describe how you would design a highly available web application, mentioning load balancing and multiple servers. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    }
  },

  wordpress: {
    fresher: {
      duration: 45,
      questions: [
        { id: "wp_f1", type: "mcq", marks: 5, question: "What is WordPress?", options: ["Content Management System", "Programming language", "Database", "Operating System"], correct: 0 },
        { id: "wp_f2", type: "mcq", marks: 5, question: "What are Themes in WordPress?", options: ["Control the design/look of the site", "Plugins", "Widgets only", "Users"], correct: 0 },
        { id: "wp_f3", type: "mcq", marks: 5, question: "What is a Plugin?", options: ["Extends functionality of WordPress", "Changes design only", "A theme", "A database table"], correct: 0 },
        { id: "wp_f4", type: "mcq", marks: 5, question: "What is the difference between Posts and Pages?", options: ["Posts are time-based (blog), Pages are static", "They are the same", "Pages are only for admins", "Posts cannot have images"], correct: 0 },
        { id: "wp_f5", type: "mcq", marks: 5, question: "Where are plugins installed from in WordPress admin?", options: ["Plugins > Add New", "Settings > General", "Appearance > Themes", "Users > Add New"], correct: 0 },
        { id: "wp_f6", type: "mcq", marks: 5, question: "What is the WordPress admin dashboard URL typically called?", options: ["wp-admin", "control-panel", "backend-portal", "cpanel"], correct: 0 },
        { id: "wp_f7", type: "mcq", marks: 5, question: "What is a Category used for in WordPress?", options: ["Broadly grouping posts by topic", "Styling the theme", "Installing plugins", "Managing users"], correct: 0 },
        { id: "wp_f8", type: "mcq", marks: 5, question: "What is a Widget?", options: ["A small block added to sidebars or footers for specific functions", "A full page template", "A plugin only", "A type of user role"], correct: 0 },
        { id: "wp_f9", type: "mcq", marks: 5, question: "Which file typically holds site-wide configuration like database details?", options: ["wp-config.php", "index.html", "style.css", "functions.js"], correct: 0 },
        { id: "wp_f10", type: "mcq", marks: 5, question: "What is the Media Library used for?", options: ["Storing and managing uploaded images and files", "Storing plugins", "Storing user passwords", "Storing themes only"], correct: 0 },
        { id: "wp_f11", type: "coding", marks: 25, question: "Write a simple custom page template structure for WordPress (PHP). (Minimum 50 characters)", language: "php", minLength: 50 },
        { id: "wp_f12", type: "coding", marks: 25, question: "Explain how to create a child theme and why it is recommended. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "wp_i1", type: "mcq", marks: 4, question: "Is WordPress free?", options: ["Yes (WordPress.org is free & open source)", "No", "Only for businesses", "Only premium"], correct: 0 },
        { id: "wp_i2", type: "mcq", marks: 4, question: "What is the WordPress admin dashboard called?", options: ["wp-admin", "control panel", "backend only", "cPanel"], correct: 0 },
        { id: "wp_i3", type: "mcq", marks: 4, question: "What is a Widget in WordPress?", options: ["Small blocks that perform specific functions in sidebars", "A full page", "A plugin only", "A theme"], correct: 0 },
        { id: "wp_i4", type: "mcq", marks: 4, question: "Which file is the main configuration file?", options: ["wp-config.php", "index.html", "style.css", "functions.js"], correct: 0 },
        { id: "wp_i5", type: "mcq", marks: 4, question: "What is a Category in WordPress used for?", options: ["Organizing posts into broad topics", "Changing the site's color scheme", "Installing plugins", "Backing up the database"], correct: 0 },
        { id: "wp_i6", type: "mcq", marks: 4, question: "What is a Tag in WordPress used for?", options: ["Describing specific details of a post, more specific than a category", "Changing user passwords", "Installing a theme", "Creating a menu"], correct: 0 },
        { id: "wp_i7", type: "mcq", marks: 4, question: "What is the Permalink setting used for?", options: ["Defining the URL structure of posts and pages", "Setting the site logo", "Managing comments only", "Choosing the theme colors"], correct: 0 },
        { id: "wp_i8", type: "mcq", marks: 4, question: "What is the Gutenberg editor?", options: ["The default block-based content editor in WordPress", "A plugin for security", "A theme name", "A hosting provider"], correct: 0 },
        { id: "wp_i9", type: "mcq", marks: 4, question: "What does 'activate' mean for a plugin?", options: ["Turning the plugin on so it starts working on the site", "Deleting the plugin", "Uploading the plugin file", "Renaming the plugin"], correct: 0 },
        { id: "wp_i10", type: "mcq", marks: 4, question: "What is the Appearance > Menus screen used for?", options: ["Creating and managing navigation menus", "Managing plugins", "Managing user roles", "Managing comments"], correct: 0 },
        { id: "wp_i11", type: "mcq", marks: 4, question: "What is a Shortcode?", options: ["A small code snippet in brackets that inserts dynamic content", "A type of user role", "A theme file", "A database table"], correct: 0 },
        { id: "wp_i12", type: "mcq", marks: 4, question: "What is the purpose of the Comments section on a post?", options: ["Allowing visitors to leave feedback or discussion on content", "Storing images", "Storing plugin settings", "Managing site backups"], correct: 0 },
        { id: "wp_i13", type: "mcq", marks: 4, question: "What user role has full control over a WordPress site?", options: ["Administrator", "Subscriber", "Contributor", "Author only"], correct: 0 },
        { id: "wp_i14", type: "mcq", marks: 4, question: "What does a 'Subscriber' role typically allow?", options: ["Managing their own profile and reading content", "Publishing posts", "Installing plugins", "Editing other users' posts"], correct: 0 },
        { id: "wp_i15", type: "mcq", marks: 4, question: "What is the featured image used for?", options: ["The main representative image shown for a post or page", "The site logo only", "The favicon", "The admin avatar"], correct: 0 },
        { id: "wp_i16", type: "mcq", marks: 4, question: "What is the purpose of the Settings > General screen?", options: ["Configuring basic site info like title, tagline and timezone", "Managing plugins", "Editing theme code", "Managing comments"], correct: 0 },
        { id: "wp_i17", type: "mcq", marks: 4, question: "What is a Sidebar in WordPress?", options: ["An area (often beside content) that can hold widgets", "The site's main navigation bar", "A plugin", "A database table"], correct: 0 },
        { id: "wp_i18", type: "mcq", marks: 4, question: "What does 'responsive design' mean for a WordPress theme?", options: ["The site layout adapts to different screen sizes", "The site loads only on desktops", "The site has no images", "The site cannot use plugins"], correct: 0 },
        { id: "wp_i19", type: "mcq", marks: 4, question: "What is the purpose of the WordPress Customizer?", options: ["Live-preview and adjust theme settings like colors and layout", "Writing PHP code directly", "Managing the database", "Installing WordPress core"], correct: 0 },
        { id: "wp_i20", type: "mcq", marks: 4, question: "What is a Draft in WordPress?", options: ["A post or page that is saved but not yet published", "A published post", "A deleted post", "A spam comment"], correct: 0 },
        { id: "wp_i21", type: "mcq", marks: 4, question: "What does 'publish' do to a post?", options: ["Makes the post live and visible to site visitors", "Deletes the post", "Saves it as a draft only", "Moves it to trash"], correct: 0 },
        { id: "wp_i22", type: "mcq", marks: 4, question: "What is the Trash in WordPress?", options: ["A temporary holding area for deleted posts before permanent removal", "The main homepage", "A plugin folder", "A theme setting"], correct: 0 },
        { id: "wp_i23", type: "mcq", marks: 4, question: "Why is keeping WordPress updated important?", options: ["To fix security vulnerabilities and bugs", "It's not important", "It only changes colors", "It disables plugins automatically"], correct: 0 },
        { id: "wp_i24", type: "mcq", marks: 4, question: "What is an SEO plugin (like Yoast) generally used for?", options: ["Helping optimize content for search engines", "Managing user logins", "Backing up the database", "Changing the site language only"], correct: 0 },
        { id: "wp_i25", type: "mcq", marks: 4, question: "What is a Backup plugin used for in WordPress?", options: ["Creating copies of the site's files and database for recovery", "Speeding up page load times", "Designing new themes", "Managing comments"], correct: 0 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "wp_e1", type: "mcq", marks: 5, question: "What is the WordPress loop?", options: ["PHP code that displays posts", "A JavaScript function", "A CSS class", "A database query only"], correct: 0 },
        { id: "wp_e2", type: "mcq", marks: 5, question: "What is the difference between get_posts() and WP_Query?", options: ["WP_Query is more powerful and flexible", "They are identical", "get_posts is always better", "WP_Query is deprecated"], correct: 0 },
        { id: "wp_e3", type: "mcq", marks: 5, question: "What is a Hook in WordPress?", options: ["Places where you can add custom code (actions & filters)", "A theme", "A plugin setting", "A database table"], correct: 0 },
        { id: "wp_e4", type: "mcq", marks: 5, question: "What is Object Caching used for in WordPress?", options: ["Improve performance by storing database query results", "Only store images", "User authentication", "Sending emails"], correct: 0 },
        { id: "wp_e5", type: "mcq", marks: 5, question: "What is the difference between an Action and a Filter hook?", options: ["Actions perform tasks at a point; Filters modify data and return it", "They are identical", "Filters cannot modify data", "Actions always return a value"], correct: 0 },
        { id: "wp_e6", type: "mcq", marks: 5, question: "What is a Custom Post Type used for?", options: ["Creating a content type beyond default Posts/Pages (e.g. Products, Events)", "Changing the site's font", "Managing user passwords", "Creating widgets only"], correct: 0 },
        { id: "wp_e7", type: "mcq", marks: 5, question: "What is a Custom Field (meta field) used for?", options: ["Storing extra structured data attached to a post", "Changing the theme colors", "Managing plugin licenses", "Creating a new user role"], correct: 0 },
        { id: "wp_e8", type: "mcq", marks: 5, question: "What is the REST API in WordPress used for?", options: ["Allowing external applications to interact with WordPress data via HTTP", "Styling the admin panel", "Storing backups", "Managing DNS records"], correct: 0 },
        { id: "wp_e9", type: "mcq", marks: 5, question: "What is a Transient in WordPress?", options: ["A way to temporarily cache data with an expiration time", "A permanent database table", "A type of user role", "A plugin category"], correct: 0 },
        { id: "wp_e10", type: "mcq", marks: 5, question: "What is the purpose of nonces in WordPress?", options: ["Protecting against CSRF by verifying request authenticity", "Speeding up queries", "Formatting dates", "Managing themes"], correct: 0 },
        { id: "wp_e11", type: "coding", marks: 25, question: "Write a custom WP_Query example to fetch the latest 5 posts from a specific category. (Minimum 50 characters)", language: "php", minLength: 50 },
        { id: "wp_e12", type: "coding", marks: 25, question: "Briefly explain how you would speed up a slow WordPress site (mention caching, images, or plugins). (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    }
  },

  // VOICE ONLY for HR and PC

  hr: {
    fresher: {
      duration: 45,
      questions: [
        { id: "hr_f1", type: "mcq", marks: 10, question: "What does HR stand for?", options: ["Human Resources", "Human Relations", "High Resources", "Human Rights"], correct: 0 },
        { id: "hr_f2", type: "mcq", marks: 10, question: "What is the main purpose of recruitment?", options: ["Attract and hire the right talent", "Only fire employees", "Only training", "Payroll only"], correct: 0 },
        { id: "hr_f3", type: "mcq", marks: 10, question: "What is Onboarding?", options: ["Process of integrating a new employee into the organization", "Exit process", "Only training", "Performance review"], correct: 0 },
        { id: "hr_f4", type: "mcq", marks: 10, question: "Choose the correct sentence:", options: ["She don't like working late.", "She doesn't likes working late.", "She doesn't like working late.", "She don't likes working late."], correct: 2 },
        { id: "hr_f5", type: "mcq", marks: 10, question: "Choose the correct word: The manager _____ the team every Monday.", options: ["meet", "meets", "meeting", "met"], correct: 1 },
        { id: "hr_f6", type: "mcq", marks: 10, question: "Which sentence is grammatically correct?", options: ["There is many employees in the office.", "There are many employees in the office.", "There is much employees in the office.", "There are much employees in the office."], correct: 1 },
        { id: "hr_f7", type: "voice", marks: 40, question: "How would you handle a conflict between two team members? Explain your approach clearly in 1-2 minutes." }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "hr_i1", type: "mcq", marks: 10, question: "What is the role of HR in a company?", options: ["Manage people-related functions", "Only accounts", "Only sales", "Only IT"], correct: 0 },
        { id: "hr_i2", type: "mcq", marks: 10, question: "What is Employee Engagement?", options: ["Emotional commitment of employees to the organization", "Only attendance", "Only salary discussion", "Only exit interview"], correct: 0 },
        { id: "hr_i3", type: "mcq", marks: 10, question: "What is a Performance Appraisal?", options: ["Systematic evaluation of employee performance", "Only salary hike", "Only training", "Hiring process"], correct: 0 },
        { id: "hr_i4", type: "mcq", marks: 10, question: "Choose the correct sentence:", options: ["He have completed the report.", "He has completed the report.", "He having completed the report.", "He is complete the report."], correct: 1 },
        { id: "hr_i5", type: "mcq", marks: 10, question: "Fill in the blank: Please _____ the form before submitting.", options: ["fill", "fills", "filled", "filling"], correct: 0 },
        { id: "hr_i6", type: "mcq", marks: 10, question: "Which is correct?", options: ["I am working here since 2022.", "I have been working here since 2022.", "I work here since 2022.", "I was working here since 2022."], correct: 1 },
        { id: "hr_i7", type: "voice", marks: 40, question: "Why do you want to work in HR? Tell us about your interest and any relevant experience." }
      ]
    },
    experienced: {
      duration: 55,
      questions: [
        { id: "hr_e1", type: "mcq", marks: 10, question: "What is the difference between Recruitment and Selection?", options: ["Recruitment attracts candidates, Selection chooses the best", "They are same", "Selection comes before recruitment", "Only recruitment is important"], correct: 0 },
        { id: "hr_e2", type: "mcq", marks: 10, question: "What is attrition?", options: ["Rate at which employees leave the organization", "Hiring rate", "Promotion rate", "Training hours"], correct: 0 },
        { id: "hr_e3", type: "mcq", marks: 10, question: "What is Succession Planning?", options: ["Identifying and developing future leaders", "Only firing process", "Only campus hiring", "Payroll management"], correct: 0 },
        { id: "hr_e4", type: "mcq", marks: 10, question: "Choose the correct sentence:", options: ["Neither of the candidates were selected.", "Neither of the candidates was selected.", "Neither of the candidates are selected.", "Neither of the candidates have selected."], correct: 1 },
        { id: "hr_e5", type: "mcq", marks: 10, question: "Which sentence is correct?", options: ["The data is accurate.", "The data are accurate.", "Both can be correct depending on usage.", "None"], correct: 2 },
        { id: "hr_e6", type: "voice", marks: 50, question: "How do you measure employee engagement and what strategies would you use to improve it in a mid-sized company?" }
      ]
    }
  },

  pc: {
    fresher: {
      duration: 45,
      questions: [
        { id: "pc_f1", type: "mcq", marks: 10, question: "What is the main responsibility of a Project Coordinator?", options: ["Support project planning, tracking and communication", "Only write code", "Only handle accounts", "Only do sales"], correct: 0 },
        { id: "pc_f2", type: "mcq", marks: 10, question: "What does a Project Timeline help with?", options: ["Tracking tasks and deadlines", "Writing code", "Designing logos", "Paying salaries"], correct: 0 },
        { id: "pc_f3", type: "mcq", marks: 10, question: "Which tool is commonly used for task tracking?", options: ["Jira / Trello / Asana", "Photoshop only", "Excel only for design", "Notepad only"], correct: 0 },
        { id: "pc_f4", type: "mcq", marks: 10, question: "Choose the correct sentence:", options: ["The team have completed the task.", "The team has completed the task.", "The team having completed the task.", "The team is complete the task."], correct: 1 },
        { id: "pc_f5", type: "mcq", marks: 10, question: "Fill in the blank: Please _____ the status report by evening.", options: ["send", "sends", "sending", "sent"], correct: 0 },
        { id: "pc_f6", type: "mcq", marks: 10, question: "Which sentence is correct?", options: ["There is five tasks pending.", "There are five tasks pending.", "There is five task pending.", "There are five task pending."], correct: 1 },
        { id: "pc_f7", type: "voice", marks: 40, question: "Explain how you would handle a delay in a project task and communicate it to stakeholders." }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "pc_i1", type: "mcq", marks: 10, question: "What is Project Coordination?", options: ["Organizing people, tasks and information so a project runs smoothly", "Only coding", "Only testing", "Only designing"], correct: 0 },
        { id: "pc_i2", type: "mcq", marks: 10, question: "Why are meeting notes important?", options: ["They record decisions and action items", "They are not important", "Only for managers", "Only for clients"], correct: 0 },
        { id: "pc_i3", type: "mcq", marks: 10, question: "What is a deadline?", options: ["The date by which a task must be completed", "A type of software", "A meeting room", "A salary date"], correct: 0 },
        { id: "pc_i4", type: "mcq", marks: 10, question: "Choose the correct sentence:", options: ["I will informed the team tomorrow.", "I will inform the team tomorrow.", "I will informing the team tomorrow.", "I will informs the team tomorrow."], correct: 1 },
        { id: "pc_i5", type: "mcq", marks: 10, question: "Which is correct?", options: ["The meeting is scheduled on Monday.", "The meeting is schedule on Monday.", "The meeting are scheduled on Monday.", "The meeting scheduled on Monday."], correct: 0 },
        { id: "pc_i6", type: "mcq", marks: 10, question: "Fill in the blank: Please _____ the agenda before the call.", options: ["share", "shares", "sharing", "shared"], correct: 0 },
        { id: "pc_i7", type: "voice", marks: 40, question: "Describe how you would prepare for and run a short project status meeting." }
      ]
    },
    experienced: {
      duration: 55,
      questions: [
        { id: "pc_e1", type: "mcq", marks: 10, question: "What is the difference between a Project Coordinator and a Project Manager?", options: ["Coordinator supports execution and communication; Manager owns planning, budget and delivery", "They are exactly the same", "Coordinator only does documentation", "Manager only attends meetings"], correct: 0 },
        { id: "pc_e2", type: "mcq", marks: 10, question: "What is Risk Management in projects?", options: ["Identifying potential problems early and planning responses", "Ignoring problems", "Only after project fails", "Only financial risks"], correct: 0 },
        { id: "pc_e3", type: "mcq", marks: 10, question: "What is a RACI matrix used for?", options: ["Clarifying roles: Responsible, Accountable, Consulted, Informed", "Tracking budget only", "Designing UI", "Writing code"], correct: 0 },
        { id: "pc_e4", type: "mcq", marks: 10, question: "Choose the correct sentence:", options: ["Neither of the deadlines were met.", "Neither of the deadlines was met.", "Neither of the deadlines are met.", "Neither of the deadlines have met."], correct: 1 },
        { id: "pc_e5", type: "mcq", marks: 10, question: "Which sentence is grammatically correct?", options: ["If the client will approve, we can start.", "If the client approves, we can start.", "If the client approve, we can start.", "If the client approved, we can start."], correct: 1 },
        { id: "pc_e6", type: "voice", marks: 50, question: "How would you handle conflicting priorities from two different stakeholders on the same project?" }
      ]
    }
  },

  data_analytics: {
    fresher: {
      duration: 45,
      questions: [
        { id: "da_f1", type: "mcq", marks: 5, question: "What is Data Analytics?", options: ["Process of examining data to find insights and support decisions", "Only storing data", "Only creating websites", "Only writing code"], correct: 0 },
        { id: "da_f2", type: "mcq", marks: 5, question: "Which of the following is a common data analysis tool?", options: ["Excel / Power BI / Tableau", "Photoshop only", "Word only", "Notepad only"], correct: 0 },
        { id: "da_f3", type: "mcq", marks: 5, question: "What does KPI stand for?", options: ["Key Performance Indicator", "Key Process Information", "Known Performance Index", "Keep Performance Internal"], correct: 0 },
        { id: "da_f4", type: "mcq", marks: 5, question: "What is the difference between structured and unstructured data?", options: ["Structured is organized in tables/rows; unstructured is free-form (text, images)", "They are the same", "Unstructured is only numbers", "Structured cannot be analyzed"], correct: 0 },
        { id: "da_f5", type: "mcq", marks: 5, question: "What is a dashboard used for?", options: ["Visual summary of key metrics for decision making", "Only storing files", "Writing code", "Sending emails"], correct: 0 },
        { id: "da_f6", type: "mcq", marks: 5, question: "What is a Pivot Table used for?", options: ["Quickly summarizing and analyzing large amounts of data", "Only formatting cells", "Only printing documents", "Creating macros only"], correct: 0 },
        { id: "da_f7", type: "mcq", marks: 5, question: "What does CSV stand for?", options: ["Comma Separated Values", "Common Sales Values", "Computer System Values", "Central Storage Volume"], correct: 0 },
        { id: "da_f8", type: "mcq", marks: 5, question: "Which chart is best for showing a trend over time?", options: ["Line chart", "Pie chart only", "A plain table", "Scatter only"], correct: 0 },
        { id: "da_f9", type: "mcq", marks: 5, question: "What is an outlier in a dataset?", options: ["A data point significantly different from other observations", "The average value", "The most common value", "A missing value"], correct: 0 },
        { id: "da_f10", type: "mcq", marks: 5, question: "Why is data cleaning important?", options: ["Removing errors and inconsistencies leads to more accurate analysis", "It is not necessary", "It only changes formatting colors", "It deletes all data permanently"], correct: 0 },
        { id: "da_f11", type: "coding", marks: 25, question: "Explain the steps you would take to clean a messy sales Excel sheet before analysis. (Minimum 50 characters)", language: "text", minLength: 50 },
        { id: "da_f12", type: "coding", marks: 25, question: "Write a simple example of how you would calculate average, total, and growth % for monthly sales. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "da_i1", type: "mcq", marks: 4, question: "What is the main goal of data analytics?", options: ["Turn data into useful insights for decisions", "Only collect data", "Only delete old data", "Only create charts for fun"], correct: 0 },
        { id: "da_i2", type: "mcq", marks: 4, question: "Which chart is best for showing trends over time?", options: ["Line chart", "Pie chart only", "Only a table", "Scatter only"], correct: 0 },
        { id: "da_i3", type: "mcq", marks: 4, question: "What is a pivot table used for?", options: ["Summarizing and analyzing large data quickly", "Only formatting cells", "Only printing", "Creating macros only"], correct: 0 },
        { id: "da_i4", type: "mcq", marks: 4, question: "What does CSV stand for?", options: ["Comma Separated Values", "Common Sales Values", "Computer System Values", "Central Storage Volume"], correct: 0 },
        { id: "da_i5", type: "mcq", marks: 4, question: "Which is an example of qualitative data?", options: ["Customer feedback comments", "Age in years", "Salary amount", "Number of orders"], correct: 0 },
        { id: "da_i6", type: "mcq", marks: 4, question: "What is data visualization?", options: ["Presenting data using charts and graphs", "Hiding data", "Deleting duplicates only", "Writing SQL only"], correct: 0 },
        { id: "da_i7", type: "mcq", marks: 4, question: "Which tool is widely used for business dashboards?", options: ["Power BI / Tableau", "Only Notepad", "Only Paint", "Only Calculator"], correct: 0 },
        { id: "da_i8", type: "mcq", marks: 4, question: "What should you check first when data looks wrong?", options: ["Source of data and possible entry errors", "Delete all rows", "Ignore it", "Change the chart colors only"], correct: 0 },
        { id: "da_i9", type: "mcq", marks: 4, question: "What is a filter used for in Excel or BI tools?", options: ["Show only rows that match certain conditions", "Delete the file", "Lock the sheet permanently", "Change font only"], correct: 0 },
        { id: "da_i10", type: "mcq", marks: 4, question: "Why is data quality important?", options: ["Bad data leads to wrong insights and decisions", "It is not important", "Only for large companies", "Only for coding teams"], correct: 0 },
        { id: "da_i11", type: "mcq", marks: 4, question: "What is Quantitative Data?", options: ["Data that can be measured and expressed in numbers", "Data that is only text", "Data that has no value", "Data that cannot be analyzed"], correct: 0 },
        { id: "da_i12", type: "mcq", marks: 4, question: "What is a Bar Chart best used for?", options: ["Comparing values across categories", "Showing a single number only", "Showing internal code structure", "Encrypting data"], correct: 0 },
        { id: "da_i13", type: "mcq", marks: 4, question: "What is a Pie Chart best used for?", options: ["Showing proportions of a whole", "Showing trends over long time periods", "Storing raw data", "Running calculations"], correct: 0 },
        { id: "da_i14", type: "mcq", marks: 4, question: "What does 'average' (mean) represent in a dataset?", options: ["The sum of values divided by the count of values", "The most frequent value", "The middle value when sorted", "The largest value"], correct: 0 },
        { id: "da_i15", type: "mcq", marks: 4, question: "What does 'median' represent in a dataset?", options: ["The middle value when data is sorted in order", "The most frequent value", "The sum of all values", "The smallest value"], correct: 0 },
        { id: "da_i16", type: "mcq", marks: 4, question: "What is a duplicate record?", options: ["An entry that appears more than once in a dataset", "A missing value", "A correctly formatted row", "An encrypted value"], correct: 0 },
        { id: "da_i17", type: "mcq", marks: 4, question: "What is the purpose of sorting data?", options: ["Arranging data in a specific order to make it easier to read or analyze", "Deleting unnecessary rows", "Encrypting sensitive data", "Creating a new database"], correct: 0 },
        { id: "da_i18", type: "mcq", marks: 4, question: "What is a Data Source?", options: ["The origin from which data is collected (e.g. a database or file)", "A chart type", "A type of formula", "A user permission"], correct: 0 },
        { id: "da_i19", type: "mcq", marks: 4, question: "What is the purpose of conditional formatting in Excel?", options: ["Automatically highlighting cells based on their values", "Deleting empty cells", "Creating new sheets", "Sending emails"], correct: 0 },
        { id: "da_i20", type: "mcq", marks: 4, question: "What is a Trend in data analysis?", options: ["A general direction in which data is changing over time", "A single outlier value", "A type of chart color", "A database backup"], correct: 0 },
        { id: "da_i21", type: "mcq", marks: 4, question: "What is Data Entry Error?", options: ["A mistake made while manually inputting data", "A software bug", "A network issue", "A chart formatting choice"], correct: 0 },
        { id: "da_i22", type: "mcq", marks: 4, question: "What is a Metric in analytics?", options: ["A quantifiable measure used to track performance", "A type of chart color", "A file format", "A user role"], correct: 0 },
        { id: "da_i23", type: "mcq", marks: 4, question: "What does 'drill down' mean in a BI dashboard?", options: ["Navigating from summary data into more detailed underlying data", "Deleting a report", "Changing the dashboard theme", "Exporting to PDF only"], correct: 0 },
        { id: "da_i24", type: "mcq", marks: 4, question: "What is a Data Set?", options: ["A collection of related data organized for analysis", "A single number", "A chart type", "A software license"], correct: 0 },
        { id: "da_i25", type: "mcq", marks: 4, question: "Why are clear chart labels and titles important?", options: ["They help viewers correctly understand what the data represents", "They are optional and never matter", "They slow down the report", "They are only for print versions"], correct: 0 }
      ]
    },
    experienced: {
      duration: 55,
      questions: [
        { id: "da_e1", type: "mcq", marks: 5, question: "What is the difference between descriptive and predictive analytics?", options: ["Descriptive explains what happened; predictive estimates what may happen", "They are the same", "Predictive only uses Excel", "Descriptive needs AI always"], correct: 0 },
        { id: "da_e2", type: "mcq", marks: 5, question: "What is ETL?", options: ["Extract, Transform, Load", "Excel Table List", "End Transaction Log", "Easy Table Lookup"], correct: 0 },
        { id: "da_e3", type: "mcq", marks: 5, question: "What is a star schema used for?", options: ["Organizing data warehouse tables for analytics", "UI design", "Email templates", "Password storage"], correct: 0 },
        { id: "da_e4", type: "mcq", marks: 5, question: "Which SQL clause groups rows for aggregation?", options: ["GROUP BY", "ORDER BY only", "WHERE only", "LIMIT only"], correct: 0 },
        { id: "da_e5", type: "mcq", marks: 5, question: "What is a Data Warehouse?", options: ["A central repository of integrated data from multiple sources for analysis", "A single Excel file", "A type of chart", "A user login system"], correct: 0 },
        { id: "da_e6", type: "mcq", marks: 5, question: "What is Data Wrangling?", options: ["Cleaning and transforming raw data into a usable format", "Deleting a database", "Designing a dashboard's colors", "Creating user accounts"], correct: 0 },
        { id: "da_e7", type: "mcq", marks: 5, question: "What is the purpose of A/B Testing in analytics?", options: ["Comparing two versions to see which performs better", "Formatting spreadsheets", "Backing up a database", "Encrypting sensitive data"], correct: 0 },
        { id: "da_e8", type: "mcq", marks: 5, question: "What is Correlation in statistics?", options: ["A measure of the relationship between two variables", "A guarantee of causation", "A type of chart only", "A data cleaning step"], correct: 0 },
        { id: "da_e9", type: "mcq", marks: 5, question: "What is Data Governance?", options: ["Policies and processes ensuring data quality, security and proper use", "A type of chart", "A pivot table feature", "A backup schedule only"], correct: 0 },
        { id: "da_e10", type: "mcq", marks: 5, question: "What is the difference between OLTP and OLAP systems?", options: ["OLTP handles daily transactions; OLAP is used for analysis and reporting", "They are identical", "OLAP is only for backups", "OLTP is only for reporting"], correct: 0 },
        { id: "da_e11", type: "coding", marks: 25, question: "Write a SQL query example that calculates total sales by region and filters regions with sales above 100000. (Minimum 50 characters)", language: "sql", minLength: 50 },
        { id: "da_e12", type: "coding", marks: 25, question: "Briefly describe how you would design a simple sales dashboard for management, listing key metrics and charts. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    }
  },

  finance: {
    fresher: {
      duration: 45,
      questions: [
        { id: "fin_f1", type: "mcq", marks: 10, question: "What is the Accounting Equation?", options: ["Assets = Liabilities + Equity", "Assets = Liabilities - Equity", "Assets + Liabilities = Equity", "None"], correct: 0 },
        { id: "fin_f2", type: "mcq", marks: 10, question: "What does P&L stand for?", options: ["Profit and Loss", "Purchase and Liability", "Payment and Loan", "None"], correct: 0 },
        { id: "fin_f3", type: "mcq", marks: 10, question: "What is GST?", options: ["Goods and Services Tax", "General Sales Tax", "Government Service Tax", "None"], correct: 0 },
        { id: "fin_f4", type: "mcq", marks: 10, question: "What is a Balance Sheet?", options: ["Statement of assets, liabilities and equity at a point in time", "Only profit statement", "Cash flow only", "Budget"], correct: 0 },
        { id: "fin_f5", type: "mcq", marks: 10, question: "What is Depreciation?", options: ["Decrease in value of an asset over time", "Increase in asset value", "Only for cash", "A type of income"], correct: 0 },
        { id: "fin_f6", type: "coding", marks: 25, question: "Calculate simple interest: Principal 10000, Rate 5%, Time 2 years. Show formula and answer. (Minimum 50 characters)", language: "text", minLength: 50 },
        { id: "fin_f7", type: "coding", marks: 25, question: "Explain the difference between Debit and Credit with one example each. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "fin_i1", type: "mcq", marks: 15, question: "What is a Balance Sheet?", options: ["Statement of assets, liabilities and equity at a point in time", "Only profit statement", "Cash flow only", "Budget"], correct: 0 },
        { id: "fin_i2", type: "mcq", marks: 15, question: "What are the main financial statements?", options: ["Balance Sheet, P&L, Cash Flow", "Only Balance Sheet", "Only Invoice", "Only Budget"], correct: 0 },
        { id: "fin_i3", type: "mcq", marks: 10, question: "What is Working Capital?", options: ["Current Assets - Current Liabilities", "Total Assets - Total Liabilities", "Only cash", "Fixed assets"], correct: 0 },
        { id: "fin_i4", type: "mcq", marks: 10, question: "What does ROI stand for?", options: ["Return on Investment", "Rate of Interest", "Return of Invoice", "None"], correct: 0 },
        { id: "fin_i5", type: "coding", marks: 25, question: "List the main financial statements and briefly explain what each shows. (Minimum 50 characters)", language: "text", minLength: 50 },
        { id: "fin_i6", type: "coding", marks: 25, question: "Why is financial literacy important for individuals and businesses? (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    experienced: {
      duration: 55,
      questions: [
        { id: "fin_e1", type: "mcq", marks: 10, question: "What is Working Capital?", options: ["Current Assets - Current Liabilities", "Total Assets - Total Liabilities", "Only cash", "Fixed assets"], correct: 0 },
        { id: "fin_e2", type: "mcq", marks: 10, question: "What is EBITDA?", options: ["Earnings Before Interest, Taxes, Depreciation and Amortization", "Earnings Before Income Tax", "Equity Before Interest", "None"], correct: 0 },
        { id: "fin_e3", type: "mcq", marks: 10, question: "What is the Current Ratio?", options: ["Current Assets / Current Liabilities", "Total Assets / Total Liabilities", "Profit / Sales", "Debt / Equity"], correct: 0 },
        { id: "fin_e4", type: "mcq", marks: 10, question: "What is Cash Flow Statement used for?", options: ["Shows inflow and outflow of cash", "Only profit", "Only assets", "Only liabilities"], correct: 0 },
        { id: "fin_e5", type: "coding", marks: 30, question: "Explain and calculate Current Ratio with sample numbers (show formula and interpretation). (Minimum 50 characters)", language: "text", minLength: 50 },
        { id: "fin_e6", type: "coding", marks: 30, question: "How would you analyze the financial health of a company using key ratios? Mention at least 3 ratios. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    }
  }
};

// Helper to get questions
function getAssessment(role, level) {
  role = (role || '').toLowerCase();
  level = (level || '').toLowerCase();
  if (QUESTION_BANK[role] && QUESTION_BANK[role][level]) {
    return QUESTION_BANK[role][level];
  }
  return null;
}

// Calculate total marks
function getTotalMarks(questions) {
  return questions.reduce((sum, q) => sum + (q.marks || 0), 0);
}
