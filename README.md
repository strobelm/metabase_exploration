# Customer Support Analytics

Customer support ticket ETL pipeline with Metabase dashboard.

## Data Overview

The system processes customer support ticket data with the following attributes:

### Data Schema

| Column Name                  | Description                                                                                                              | Data Type    |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------ |
| ticket_id                    | Unique identifier for each customer ticket                                                                               | INTEGER      |
| customer_name                | Full name of the customer                                                                                                | VARCHAR(100) |
| customer_email               | Email address of the customer                                                                                            | VARCHAR(100) |
| customer_age                 | Age of the customer in years                                                                                             | INTEGER      |
| customer_gender              | Gender of the customer (Male, Female, Other)                                                                             | VARCHAR(20)  |
| product_purchased            | Name of the product the customer purchased                                                                               | VARCHAR(100) |
| date_of_purchase             | Date when the product was purchased                                                                                      | DATE         |
| ticket_type                  | Category of the support ticket (Technical issue, Billing inquiry, Product inquiry, Refund request, Cancellation request) | VARCHAR(50)  |
| ticket_subject               | Brief description of the issue                                                                                           | VARCHAR(200) |
| ticket_description           | Detailed explanation of the customer's issue                                                                             | TEXT         |
| ticket_status                | Current status of the ticket (Open, Closed, Pending Customer Response)                                                   | VARCHAR(50)  |
| resolution                   | Description of how the issue was resolved (for closed tickets)                                                           | TEXT         |
| ticket_priority              | Urgency level of the ticket (Low, High, Critical)                                                                        | VARCHAR(20)  |
| ticket_channel               | Platform through which the ticket was submitted                                                                          | VARCHAR(50)  |
| first_response_time          | Timestamp of the first response from the support team                                                                    | TIMESTAMP    |
| time_to_resolution           | Timestamp when the ticket was resolved                                                                                   | TIMESTAMP    |
| customer_satisfaction_rating | Customer's rating of the support provided (1-5 scale)                                                                    | REAL         |

Sample data includes technical issues, billing inquiries, refund requests, and product inquiries across various products like electronics, software, and appliances.

### Sample Data Entries

```
1. Ticket ID: 3
   Customer: Christopher Robbins (gonzalestracy@example.com)
   Age/Gender: 48, Other
   Product: Dell XPS
   Purchase Date: July 14, 2020
   Type: Technical issue
   Subject: Network problem
   Description: I'm facing a problem with my Dell XPS. The Dell XPS is not turning on. It was working fine until yesterday, but now it doesn't respond.
   Status: Closed
   Resolution: Case maybe show recently my computer follow.
   Priority: Low

2. Ticket ID: 7
   Customer: Jacqueline Wright (donaldkeith@example.org)
   Age/Gender: 24, Other
   Product: Microsoft Surface
   Purchase Date: February 23, 2020
   Type: Product inquiry
   Subject: Refund request
   Description: I'm unable to access my Microsoft Surface account. It keeps displaying an 'Invalid Credentials' error, even though I'm using the correct login information. How can I regain access to my account?
   Status: Open
   Priority: Critical

3. Ticket ID: 16
   Customer: Elizabeth Foley (amy41@example.net)
   Age/Gender: 18, Other
   Product: GoPro Action Camera
   Purchase Date: June 24, 2021
   Type: Billing inquiry
   Subject: Product recommendation
   Description: I've noticed a sudden decrease in battery life on my GoPro Action Camera. It used to last much longer.
   Status: Pending Customer Response
   Priority: High
```

## Metabase Views

The system includes several pre-configured SQL views for the Metabase dashboard:

### 1. ticket_stats_by_product

Provides aggregated statistics for each product:

- Total tickets count
- Closed/open/pending ticket counts
- Average customer satisfaction rating
- Count of rated tickets

### 2. ticket_stats_by_channel

Shows performance metrics for each support channel:

- Total tickets per channel
- Unique customer count
- Closed ticket count
- Average satisfaction rating

### 3. ticket_priority_distribution

Displays the distribution of tickets by priority level:

- Ticket count per priority
- Percentage of total tickets

### 4. open_ticket_age

Lists all open tickets with their age for follow-up:

- Ticket details (ID, customer, product, subject)
- Time elapsed since first response
- Current status

### 5. resolution_time_stats

Provides resolution time metrics by priority:

- Average hours to resolve
- Minimum/maximum resolution time
- Invalid time entry count

### 6. customer_demographics

Shows customer data segmented by demographics:

- Age group breakdown
- Gender distribution
- Average satisfaction by demographic group

### 7. monthly_ticket_trends

Tracks ticket volumes and metrics over time:

- Monthly ticket totals
- Closed ticket count by month
- Average satisfaction rating trends
- Unique customer count by month

### 8. product_age_at_ticket

Analyzes the relationship between purchase date and ticket creation:

- Days between purchase and ticket creation

### 9. ticket_description_keywords

Performs basic text analysis on ticket descriptions:

- Common words/terms in tickets
- Word frequency counts

## Quick Start

```
docker compose up -d
```

Access Metabase: http://localhost:3000

Login: admin@example.com / p4ssword1

## Components

- ETL Pipeline (Python/Polars)
- PostgreSQL Database
- Metabase Dashboard
