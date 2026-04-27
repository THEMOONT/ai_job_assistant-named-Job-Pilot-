import re


MASTER_SKILLS = [
    # Programming Languages
    "Python", "Java", "C", "C++", "C#", "Go", "Golang", "Rust", "Ruby",
    "PHP", "Perl", "Scala", "Kotlin", "Swift", "R", "MATLAB", "TypeScript",
    "JavaScript", "Bash", "PowerShell", "Shell Scripting",

    # Web Technologies
    "HTML", "CSS", "SASS", "Bootstrap", "Tailwind CSS", "React", "Next.js",
    "Vue.js", "Angular", "Node.js", "Express.js", "jQuery", "AJAX",

    # Python Frameworks
    "Django", "Flask", "FastAPI", "Pyramid", "Tornado",

    # Java Frameworks
    "Spring", "Spring Boot", "Hibernate", "Struts", "Maven", "Gradle",

    # APIs / Data Formats
    "REST API", "RESTful API", "SOAP", "GraphQL", "JSON", "XML", "YAML",
    "Swagger", "OpenAPI", "Postman", "curl",

    # Databases
    "SQL", "PL/SQL", "T-SQL", "Oracle", "Oracle 19c", "Oracle 12c",
    "PostgreSQL", "MySQL", "MariaDB", "MongoDB", "Redis", "SQLite",
    "Microsoft SQL Server", "Cassandra", "DynamoDB", "Elasticsearch",

    # Cloud Platforms
    "AWS", "Azure", "Google Cloud", "GCP", "OCI", "DigitalOcean",
    "Heroku", "Vercel", "Netlify",

    # AWS Services
    "EC2", "S3", "IAM", "RDS", "Lambda", "CloudWatch", "VPC",
    "Route53", "ECS", "EKS", "SNS", "SQS",

    # DevOps / Containers
    "Docker", "Kubernetes", "Podman", "OpenShift", "Terraform",
    "Ansible", "Chef", "Puppet", "Jenkins", "GitLab CI/CD",
    "GitHub Actions", "CI/CD",

    # Version Control
    "Git", "GitHub", "GitLab", "Bitbucket", "SVN",

    # OS / Infrastructure
    "Linux", "UNIX", "Windows", "Ubuntu", "CentOS", "Red Hat",
    "Fedora", "Debian", "VMware", "VirtualBox",

    # Monitoring / Logging
    "Splunk", "Grafana", "Prometheus", "Nagios", "Zabbix",
    "Datadog", "New Relic", "Kibana", "ELK Stack",

    # Servers
    "Apache", "Nginx", "Tomcat", "WildFly", "JBoss", "IIS",

    # Ticketing / ITSM
    "JIRA", "ServiceNow", "Zendesk", "Freshdesk", "Remedy",

    # Networking
    "TCP/IP", "DNS", "DHCP", "VPN", "Firewall", "Load Balancer",
    "SSH", "FTP", "SFTP", "HTTP", "HTTPS",

    # Security
    "OAuth", "JWT", "SSO", "LDAP", "Active Directory", "Cybersecurity",
    "Penetration Testing", "Vulnerability Management",

    # Data Engineering / Analytics
    "Pandas", "NumPy", "Matplotlib", "Power BI", "Tableau",
    "Excel", "Advanced Excel", "ETL", "Data Warehousing",

    # AI / ML
    "Machine Learning", "Deep Learning", "NLP", "TensorFlow",
    "PyTorch", "Scikit-learn", "OpenAI", "LLM", "LangChain",

    # QA / Testing
    "Selenium", "JUnit", "Pytest", "Cypress", "Playwright",
    "Manual Testing", "Automation Testing", "Load Testing",

    # Mobile
    "Android", "iOS", "React Native", "Flutter",

    # ERP / CRM
    "SAP", "Salesforce", "CRM", "ERP",

    # Support / Operations
    "Technical Support", "Production Support", "Application Support",
    "Incident Management", "Problem Management", "Change Management",
    "Root Cause Analysis", "RCA", "SLA", "Troubleshooting",
    "Log Analysis", "Monitoring", "Customer Support",

    # Finance / Business
    "Accounting", "Tally", "MIS Reporting", "Business Analysis",
    "Agile", "Scrum", "Kanban", "Project Management"
]


def extract_skills(text):

    found_skills = []

    text_lower = text.lower()

    for skill in MASTER_SKILLS:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))
