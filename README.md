# AWS Bedrock RAG-Based E-Learning Chatbot

An AI-powered e-learning assistant designed to help users find and understand learning materials through a conversational interface. The project uses a Retrieval-Augmented Generation (RAG) architecture with AWS services.

## Overview

The AWS Bedrock RAG-Based E-Learning Chatbot aims to provide an interactive learning experience by allowing users to ask questions about educational content in natural language.

The application is designed to retrieve relevant information from a knowledge base and use a foundation model to generate context-aware responses.

The project combines a Streamlit-based frontend with AWS services, including Amazon Bedrock Knowledge Bases, AWS Lambda, and Amazon API Gateway.

**Note:** The foundation model invocation is not working yet. The end-to-end RAG response-generation workflow is still under development and requires successful foundation model integration and testing.

## Objectives

- Build a conversational interface for an e-learning assistant.
- Explore Retrieval-Augmented Generation (RAG) for question answering.
- Integrate AWS managed AI services into a cloud-based application.
- Develop a serverless backend using AWS Lambda and API Gateway.
- Learn how knowledge retrieval and foundation models work together.
- Build practical experience with Generative AI and AWS cloud services.

## Key Features

- **Interactive Chat Interface:** A Streamlit-based interface for submitting learning-related questions.
- **Knowledge Base Integration:** Designed to retrieve relevant educational content using Amazon Bedrock Knowledge Bases.
- **Serverless Backend:** AWS Lambda handles backend request processing.
- **API Integration:** Amazon API Gateway provides an HTTP endpoint for frontend-to-backend communication.
- **Configurable API Endpoint:** The Streamlit interface allows the API endpoint to be configured.
- **Context-Aware Responses:** Planned functionality to generate answers grounded in retrieved learning materials using a foundation model.

*Feature availability depends on successful integration and testing of the corresponding AWS services.*

## Technology Stack

| Category | Technologies |
|---|---|
| Frontend | Python, Streamlit |
| Generative AI | Amazon Bedrock |
| Retrieval | Amazon Bedrock Knowledge Bases |
| Backend | AWS Lambda |
| API Layer | Amazon API Gateway |
| Language | Python |
| Architecture | Retrieval-Augmented Generation (RAG), Serverless Computing |

## System Architecture

The planned request flow is:

1. The user enters a question in the Streamlit application.
2. The frontend sends the question to an API Gateway endpoint.
3. AWS Lambda receives and processes the request.
4. Amazon Bedrock Knowledge Bases retrieves relevant content.
5. A supported foundation model generates an answer using the retrieved context.
6. The backend returns the response to the Streamlit application.
7. The answer is displayed to the user.

**Current limitation:** The foundation model invocation step is not yet operational. Therefore, the complete question-to-generated-answer workflow has not been verified.

## What Is RAG?

Retrieval-Augmented Generation (RAG) combines information retrieval with generative AI.

Instead of relying only on a model's pre-trained knowledge, a RAG application retrieves relevant information from an external knowledge source and provides it as context for generating an answer.

A typical RAG workflow includes:

- **Retrieval:** Find relevant documents or passages.
- **Augmentation:** Provide the retrieved context alongside the user's question.
- **Generation:** Use a foundation model to formulate a response grounded in that context.


This is a suggested structure. Update the filenames to match the files actually present in your project. The Lambda code may also be maintained separately in the AWS Console.

## Setup and Execution

### Prerequisites

- Python 3.10 or another version supported by your installed dependencies.
- An AWS account with the required permissions.
- An API Gateway endpoint configured for the backend.
- An appropriately configured Amazon Bedrock Knowledge Base.
- Access to a supported foundation model, with the required permissions and configuration.

## Challenges and Learning

During development, foundation model invocation returned an AWS Bedrock validation error indicating that the operation was not allowed.

Troubleshooting this issue involves checking model access and availability, supported API operations, IAM permissions, and compatibility between the selected model and the chosen Bedrock API.

Resolving this issue is a current development goal.

## Future Enhancements

- Complete foundation model integration.
- Generate answers grounded in retrieved educational documents.
- Add source references to chatbot responses.
- Improve error handling and API response validation.
- Add chat history and session management.
- Evaluate retrieval relevance and answer quality.
- Improve deployment documentation and monitoring.

## Security Considerations

- Never commit AWS access keys or secret keys.
- Use IAM roles and least-privilege permissions.
- Avoid committing `.env` files and sensitive configuration.
- Do not upload private or copyrighted learning materials without permission.
- Monitor AWS usage and costs during testing.

## Disclaimer

This project is an educational and portfolio project developed to explore Generative AI, Retrieval-Augmented Generation, and AWS cloud services. The foundation model integration is still in progress, and the complete RAG workflow has not yet been verified.

## Author

**Sayali Ramprasad Gayake**  
BE Computer Engineering Graduate  
Interests: Generative AI, Machine Learning, Python, and AWS Cloud Computing.

