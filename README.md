# Smart order processor

This is a lightweight order management solution intended to be created and deployed in Azure. In this project, orders can be created, received and payment processing is possible. Orders flow through an event-driven architecture using Service Bus and Logic Apps for reliable processing and notifications.

## Purpose

The purpose of this project is to demonstrate Azure integration patterns including, event driven architecture, serverless computing, and CI/CD pipelines.

## Tech Stack
- Bicep
- Azure Functions
- Azure Service Bus
- Azure Logic Apps
- Azure API Management (APIM)
- Azure Cosmos DB
- Azure DevOps (CI/CD)

## Project Structure
- `infra/` — Bicep templates for all Azure infrastructure
- `functions/` — Python Azure Functions (place_order, get_order_status, process_payment)
- `logic-apps/` — Logic App workflow definitions (order flow, payment flow)
- `tests/` — Pytest unit tests for Azure Functions
- `azure-pipelines.yml` — CI/CD pipeline definition
