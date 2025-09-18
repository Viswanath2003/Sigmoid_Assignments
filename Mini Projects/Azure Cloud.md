# Azure cloud assignment

# Azure Cloud Mini-Projects for DataOps

## Project 1: Azure Storage & Data Lake Architecture

**Duration**: 3-4 hours

**Difficulty**: Beginner-Intermediate

### Objective

Design and implement a multi-tier data storage architecture using Azure Storage services for a DataOps pipeline.

### Tasks

1. **Azure Storage Account Setup**
    - Create Storage Account with different access tiers (Hot, Cool, Archive)
    - Configure Blob Storage containers for:
        - `raw-data` (incoming data)
        - `processed-data` (transformed data)
        - `archived-data` (historical data)
        - `backup-data` (disaster recovery)
2. **Data Lake Gen2 Implementation**
    - Enable hierarchical namespace
    - Create file system structure:
        
        ```
        datalake/├── bronze/ (raw data)│   ├── sales/│   ├── customers/│   └── products/├── silver/ (cleaned data)│   ├── sales_processed/│   ├── customer_profiles/│   └── product_catalog/└── gold/ (aggregated data)    ├── daily_sales_summary/    ├── customer_analytics/    └── product_performance/
        
        ```
        
3. **Access Control & Security**
    - Configure Azure AD authentication
    - Set up RBAC roles for different team members:
        - Data Engineers (Contributor)
        - Data Analysts (Reader)
        - Data Scientists (Custom role)
    - Implement SAS tokens for temporary access
4. **Lifecycle Management**
    - Create lifecycle policies to automatically:
        - Move data to Cool tier after 30 days
        - Move data to Archive tier after 180 days
        - Delete old backup data after 7 years

### Deliverables

- ARM template or Azure CLI script for infrastructure
- Documentation of storage architecture design
- Access control matrix
- Cost optimization report

### Key Learning Outcomes

- Azure storage tiers and cost optimization
- Data Lake architecture best practices
- Security and access management
- Infrastructure as Code basics

---

## Project 2: Azure Virtual Machines for Data Processing

**Duration**: 4-5 hours

**Difficulty**: Intermediate

### Objective

Deploy and configure Azure VMs for distributed data processing workloads with proper monitoring and scaling.

### Tasks

1. **VM Deployment & Configuration**
    - Deploy Ubuntu VM for data processing
    - Install and configure:
        - Python 3.9+ with data libraries (pandas, numpy, dask)
        - Docker and docker-compose
        - Azure CLI
        - Monitoring agents
    - Create custom VM image for reuse
2. **Virtual Machine Scale Sets (VMSS)**
    - Create VMSS for auto-scaling data processing
    - Configure scaling rules based on:
        - CPU utilization > 70%
        - Memory usage > 80%
        - Queue length in Storage Queue
    - Set up automatic scaling policies
3. **Load Balancer & Traffic Management**
    - Configure Azure Load Balancer
    - Set up health probes for data processing services
    - Implement session persistence for stateful processing
4. **Backup & Disaster Recovery**
    - Configure Azure Backup for VMs
    - Create recovery plans
    - Test disaster recovery procedures
    - Document RTO and RPO requirements
5. **Monitoring & Alerting**
    - Enable Azure Monitor for VMs
    - Create custom metrics for:
        - Data processing throughput
        - Queue processing time
        - Error rates
    - Set up alerts for critical thresholds

### Deliverables

- VM deployment automation scripts
- VMSS configuration templates
- Monitoring dashboard
- Disaster recovery runbook

### Key Learning Outcomes

- VM management and optimization
- Auto-scaling strategies for data workloads
- Monitoring and alerting best practices
- Business continuity planning

---

## Project 3: Azure Networking for Secure Data Operations

**Duration**: 3-4 hours

**Difficulty**: Intermediate-Advanced

### Objective

Design and implement secure network architecture for DataOps workloads with proper isolation and connectivity.

### Tasks

1. **Virtual Network Design**
    - Create VNet with multiple subnets:
        - `data-ingestion-subnet` (10.0.1.0/24)
        - `data-processing-subnet` (10.0.2.0/24)
        - `data-storage-subnet` (10.0.3.0/24)
        - `management-subnet` (10.0.4.0/24)
2. **Network Security Groups (NSG)**
    - Create NSGs for each subnet with appropriate rules:
        - Allow HTTPS (443) for data ingestion
        - Allow SSH (22) only from management subnet
        - Block direct internet access to storage subnet
        - Allow internal communication between processing subnets
3. **Azure Private Endpoints**
    - Configure Private Endpoints for:
        - Storage Accounts
        - Key Vault
        - SQL Database
    - Set up Private DNS zones for name resolution
4. **VPN & Hybrid Connectivity**
    - Set up Site-to-Site VPN (simulation)
    - Configure ExpressRoute (documentation only)
    - Implement Point-to-Site VPN for remote access
5. **Network Monitoring**
    - Enable Network Watcher
    - Set up Flow Logs for NSGs
    - Create network topology diagrams
    - Implement connection monitoring

### Deliverables

- Network architecture diagram
- NSG rule documentation
- Private endpoint configuration guide
- Network monitoring dashboard

### Key Learning Outcomes

- Secure network design principles
- Private connectivity implementation
- Network monitoring and troubleshooting
- Hybrid cloud networking concepts

---

## Project 4: Azure SQL Database for Data Warehousing

**Duration**: 4-5 hours

**Difficulty**: Intermediate-Advanced

### Objective

Implement Azure SQL Database as a data warehouse with proper performance optimization and security.

### Tasks

1. **SQL Database Deployment**
    - Create Azure SQL Database (General Purpose tier)
    - Configure elastic pool for multiple databases
    - Set up read replicas for reporting workloads
    - Enable auto-scaling
2. **Data Warehouse Schema Design**
    - Create star schema for sales analytics:
        - Fact table: `sales_transactions`
        - Dimension tables: `customers`, `products`, `time`, `locations`
    - Implement proper indexing strategy
    - Create columnstore indexes for analytics
3. **Security Implementation**
    - Enable Azure AD authentication
    - Configure Always Encrypted for sensitive data
    - Set up Transparent Data Encryption (TDE)
    - Implement Row Level Security (RLS)
    - Configure Dynamic Data Masking
4. **Performance Optimization**
    - Enable Query Performance Insights
    - Create and optimize stored procedures
    - Implement partitioning strategies
    - Set up automated tuning
5. **Backup & High Availability**
    - Configure automated backups
    - Set up geo-replication
    - Test point-in-time recovery
    - Implement failover groups

### Deliverables

- Database schema documentation
- Security configuration guide
- Performance optimization report
- Backup and recovery procedures

### Key Learning Outcomes

- Data warehouse design principles
- Azure SQL security features
- Performance tuning techniques
- High availability and disaster recovery

---

## Project 5: Azure Key Vault & Secrets Management

**Duration**: 2-3 hours

**Difficulty**: Intermediate

### Objective

Implement comprehensive secrets management for DataOps pipelines using Azure Key Vault.

### Tasks

1. **Key Vault Setup**
    - Create Azure Key Vault
    - Configure access policies for different roles
    - Enable soft delete and purge protection
    - Set up network restrictions
2. **Secrets Management**
    - Store various types of secrets:
        - Database connection strings
        - API keys for external services
        - Certificates for HTTPS
        - SSH keys for VM access
    - Implement secret versioning
    - Set up automatic secret rotation
3. **Integration with Services**
    - Configure VM to retrieve secrets from Key Vault
    - Set up managed identity for authentication
    - Integrate with Azure Functions
    - Connect to Azure DevOps for CI/CD
4. **Monitoring & Auditing**
    - Enable Key Vault logging
    - Set up alerts for unauthorized access attempts
    - Create audit reports
    - Monitor secret usage patterns

### Deliverables

- Key Vault configuration documentation
- Secret management procedures
- Integration examples with code
- Security audit report

### Key Learning Outcomes

- Secrets management best practices
- Managed identity implementation
- Security monitoring and auditing
- Service integration patterns

---

## Project 6: Azure Resource Management & Cost Optimization

**Duration**: 3-4 hours

**Difficulty**: Intermediate

### Objective

Implement proper resource management and cost optimization strategies for DataOps workloads.

### Tasks

1. **Resource Organization**
    - Create resource group hierarchy:
        - `rg-dataops-dev`
        - `rg-dataops-staging`
        - `rg-dataops-prod`
    - Implement consistent naming conventions
    - Apply resource tags for cost tracking
2. **Azure Resource Manager (ARM) Templates**
    - Create ARM templates for:
        - Complete data processing environment
        - Storage account with lifecycle policies
        - VM with monitoring extensions
        - SQL database with security settings
    - Implement parameter files for different environments
3. **Cost Management & Billing**
    - Set up cost alerts and budgets
    - Analyze spending patterns
    - Identify cost optimization opportunities
    - Create cost allocation reports by department/project
4. **Azure Policy Implementation**
    - Create policies to enforce:
        - Required tags on resources
        - Allowed VM SKUs
        - Storage account encryption
        - Network security requirements
    - Implement compliance reporting
5. **Automation & Governance**
    - Set up Azure Automation for:
        - Start/stop VMs on schedule
        - Automated backups
        - Resource cleanup
    - Create runbooks for common tasks

### Deliverables

- ARM template library
- Cost optimization report
- Azure Policy definitions
- Automation runbooks

### Key Learning Outcomes

- Infrastructure as Code best practices
- Cost management strategies
- Governance and compliance
- Automation implementation

---

## Assessment Criteria

### For Each Project:

- **Technical Implementation** (30%): Correct configuration and deployment
- **Security Best Practices** (25%): Proper access control and data protection
- **Documentation Quality** (25%): Clear, comprehensive documentation
- **Cost Optimization** (20%): Efficient resource usage and cost-awareness

### Portfolio Readiness Checklist:

- [ ]  All resources properly tagged and organized
- [ ]  Security configurations documented and implemented
- [ ]  Cost optimization strategies applied
- [ ]  ARM templates or automation scripts included
- [ ]  Architecture diagrams and documentation
- [ ]  Real-world DataOps scenarios demonstrated

---

## Integration with Git/GitHub Projects:

- Store all ARM templates and scripts in Git repository
- Document infrastructure changes through commit history
- Use GitHub Actions for infrastructure deployment (future project)
- Version control all configuration files

## Next Steps:

1. Complete projects in order (1-6)
2. Document lessons learned and challenges faced
3. Create a consolidated Azure architecture for your portfolio
4. Prepare to integrate with Azure DevOps for CI/CD

## Tips for Success:

- Start with free tier resources to minimize costs
- Clean up resources after testing to avoid charges
- Use Azure CLI or PowerShell for automation
- Document security configurations thoroughly
- Test disaster recovery procedures
- Monitor costs regularly during development
