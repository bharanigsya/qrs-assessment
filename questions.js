// Question Bank - Role + Level based
// EVERY role + level totals exactly 100 marks
// Voice questions ONLY for HR and PC roles

const QUESTION_BANK = {
  salesforce: {
    fresher: {
      duration: 45,
      questions: [
        { id: "sf_f1", type: "mcq", marks: 5, question: "What is a Salesforce Object?", options: ["A database table", "A UI component", "A workflow", "An Apex class"], correct: 0 },
        { id: "sf_f2", type: "mcq", marks: 5, question: "Which of the following is used for automation in Salesforce?", options: ["Flow", "HTML", "CSS", "JavaScript only"], correct: 0 },
        { id: "sf_f3", type: "mcq", marks: 5, question: "What does SOQL stand for?", options: ["Salesforce Object Query Language", "Simple Object Query Language", "Structured Object Query Language", "Salesforce Online Query Language"], correct: 0 },
        { id: "sf_f4", type: "mcq", marks: 5, question: "Profiles control:", options: ["Object & Field level security", "Only page layouts", "Only reports", "Only dashboards"], correct: 0 },
        { id: "sf_f5", type: "mcq", marks: 10, question: "Which relationship allows a child record to exist without a parent?", options: ["Lookup", "Master-Detail", "Hierarchical", "Self"], correct: 0 },
        { id: "sf_f6", type: "mcq", marks: 10, question: "What is the difference between a Role and a Profile?", options: ["Role is for record access hierarchy, Profile is for object/field permissions", "They are the same", "Role controls UI, Profile controls data", "Profile is only for admins"], correct: 0 },
        { id: "sf_f7", type: "mcq", marks: 10, question: "In Lightning Experience, what is used to create custom pages?", options: ["Lightning App Builder", "Visualforce only", "Apex Pages", "Classic Page Layouts only"], correct: 0 },
        { id: "sf_f8", type: "coding", marks: 25, question: "Write a simple Apex trigger that updates a checkbox field 'Is_Active__c' to true when a Contact is created. (Minimum 50 characters)", language: "apex", minLength: 50 },
        { id: "sf_f9", type: "coding", marks: 25, question: "Write a SOQL query to fetch all Accounts where Industry = 'Technology' and limit the results to 10 records. (Minimum 50 characters)", language: "soql", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "sf_i1", type: "mcq", marks: 10, question: "What is Salesforce?", options: ["CRM Platform", "Database only", "Programming language", "Operating System"], correct: 0 },
        { id: "sf_i2", type: "mcq", marks: 10, question: "Which cloud is used for sales processes?", options: ["Sales Cloud", "Service Cloud", "Marketing Cloud", "Commerce Cloud"], correct: 0 },
        { id: "sf_i3", type: "mcq", marks: 10, question: "What is a Lead in Salesforce?", options: ["Potential customer", "Existing customer", "Product", "Invoice"], correct: 0 },
        { id: "sf_i4", type: "mcq", marks: 10, question: "What does CRM stand for?", options: ["Customer Relationship Management", "Customer Resource Management", "Company Resource Management", "Client Relationship Module"], correct: 0 },
        { id: "sf_i5", type: "mcq", marks: 10, question: "What is a Report in Salesforce used for?", options: ["Analyzing data", "Sending emails only", "Creating users", "Changing page layouts"], correct: 0 },
        { id: "sf_i6", type: "coding", marks: 25, question: "Write a simple SOQL query to fetch all Contacts related to a specific Account Id. (Minimum 50 characters)", language: "soql", minLength: 50 },
        { id: "sf_i7", type: "coding", marks: 25, question: "Describe the steps to create a new custom object in Salesforce and add 3 custom fields. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "sf_e1", type: "mcq", marks: 5, question: "What is the governor limit for SOQL queries in a synchronous transaction?", options: ["100", "50", "200", "150"], correct: 0 },
        { id: "sf_e2", type: "mcq", marks: 5, question: "Which design pattern is commonly used in Apex triggers?", options: ["Trigger Handler / Helper", "Singleton only", "MVC only", "Factory only"], correct: 0 },
        { id: "sf_e3", type: "mcq", marks: 10, question: "What is the purpose of Platform Cache?", options: ["Store frequently accessed data to reduce SOQL/API calls", "Store user sessions only", "Replace custom settings", "Only for Visualforce"], correct: 0 },
        { id: "sf_e4", type: "mcq", marks: 10, question: "In a master-detail relationship, what happens when the master is deleted?", options: ["All detail records are deleted", "Detail records become orphans", "Detail records are reparented automatically", "Nothing"], correct: 0 },
        { id: "sf_e5", type: "coding", marks: 30, question: "Write an Apex class with a method that accepts a list of Account IDs and returns a Map of Account Id to number of related Contacts. Handle bulkification properly. (Minimum 50 characters)", language: "apex", minLength: 50 },
        { id: "sf_e6", type: "coding", marks: 40, question: "Write a Lightning Web Component (LWC) that displays a list of Accounts using @wire service. Include the HTML template structure and JS controller (mock data is fine). (Minimum 50 characters)", language: "javascript", minLength: 50 }
      ]
    }
  },

  testing: {
    fresher: {
      duration: 45,
      questions: [
        { id: "t_f1", type: "mcq", marks: 5, question: "What is the difference between Verification and Validation?", options: ["Verification: Are we building the product right? Validation: Are we building the right product?", "They are the same", "Verification is only manual", "Validation is only automated"], correct: 0 },
        { id: "t_f2", type: "mcq", marks: 5, question: "Which is a black-box testing technique?", options: ["Equivalence Partitioning", "Statement Coverage", "Path Coverage", "Mutation Testing"], correct: 0 },
        { id: "t_f3", type: "mcq", marks: 5, question: "What does STLC stand for?", options: ["Software Testing Life Cycle", "System Testing Life Cycle", "Software Test Logic Cycle", "Standard Testing Life Cycle"], correct: 0 },
        { id: "t_f4", type: "mcq", marks: 10, question: "What is a Test Case?", options: ["A set of conditions to verify a feature", "A bug report", "A requirement document", "A code module"], correct: 0 },
        { id: "t_f5", type: "mcq", marks: 10, question: "Which tool is commonly used for API testing?", options: ["Postman", "Photoshop", "Excel only", "Word"], correct: 0 },
        { id: "t_f6", type: "mcq", marks: 15, question: "What is Regression Testing?", options: ["Testing to ensure new changes don't break existing functionality", "Testing only new features", "Performance testing", "Security testing only"], correct: 0 },
        { id: "t_f7", type: "coding", marks: 25, question: "Write a simple Selenium (Python or Java) code snippet to open Google and search for 'Software Testing'. (Minimum 50 characters)", language: "python", minLength: 50 },
        { id: "t_f8", type: "coding", marks: 25, question: "Write step-by-step manual test cases for testing a Login page (username, password, submit, error messages). (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "t_i1", type: "mcq", marks: 15, question: "What is Software Testing?", options: ["Process of evaluating software to find defects", "Writing code", "Designing UI", "Deploying software"], correct: 0 },
        { id: "t_i2", type: "mcq", marks: 15, question: "What is a Bug?", options: ["A defect in the software", "A feature", "A requirement", "A test case"], correct: 0 },
        { id: "t_i3", type: "mcq", marks: 10, question: "Which is functional testing?", options: ["Unit Testing", "Load Testing", "Stress Testing", "Volume Testing"], correct: 0 },
        { id: "t_i4", type: "mcq", marks: 10, question: "What is Smoke Testing?", options: ["Basic testing to check if build is stable", "Full regression", "Performance testing", "Security testing"], correct: 0 },
        { id: "t_i5", type: "coding", marks: 25, question: "Write steps (manual test case format) to test a Login page including positive and negative scenarios. (Minimum 50 characters)", language: "text", minLength: 50 },
        { id: "t_i6", type: "coding", marks: 25, question: "Explain the difference between Black Box and White Box testing with examples. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "t_e1", type: "mcq", marks: 5, question: "What is the difference between Severity and Priority?", options: ["Severity: impact on system, Priority: order of fixing", "They are the same", "Severity is only for critical bugs", "Priority is decided by developers only"], correct: 0 },
        { id: "t_e2", type: "mcq", marks: 5, question: "Which framework is commonly used with Selenium?", options: ["TestNG / JUnit / PyTest", "Only React", "Only Spring", "Only Django"], correct: 0 },
        { id: "t_e3", type: "mcq", marks: 10, question: "What is Shift-Left Testing?", options: ["Testing early in the development cycle", "Testing only at the end", "Only performance testing", "Only security testing"], correct: 0 },
        { id: "t_e4", type: "mcq", marks: 10, question: "What is the purpose of a Test Plan?", options: ["Document scope, approach, resources and schedule of testing", "Only list test cases", "Only bug reports", "Code documentation"], correct: 0 },
        { id: "t_e5", type: "coding", marks: 30, question: "Write a Page Object Model example for a Login page in Selenium (any language). Include at least locator strategy and one method. (Minimum 50 characters)", language: "java", minLength: 50 },
        { id: "t_e6", type: "coding", marks: 40, question: "Write a simple API test using RestAssured or Python requests library to validate status code 200 and response body for a GET endpoint. (Minimum 50 characters)", language: "java", minLength: 50 }
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
        { id: "db_f4", type: "mcq", marks: 10, question: "What is Normalization?", options: ["Process of organizing data to reduce redundancy", "Adding more tables", "Denormalization", "Indexing only"], correct: 0 },
        { id: "db_f5", type: "mcq", marks: 10, question: "Which join returns only matching records from both tables?", options: ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"], correct: 0 },
        { id: "db_f6", type: "mcq", marks: 15, question: "What is an Index used for?", options: ["Speed up data retrieval", "Store data", "Delete data", "Backup"], correct: 0 },
        { id: "db_f7", type: "coding", marks: 25, question: "Write a SQL query to find the second highest salary from an Employee table (assume columns: id, name, salary). (Minimum 50 characters)", language: "sql", minLength: 50 },
        { id: "db_f8", type: "coding", marks: 25, question: "Write SQL to create a table Employees with columns id (PK), name, department, salary and insert 2 sample rows. (Minimum 50 characters)", language: "sql", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "db_i1", type: "mcq", marks: 15, question: "What is a Database?", options: ["Organized collection of data", "A programming language", "An operating system", "A web server"], correct: 0 },
        { id: "db_i2", type: "mcq", marks: 15, question: "Which is a relational database?", options: ["MySQL", "MongoDB", "Redis", "Cassandra"], correct: 0 },
        { id: "db_i3", type: "mcq", marks: 10, question: "What does DDL stand for?", options: ["Data Definition Language", "Data Digging Language", "Data Design Language", "Data Development Language"], correct: 0 },
        { id: "db_i4", type: "mcq", marks: 10, question: "What is a Foreign Key?", options: ["A key that links two tables", "Primary key of same table", "An index", "A view"], correct: 0 },
        { id: "db_i5", type: "coding", marks: 25, question: "Write SQL to create a table Students with columns id, name, age, email. (Minimum 50 characters)", language: "sql", minLength: 50 },
        { id: "db_i6", type: "coding", marks: 25, question: "Write a SELECT query with WHERE and ORDER BY on any sample table. (Minimum 50 characters)", language: "sql", minLength: 50 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "db_e1", type: "mcq", marks: 5, question: "What is the difference between Clustered and Non-Clustered Index?", options: ["Clustered determines physical order of data, Non-clustered is separate structure", "They are the same", "Non-clustered is always faster", "Clustered can be multiple"], correct: 0 },
        { id: "db_e2", type: "mcq", marks: 5, question: "What is a Deadlock?", options: ["Two transactions waiting for each other to release locks", "A crashed database", "Slow query", "Missing index"], correct: 0 },
        { id: "db_e3", type: "mcq", marks: 10, question: "What is CAP Theorem?", options: ["Consistency, Availability, Partition tolerance", "Concurrency, Atomicity, Performance", "Cache, API, Performance", "None"], correct: 0 },
        { id: "db_e4", type: "mcq", marks: 10, question: "In PostgreSQL/MySQL, what is EXPLAIN used for?", options: ["Show query execution plan", "Execute the query", "Delete data", "Create index"], correct: 0 },
        { id: "db_e5", type: "coding", marks: 30, question: "Write a query to find employees who earn more than their managers using self-join. (Minimum 50 characters)", language: "sql", minLength: 50 },
        { id: "db_e6", type: "coding", marks: 40, question: "Write an example using window function (ROW_NUMBER or RANK) to rank employees by salary within each department. (Minimum 50 characters)", language: "sql", minLength: 50 }
      ]
    }
  },

  integration: {
    fresher: {
      duration: 45,
      questions: [
        { id: "int_f1", type: "mcq", marks: 10, question: "What is an API?", options: ["Application Programming Interface", "Application Process Integration", "Automated Program Interface", "None"], correct: 0 },
        { id: "int_f2", type: "mcq", marks: 10, question: "Which protocol is commonly used for web APIs?", options: ["HTTP/HTTPS", "FTP only", "SMTP", "SSH"], correct: 0 },
        { id: "int_f3", type: "mcq", marks: 10, question: "What does REST stand for?", options: ["Representational State Transfer", "Remote Execution State Transfer", "Relational State Transfer", "None"], correct: 0 },
        { id: "int_f4", type: "mcq", marks: 10, question: "What is JSON commonly used for?", options: ["Data exchange format", "Database only", "Styling pages", "Compiling code"], correct: 0 },
        { id: "int_f5", type: "mcq", marks: 10, question: "What is Middleware in integration?", options: ["Software that connects different applications", "A database", "A frontend framework", "An operating system"], correct: 0 },
        { id: "int_f6", type: "coding", marks: 25, question: "Write a simple REST API call (using fetch or axios or curl) to GET data from an endpoint and log the response. (Minimum 50 characters)", language: "javascript", minLength: 50 },
        { id: "int_f7", type: "coding", marks: 25, question: "Explain the difference between SOAP and REST with one example each. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "int_i1", type: "mcq", marks: 15, question: "What is Integration in software?", options: ["Connecting different systems to work together", "Writing UI", "Database design", "Testing only"], correct: 0 },
        { id: "int_i2", type: "mcq", marks: 15, question: "What is an API endpoint?", options: ["A specific URL where an API can be accessed", "A database table", "A UI button", "A server room"], correct: 0 },
        { id: "int_i3", type: "mcq", marks: 10, question: "Which status code means success?", options: ["200", "404", "500", "301"], correct: 0 },
        { id: "int_i4", type: "mcq", marks: 10, question: "What does HTTP POST typically do?", options: ["Create or submit data", "Only read data", "Delete data", "Update only"], correct: 0 },
        { id: "int_i5", type: "coding", marks: 25, question: "Describe steps to integrate two systems using API (authentication, request, response handling). (Minimum 50 characters)", language: "text", minLength: 50 },
        { id: "int_i6", type: "coding", marks: 25, question: "Write a sample JSON payload for creating a user (name, email, role). (Minimum 50 characters)", language: "json", minLength: 50 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "int_e1", type: "mcq", marks: 10, question: "What is the difference between Synchronous and Asynchronous integration?", options: ["Sync waits for response, Async does not", "They are same", "Async is always slower", "Sync is only for batch"], correct: 0 },
        { id: "int_e2", type: "mcq", marks: 10, question: "What is an ESB?", options: ["Enterprise Service Bus", "Enterprise System Bridge", "External Service Broker", "None"], correct: 0 },
        { id: "int_e3", type: "mcq", marks: 10, question: "What is Idempotency in APIs?", options: ["Same request can be made multiple times without different effects", "Request can be made only once", "Only for GET", "Only for POST"], correct: 0 },
        { id: "int_e4", type: "mcq", marks: 10, question: "What is a Message Queue used for?", options: ["Decoupling systems and handling async communication", "Storing user sessions", "Rendering UI", "Compiling code"], correct: 0 },
        { id: "int_e5", type: "coding", marks: 30, question: "Design a simple message flow using a queue for order processing. Include producer and consumer concepts + sample code structure. (Minimum 50 characters)", language: "javascript", minLength: 50 },
        { id: "int_e6", type: "coding", marks: 30, question: "Explain how you would handle retries, idempotency and error handling in a distributed integration between two systems. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    }
  },

  infra: {
    fresher: {
      duration: 45,
      questions: [
        { id: "inf_f1", type: "mcq", marks: 10, question: "What is a Virtual Machine?", options: ["Emulation of a computer system", "A physical server", "A programming language", "A database"], correct: 0 },
        { id: "inf_f2", type: "mcq", marks: 10, question: "What does CI/CD stand for?", options: ["Continuous Integration / Continuous Deployment", "Code Integration / Code Deployment", "Continuous Inspection / Continuous Delivery", "None"], correct: 0 },
        { id: "inf_f3", type: "mcq", marks: 10, question: "What is Kubernetes used for?", options: ["Container orchestration", "Database management", "Frontend framework", "Version control"], correct: 0 },
        { id: "inf_f4", type: "mcq", marks: 10, question: "What is Docker?", options: ["Containerization platform", "A programming language", "A database", "A cloud provider only"], correct: 0 },
        { id: "inf_f5", type: "mcq", marks: 10, question: "Which of the following is a cloud provider?", options: ["AWS", "MySQL", "React", "Git"], correct: 0 },
        { id: "inf_f6", type: "coding", marks: 25, question: "Write a simple Dockerfile for a Node.js application (FROM, WORKDIR, COPY, RUN, CMD). (Minimum 50 characters)", language: "dockerfile", minLength: 50 },
        { id: "inf_f7", type: "coding", marks: 25, question: "Explain the difference between a container and a virtual machine. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "inf_i1", type: "mcq", marks: 15, question: "What is Linux?", options: ["Open-source operating system", "A database", "A programming language", "A cloud provider"], correct: 0 },
        { id: "inf_i2", type: "mcq", marks: 15, question: "What is a Server?", options: ["A computer that provides services to other computers", "Only a desktop", "A mobile phone", "A browser"], correct: 0 },
        { id: "inf_i3", type: "mcq", marks: 10, question: "What does IP stand for?", options: ["Internet Protocol", "Internal Process", "Internet Provider", "Input Port"], correct: 0 },
        { id: "inf_i4", type: "mcq", marks: 10, question: "What is SSH used for?", options: ["Secure remote login", "Sending emails", "Browsing websites", "Playing videos"], correct: 0 },
        { id: "inf_i5", type: "coding", marks: 25, question: "Write basic Linux commands to list files, change directory, view file content and check disk space. (Minimum 50 characters)", language: "bash", minLength: 50 },
        { id: "inf_i6", type: "coding", marks: 25, question: "Explain what Cloud Computing is and name the three main service models (IaaS, PaaS, SaaS). (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "inf_e1", type: "mcq", marks: 10, question: "What is Infrastructure as Code (IaC)?", options: ["Managing infrastructure through code (Terraform, CloudFormation etc.)", "Manual server setup", "Only Docker", "Only monitoring"], correct: 0 },
        { id: "inf_e2", type: "mcq", marks: 10, question: "What is the difference between Horizontal and Vertical scaling?", options: ["Horizontal: add more machines, Vertical: increase resources of existing", "They are same", "Vertical is always better", "Horizontal only for databases"], correct: 0 },
        { id: "inf_e3", type: "mcq", marks: 10, question: "What is a Load Balancer?", options: ["Distributes incoming traffic across multiple servers", "A type of database", "A firewall only", "A monitoring tool"], correct: 0 },
        { id: "inf_e4", type: "mcq", marks: 10, question: "What is High Availability?", options: ["System designed to be operational continuously with minimal downtime", "Only fast performance", "Cheap infrastructure", "Single server setup"], correct: 0 },
        { id: "inf_e5", type: "coding", marks: 30, question: "Write a basic Terraform configuration to create an AWS EC2 instance (or equivalent cloud resource). (Minimum 50 characters)", language: "hcl", minLength: 50 },
        { id: "inf_e6", type: "coding", marks: 30, question: "How do you design a highly available architecture for a web application? Mention multi-AZ, load balancer, auto-scaling. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    }
  },

  wordpress: {
    fresher: {
      duration: 45,
      questions: [
        { id: "wp_f1", type: "mcq", marks: 10, question: "What is WordPress?", options: ["Content Management System", "Programming language", "Database", "Operating System"], correct: 0 },
        { id: "wp_f2", type: "mcq", marks: 10, question: "What are Themes in WordPress?", options: ["Control the design/look of the site", "Plugins", "Widgets only", "Users"], correct: 0 },
        { id: "wp_f3", type: "mcq", marks: 10, question: "What is a Plugin?", options: ["Extends functionality of WordPress", "Changes design only", "A theme", "A database table"], correct: 0 },
        { id: "wp_f4", type: "mcq", marks: 10, question: "What is the difference between Posts and Pages?", options: ["Posts are time-based (blog), Pages are static", "They are the same", "Pages are only for admins", "Posts cannot have images"], correct: 0 },
        { id: "wp_f5", type: "mcq", marks: 10, question: "Where are plugins installed from in WordPress admin?", options: ["Plugins > Add New", "Settings > General", "Appearance > Themes", "Users > Add New"], correct: 0 },
        { id: "wp_f6", type: "coding", marks: 25, question: "Write a simple custom page template structure for WordPress (PHP). (Minimum 50 characters)", language: "php", minLength: 50 },
        { id: "wp_f7", type: "coding", marks: 25, question: "Explain how to create a child theme and why it is recommended. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "wp_i1", type: "mcq", marks: 15, question: "Is WordPress free?", options: ["Yes (WordPress.org is free & open source)", "No", "Only for businesses", "Only premium"], correct: 0 },
        { id: "wp_i2", type: "mcq", marks: 15, question: "What is the WordPress admin dashboard called?", options: ["wp-admin", "control panel", "backend only", "cPanel"], correct: 0 },
        { id: "wp_i3", type: "mcq", marks: 10, question: "What is a Widget in WordPress?", options: ["Small blocks that perform specific functions in sidebars", "A full page", "A plugin only", "A theme"], correct: 0 },
        { id: "wp_i4", type: "mcq", marks: 10, question: "Which file is the main configuration file?", options: ["wp-config.php", "index.html", "style.css", "functions.js"], correct: 0 },
        { id: "wp_i5", type: "coding", marks: 25, question: "How do you install a plugin in WordPress? Write the steps. (Minimum 50 characters)", language: "text", minLength: 50 },
        { id: "wp_i6", type: "coding", marks: 25, question: "Explain the purpose of the functions.php file in a theme. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    experienced: {
      duration: 60,
      questions: [
        { id: "wp_e1", type: "mcq", marks: 10, question: "What is the WordPress loop?", options: ["PHP code that displays posts", "A JavaScript function", "A CSS class", "A database query only"], correct: 0 },
        { id: "wp_e2", type: "mcq", marks: 10, question: "What is the difference between get_posts() and WP_Query?", options: ["WP_Query is more powerful and flexible", "They are identical", "get_posts is always better", "WP_Query is deprecated"], correct: 0 },
        { id: "wp_e3", type: "mcq", marks: 10, question: "What is a Hook in WordPress?", options: ["Places where you can add custom code (actions & filters)", "A theme", "A plugin setting", "A database table"], correct: 0 },
        { id: "wp_e4", type: "mcq", marks: 10, question: "What is Object Caching used for in WordPress?", options: ["Improve performance by storing database query results", "Only store images", "User authentication", "Sending emails"], correct: 0 },
        { id: "wp_e5", type: "coding", marks: 30, question: "Write a custom WP_Query to fetch latest 5 posts from a specific category. (Minimum 50 characters)", language: "php", minLength: 50 },
        { id: "wp_e6", type: "coding", marks: 30, question: "How would you optimize a slow WordPress site? Mention caching, queries, images, plugins. (Minimum 50 characters)", language: "text", minLength: 50 }
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
        { id: "da_f1", type: "mcq", marks: 10, question: "What is Data Analytics?", options: ["Process of examining data to find insights and support decisions", "Only storing data", "Only creating websites", "Only writing code"], correct: 0 },
        { id: "da_f2", type: "mcq", marks: 10, question: "Which of the following is a common data analysis tool?", options: ["Excel / Power BI / Tableau", "Photoshop only", "Word only", "Notepad only"], correct: 0 },
        { id: "da_f3", type: "mcq", marks: 10, question: "What does KPI stand for?", options: ["Key Performance Indicator", "Key Process Information", "Known Performance Index", "Keep Performance Internal"], correct: 0 },
        { id: "da_f4", type: "mcq", marks: 10, question: "What is the difference between structured and unstructured data?", options: ["Structured is organized in tables/rows; unstructured is free-form (text, images)", "They are the same", "Unstructured is only numbers", "Structured cannot be analyzed"], correct: 0 },
        { id: "da_f5", type: "mcq", marks: 10, question: "What is a dashboard used for?", options: ["Visual summary of key metrics for decision making", "Only storing files", "Writing code", "Sending emails"], correct: 0 },
        { id: "da_f6", type: "coding", marks: 25, question: "Explain the steps you would take to clean a messy sales Excel sheet before analysis. (Minimum 50 characters)", language: "text", minLength: 50 },
        { id: "da_f7", type: "coding", marks: 25, question: "Write a simple example of how you would calculate average, total, and growth % for monthly sales. (Minimum 50 characters)", language: "text", minLength: 50 }
      ]
    },
    intern: {
      duration: 40,
      questions: [
        { id: "da_i1", type: "mcq", marks: 10, question: "What is the main goal of data analytics?", options: ["Turn data into useful insights for decisions", "Only collect data", "Only delete old data", "Only create charts for fun"], correct: 0 },
        { id: "da_i2", type: "mcq", marks: 10, question: "Which chart is best for showing trends over time?", options: ["Line chart", "Pie chart only", "Only a table", "Scatter only"], correct: 0 },
        { id: "da_i3", type: "mcq", marks: 10, question: "What is a pivot table used for?", options: ["Summarizing and analyzing large data quickly", "Only formatting cells", "Only printing", "Creating macros only"], correct: 0 },
        { id: "da_i4", type: "mcq", marks: 10, question: "What does CSV stand for?", options: ["Comma Separated Values", "Common Sales Values", "Computer System Values", "Central Storage Volume"], correct: 0 },
        { id: "da_i5", type: "mcq", marks: 10, question: "Which is an example of qualitative data?", options: ["Customer feedback comments", "Age in years", "Salary amount", "Number of orders"], correct: 0 },
        { id: "da_i6", type: "mcq", marks: 10, question: "What is data visualization?", options: ["Presenting data using charts and graphs", "Hiding data", "Deleting duplicates only", "Writing SQL only"], correct: 0 },
        { id: "da_i7", type: "mcq", marks: 10, question: "Which tool is widely used for business dashboards?", options: ["Power BI / Tableau", "Only Notepad", "Only Paint", "Only Calculator"], correct: 0 },
        { id: "da_i8", type: "mcq", marks: 10, question: "What should you check first when data looks wrong?", options: ["Source of data and possible entry errors", "Delete all rows", "Ignore it", "Change the chart colors only"], correct: 0 },
        { id: "da_i9", type: "mcq", marks: 10, question: "What is a filter used for in Excel or BI tools?", options: ["Show only rows that match certain conditions", "Delete the file", "Lock the sheet permanently", "Change font only"], correct: 0 },
        { id: "da_i10", type: "mcq", marks: 10, question: "Why is data quality important?", options: ["Bad data leads to wrong insights and decisions", "It is not important", "Only for large companies", "Only for coding teams"], correct: 0 }
      ]
    },
    experienced: {
      duration: 55,
      questions: [
        { id: "da_e1", type: "mcq", marks: 10, question: "What is the difference between descriptive and predictive analytics?", options: ["Descriptive explains what happened; predictive estimates what may happen", "They are the same", "Predictive only uses Excel", "Descriptive needs AI always"], correct: 0 },
        { id: "da_e2", type: "mcq", marks: 10, question: "What is ETL?", options: ["Extract, Transform, Load", "Excel Table List", "End Transaction Log", "Easy Table Lookup"], correct: 0 },
        { id: "da_e3", type: "mcq", marks: 10, question: "What is a star schema used for?", options: ["Organizing data warehouse tables for analytics", "UI design", "Email templates", "Password storage"], correct: 0 },
        { id: "da_e4", type: "mcq", marks: 10, question: "Which SQL clause groups rows for aggregation?", options: ["GROUP BY", "ORDER BY only", "WHERE only", "LIMIT only"], correct: 0 },
        { id: "da_e5", type: "coding", marks: 30, question: "Write a SQL query example that calculates total sales by region and filters regions with sales above 100000. (Minimum 50 characters)", language: "sql", minLength: 50 },
        { id: "da_e6", type: "coding", marks: 30, question: "How would you design a simple sales dashboard for management? List key metrics, charts, and filters. (Minimum 50 characters)", language: "text", minLength: 50 }
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