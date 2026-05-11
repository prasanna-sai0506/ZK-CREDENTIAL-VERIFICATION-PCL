# ZK CREDENTIAL VERIFICATION SYSTEM
## Document-Agnostic On-Chain Identity Using Zero-Knowledge Proofs

---

# PROJECT REPORT

Submitted in partial fulfillment of requirements for advancing Zero-Knowledge Cryptography and Decentralized Identity Systems.

## AUTHOR INFORMATION

**Project Title:** ZK Credential Verification System – LLM-Driven Claim Extraction with Zero-Knowledge Proofs

**Development Period:** 2025-2026

**Repository:** zk-credential

**Technology Stack:** React 18 + Vite, FastAPI, Celery + Redis, PostgreSQL, GPT-4o/LLaMA, Circom 2.1, snarkjs, Solidity + Hardhat

---

# CANDIDATE'S DECLARATION

We hereby certify that this project report entitled "ZK Credential Verification System – Document-Agnostic On-Chain Identity" represents an authentic record of our work and development efforts. All components, implementations, and integrations described herein have been developed according to industry best practices and academic standards.

The research and implementation have not been submitted for any other degree or published elsewhere without proper attribution.

---

# ACKNOWLEDGEMENT

We extend our sincere gratitude to the open-source communities behind Circom, snarkjs, FastAPI, and the LLM providers that made this project possible. Special thanks to the Zero-Knowledge Proofs research community and blockchain development platforms for providing the foundational technologies. We acknowledge the contributions of all team members and stakeholders who provided feedback throughout the development lifecycle.

---

# ABSTRACT

The ZK Credential Verification System addresses a critical challenge in digital identity verification: enabling third-party verification of claims from identity documents without exposing the raw document content. Traditional identity verification systems require users to share complete documents with verifiers, creating significant privacy risks and regulatory compliance challenges.

This project introduces an innovative solution that combines Large Language Models (LLMs) with Zero-Knowledge Cryptography to create a document-agnostic verification framework. Users upload identity documents (passports, degrees, employment letters, etc.) in any format. An LLM-powered service extracts structured claims from these documents while maintaining privacy through encryption-at-rest and in-transit mechanisms. These extracted claims are transformed into cryptographic proofs using Circom-based Groth16 zero-knowledge circuits. The resulting proofs are posted on-chain via a Solidity smart contract, allowing third-party verifiers to cryptographically validate claims without ever accessing the original documents.

The system architecture integrates multiple cutting-edge technologies: React 18 with Vite for the frontend, FastAPI for backend services, Celery for asynchronous task processing, PostgreSQL for persistent storage, and blockchain infrastructure for immutable proof verification. The workflow is secured end-to-end with AES-256-GCM encryption, JWT authentication, and cryptographic commitment schemes.

**Keywords:** Zero-Knowledge Proofs, Groth16, Circom, Decentralized Identity, LLM-Based Extraction, Smart Contracts, Privacy-Preserving Verification, Cryptographic Commitment, On-Chain Verification, Document Processing

---

# TABLE OF CONTENTS

1. Introduction
   - 1.1 Project Overview
   - 1.2 Problem Statement
   - 1.3 Objectives and Goals
   - 1.4 System Overview

2. Technologies and Libraries Used
   - 2.1 Frontend Technologies
   - 2.2 Backend Technologies
   - 2.3 Blockchain and Cryptography
   - 2.4 External Services

3. Application Architecture
   - 3.1 System Architecture Overview
   - 3.2 Core Modules
   - 3.3 Data Flow and Processing Pipeline

4. Frontend Implementation
   - 4.1 React 18 + Vite Framework
   - 4.2 User Interface Components
   - 4.3 State Management with Zustand
   - 4.4 Wallet Integration

5. Backend Services
   - 5.1 FastAPI Framework
   - 5.2 Authentication and Security
   - 5.3 Core Service Modules
   - 5.4 Database Design

6. Document Processing and LLM Integration
   - 6.1 Document Upload and Storage
   - 6.2 LLM-Based Claim Extraction
   - 6.3 Claim Validation and Normalization

7. Zero-Knowledge Proof Generation
   - 7.1 Circom Circuit Design
   - 7.2 Witness Generation
   - 7.3 Proof Generation with snarkjs

8. Smart Contract Integration
   - 8.1 Solidity CredentialVerifier Contract
   - 8.2 On-Chain Verification Logic
   - 8.3 Contract Deployment Strategy

9. Asynchronous Task Processing
   - 9.1 Celery Architecture
   - 9.2 Task Pipeline
   - 9.3 Redis Integration

10. Security and Encryption
    - 10.1 End-to-End Encryption
    - 10.2 JWT Authentication
    - 10.3 Data Protection Measures
    - 10.4 Secrets Management

11. Deployment and DevOps
    - 11.1 Docker Containerization
    - 11.2 Docker Compose Configuration
    - 11.3 Environment Configuration
    - 11.4 Production Deployment

12. Testing and Validation
    - 12.1 Circuit Testing
    - 12.2 API Testing
    - 12.3 End-to-End Smoke Testing
    - 12.4 Security Testing

13. Future Enhancements
    - 13.1 Scalability Improvements
    - 13.2 Additional Document Types
    - 13.3 Advanced Features

14. Challenges and Solutions
    - 14.1 Technical Challenges
    - 14.2 Implemented Solutions

15. Conclusion

16. References

---

# 1. INTRODUCTION

## 1.1 Project Overview

The ZK Credential Verification System represents a paradigm shift in how digital identity verification can be conducted in decentralized environments. In our increasingly digital world, the verification of identity credentials has become both more important and more challenging. Organizations need to verify claims about individuals—such as age, citizenship, educational qualifications, or employment status—while individuals rightfully demand privacy protection for their sensitive documents.

Traditional identity verification systems operate on a "document sharing" model: a user must provide complete copies of their identity documents to any organization that needs to verify a claim. This approach creates multiple problems. First, it violates the principle of data minimization by sharing entire documents when only specific claims are needed. Second, it creates significant privacy risks, as documents often contain sensitive information beyond what needs verification. Third, it creates regulatory compliance challenges under frameworks like GDPR and regulations in multiple jurisdictions that aim to protect personal data.

The ZK Credential Verification System solves these problems through a novel combination of technologies. The system enables users to upload any identity document and have the system automatically extract relevant claims using Large Language Models. These claims are then converted into cryptographic commitments and zero-knowledge proofs that can be verified on-chain without revealing the original document or extracted data to verifiers.

The system operates on the principle that verification should be a binary cryptographic operation: either a claim is valid (and the proof is accepted), or it is not. No intermediate data, no document content, and no personal information associated with the document needs to be shared with verifiers. This represents a genuine advance in privacy-preserving identity verification.

## 1.2 Problem Statement

Contemporary digital identity systems face several critical challenges:

**Privacy Erosion:** When organizations request document verification, they typically require users to share complete identity documents. A passport, for example, contains biometric information, security features, and numerous data fields beyond what needs verification. Sharing entire documents unnecessarily exposes individuals to privacy violations.

**Data Accumulation and Proliferation:** Each organization that collects identity documents creates a new data store containing sensitive personal information. This creates an ever-expanding attack surface for data breaches. The more organizations hold copies of identity documents, the higher the probability of unauthorized access or misuse.

**Regulatory Compliance Burden:** International regulations like GDPR, CCPA, and emerging frameworks in other jurisdictions mandate organizations to hold only the minimum data necessary for their purposes. Document-sharing verification mechanisms conflict directly with these regulatory requirements.

**Fraud Prevention and Authenticity:** Traditional document verification relies on visual inspection or simple digital validation, which does not permanently establish authentic claims on immutable systems. There is no cryptographic guarantee that a verified claim remains valid or that the verification was legitimate.

**Cross-Border Complications:** Identity documents are issued by different governments and bodies worldwide. No unified mechanism exists for cryptographically verifying claims across jurisdictions in a trustless manner.

**Document Format Heterogeneity:** Identity documents come in countless formats—passports, national ID cards, educational transcripts, employment letters, certificates, etc. Organizations struggle to support multiple document types and extraction standards.

The ZK Credential Verification System directly addresses each of these pain points by introducing a cryptographic, privacy-preserving, and document-agnostic verification framework.

## 1.3 Objectives and Goals

### Primary Objectives

1. **Privacy-First Design:** Enable claim verification without exposing raw documents or extracted data to verifiers. Implement encryption mechanisms that ensure no intermediate party (except the claim issuer) can access document content.

2. **Automated Claim Extraction:** Leverage modern Large Language Models to automatically extract structured claims from unstructured identity documents, eliminating manual data entry and supporting document format heterogeneity.

3. **Cryptographic Commitment:** Implement zero-knowledge proof technology to create unforgeable cryptographic proofs of claims that can be independently verified on-chain without accessing the original document.

4. **Document-Agnostic Processing:** Support multiple document formats (PDFs, images, scanned documents) and document types (passports, degrees, employment letters, etc.) through flexible LLM-based extraction.

5. **On-Chain Permanence:** Implement smart contracts that enable immutable recording and verification of cryptographic proofs on public blockchains, creating a permanent audit trail.

### Secondary Objectives

1. **User Experience Excellence:** Provide an intuitive interface that requires minimal technical knowledge while handling complex cryptographic operations transparently.

2. **Security Assurance:** Implement industry-standard encryption, authentication, and secure development practices throughout the system.

3. **Scalability and Performance:** Design the system to handle high throughput while maintaining security and privacy guarantees.

4. **Extensibility:** Create a modular architecture that allows future enhancements such as different LLM providers, additional circuit designs, and expanded claim types.

5. **Regulatory Compliance:** Ensure the system meets privacy regulations and provides verifiable logs for compliance documentation.

## 1.4 System Overview

The ZK Credential Verification System operates through a carefully orchestrated workflow:

**User Submission Phase:** A user accesses the web-based interface and uploads an identity document in any supported format (PDF, JPEG, PNG, etc.). The document is immediately encrypted using AES-256-GCM encryption with a key derived from the user's authentication credentials.

**Asynchronous Processing:** The encrypted document is queued for asynchronous processing using Celery, a distributed task queue system. This decouples the upload operation from intensive processing, enabling responsive user experience.

**Intelligent Claim Extraction:** The backend service decrypts the document and processes it using a Large Language Model (GPT-4o, LLaMA, or similar). The LLM extracts structured claims relevant to identity verification (age, nationality, educational qualifications, etc.) with context-aware understanding of document semantics.

**Claim Validation:** Extracted claims are validated against predefined schemas and rules. The system normalizes claims into standard formats (e.g., dates into ISO 8601 format, boolean values into consistent representation).

**Witness Generation:** Validated claims are converted into witness data compatible with the ZK circuit through a deterministic transformation process that preserves claim semantics while preparing data for cryptographic processing.

**ZK Proof Generation:** The snarkjs library generates a Groth16 zero-knowledge proof using the circuit and witness data. This proof demonstrates knowledge of valid claims without revealing claim details.

**On-Chain Submission:** The user submits the proof to the Ethereum network via the CredentialVerifier smart contract. The contract stores the proof indexed by the user's wallet address.

**Third-Party Verification:** Any third party can query the smart contract with a user's address and bitmap representing desired claims, receiving a boolean response indicating whether the user possesses a valid proof for those claims.

Throughout this workflow, privacy is maintained through multiple layers: document encryption, restrictive data access controls, and zero-knowledge cryptography.

---

# 2. TECHNOLOGIES AND LIBRARIES USED

## 2.1 Frontend Technologies

### React 18

React 18 serves as the foundational framework for the frontend application. React's component-based architecture enables modular UI development, facilitating code reuse and maintainability. The upgrade to React 18 provides significant performance improvements including automatic batching of state updates, which reduces unnecessary re-renders and improves responsiveness.

React 18's Suspense capability is leveraged for handling asynchronous operations elegantly. As documents are processed asynchronously, Suspense boundaries allow the UI to display loading states gracefully without blocking user interaction. The concurrent rendering features in React 18 enable the application to maintain responsiveness even during intensive computations.

### Vite

Vite replaces traditional bundlers like Webpack with a modern, developer-friendly approach. Vite uses native ES modules during development, providing near-instantaneous Hot Module Replacement (HMR). When a developer modifies a component, changes reflect in the browser in milliseconds, dramatically improving developer experience during active development.

For production, Vite generates optimized bundles using Rollup, ensuring efficient code splitting and minimal JavaScript payloads. The application benefits from Vite's tree-shaking capabilities, which eliminate unused code and reduce bundle sizes by up to 30-40% compared to traditional bundlers.

### Zustand State Management

Zustand provides a lightweight alternative to Redux for state management. The store-based architecture in this project uses Zustand for two primary stores:

**walletStore:** Manages blockchain wallet connection state, including connected addresses, network information, and balance data. This store handles wallet-specific operations without the overhead of larger state management libraries.

**jobStore:** Maintains the status of asynchronous jobs (document uploads, proof generation, verification). The store supports polling mechanisms for checking job status, enabling real-time UI updates as backend processes complete.

Zustand's minimalist API reduces boilerplate compared to Redux while providing sufficient power for this application's needs. The store updates trigger efficient re-renders only in components subscribed to relevant state changes.

### Wallet Integration (Web3.js/ethers.js)

The application integrates blockchain wallet functionality enabling users to connect their MetaMask or compatible wallets. This integration handles:

- Wallet connection and disconnection
- Transaction signing and submission
- Network switching (particularly Sepolia testnet for development)
- Gas estimation for contract interactions
- Account switching detection

The wallet integration allows users to submit ZK proofs to the blockchain programmatically, creating an immutable record of verified claims associated with their address.

### TypeScript

TypeScript provides static type checking across the entire frontend codebase, catching errors at development time rather than runtime. Type definitions are provided for all API responses, enabling IDE autocomplete and reducing debugging time. The strict mode configuration ensures comprehensive type coverage.

## 2.2 Backend Technologies

### FastAPI

FastAPI serves as the backend framework, chosen for its exceptional performance, intuitive API design, and automatic documentation generation. FastAPI leverages Python's type hints to provide OpenAPI documentation automatically, enabling external developers to understand the API without manual documentation maintenance.

Key features utilized:

- **Async/Await Support:** All I/O operations use async functions, enabling efficient handling of concurrent requests without blocking threads.
- **Dependency Injection:** FastAPI's dependency injection system simplifies authentication and database session management across routes.
- **Automatic Request Validation:** Pydantic models automatically validate incoming requests, rejecting invalid data before reaching business logic.
- **Middleware Support:** Custom middleware handles CORS, request logging, and error formatting.

FastAPI's performance benchmarks consistently rank it among the fastest Python web frameworks, with throughput comparable to Node.js/Go applications, making it suitable for the high-concurrency demands of this system.

### Pydantic

Pydantic provides data validation and serialization using Python type hints. All API request/response models are defined as Pydantic classes, ensuring:

- Automatic request parsing and validation
- Consistent error messages for validation failures
- Serialization of complex types (dates, UUIDs, custom objects)
- Runtime type checking with detailed error reporting

Custom validators in Pydantic models enforce business logic constraints (e.g., ensuring extracted claim values match expected patterns).

### SQLAlchemy ORM

SQLAlchemy provides an Object-Relational Mapping layer for database interactions. The ORM abstracts database operations, enabling:

- Database-agnostic Python code (could switch from PostgreSQL to another database)
- Lazy loading and relationship management
- Query optimization through careful relationship configuration
- Transaction management with automatic rollback on exceptions

### asyncpg

asyncpg is an asynchronous PostgreSQL adapter that maintains performance with I/O-bound operations. Unlike psycopg2 (the synchronous PostgreSQL adapter), asyncpg does not block the event loop, enabling true asynchronous database operations. This is critical for handling multiple concurrent requests efficiently.

### Celery

Celery is a distributed task queue that enables asynchronous processing of long-running operations. The document processing pipeline is implemented as a Celery task chain:

1. **Upload Acceptance:** FastAPI receives the document and queues a processing task
2. **Async Processing:** Celery workers process documents independently
3. **Status Polling:** The frontend polls the `/status` endpoint for current progress
4. **Completion Notification:** When processing completes, results are persisted to the database

Celery enables horizontal scaling by adding additional worker processes, allowing the system to handle increased document processing load.

### Redis

Redis serves as the message broker for Celery tasks and provides caching for frequently accessed data. The message broker receives task enqueue requests from FastAPI and distributes them to Celery workers. Redis's in-memory data structure enables efficient:

- Task queue management
- Result caching (reducing database queries)
- Session management (though persistent storage uses PostgreSQL)
- Real-time metrics tracking

## 2.3 Blockchain and Cryptography

### Circom

Circom is a circuit compiler for designing zero-knowledge circuits. The credential.circom circuit implements the mathematical constraints that zero-knowledge proofs must satisfy. The circuit is designed to:

- Accept extracted claim values as private inputs and public inputs (statement)
- Perform cryptographic verification of claim commitments
- Generate constraints that prove claim validity without revealing claim details
- Minimize circuit complexity to reduce proof generation time

The circuit uses Poseidon hash functions for efficient hashing within the circuit, which is optimized for zk-SNARKs compared to SHA-256.

### snarkjs

snarkjs is a JavaScript library that implements zk-SNARK functionality. The library provides:

- **Trusted Setup:** Generates circuit parameters (proving key, verification key) for Groth16
- **Witness Computation:** Converts claim data into witness format compatible with circuit
- **Proof Generation:** Generates cryptographic proofs using the proving key
- **Proof Verification:** Enables off-chain proof verification before contract interaction

### Hardhat

Hardhat is an Ethereum development environment providing:

- Smart contract compilation and deployment
- Testing framework for contract functionality
- Local blockchain (Hardhat Network) for development
- Network configuration for testnet and mainnet deployment
- Gas estimation and optimization tools

### Solidity

Solidity is the language for writing smart contracts. The CredentialVerifier contract implements:

- Proof verification logic using previously generated verification keys
- Storage of verified proof-to-address mappings
- Query functions enabling third parties to verify claims associated with addresses
- Access control preventing unauthorized proof submissions

## 2.4 External Services

### OpenAI GPT-4o and Groq LLaMA

The system integrates with LLM providers for intelligent claim extraction:

**OpenAI GPT-4o:** Selected for its superior understanding of document semantics and context. GPT-4o demonstrates exceptional performance on OCR'd text and handwritten documents, making it ideal for diverse document types.

**Groq LLaMA:** Provides a cost-effective alternative with faster inference speeds. LLaMA models are open-source and can be self-hosted, providing cost scalability.

The system is designed to support multiple providers through an abstraction layer, allowing fallback to alternative providers if one experiences outages.

### Pytesseract (Tesseract OCR)

For scanned documents or images without embedded text, Tesseract provides optical character recognition. The OCR output is passed to the LLM for claim extraction, enabling support for physical documents that have been scanned.

---

# 3. APPLICATION ARCHITECTURE

## 3.1 System Architecture Overview

The ZK Credential system follows a layered architecture emphasizing separation of concerns and scalability:

```
┌─────────────────────────────────────────────────────┐
│         USER INTERFACE LAYER (Frontend)             │
│   React 18 + Vite + Zustand + Web3.js              │
└────────────────┬────────────────────────────────────┘
                 │ HTTPS + JWT Auth
┌────────────────▼────────────────────────────────────┐
│      API LAYER (FastAPI)                            │
│  Routes - Auth - Validation - Error Handling       │
└────────────────┬────────────────────────────────────┘
                 │ Request Dispatch
┌────────────────▼────────────────────────────────────┐
│    SERVICE LAYER                                    │
│  Document Processing - Claim Extraction             │
│  Validation - ZK Generation                         │
└────────────────┬────────────────────────────────────┘
                 │ Data Persistence
┌────────────────▼────────────────────────────────────┐
│    DATA LAYER                                       │
│  PostgreSQL - Redis - Blob Storage (S3/Local)      │
└─────────────────────────────────────────────────────┘
                 │ Blockchain Interaction
┌────────────────▼────────────────────────────────────┐
│    BLOCKCHAIN LAYER                                 │
│  Smart Contracts - On-Chain Verification            │
└─────────────────────────────────────────────────────┘
```

This architecture provides clear separation allowing independent scaling and maintenance of each layer.

## 3.2 Core Modules

### API Module (backend/app/api/)

The API module implements FastAPI routes exposing system functionality. Key endpoints:

**Document Upload (POST /api/v1/documents/upload):** Accepts document uploads with multipart encoding. The endpoint:
- Authenticates the request using JWT tokens
- Generates a unique document ID
- Encrypts the document using AES-256-GCM
- Queues the processing task
- Returns document ID and job ID for status polling

**Job Status (GET /api/v1/jobs/{job_id}/status):** Provides real-time updates on asynchronous processing. Returns status enum (queued, processing, done, failed) and progress metadata.

**Proof Submission (POST /api/v1/proofs/submit):** Accepts user-signed proofs and submits them to the blockchain. Validates proof format before contract interaction.

**Claim Verification (POST /api/v1/verify):** Public endpoint enabling third parties to verify if an address possesses valid proofs for specified claims.

### Services Module (backend/app/services/)

**llm_parser.py:** Orchestrates LLM-based claim extraction from documents. The service:
- Decrypts uploaded documents
- Determines document type (PDF, image, etc.)
- Applies OCR if necessary
- Constructs detailed prompts for LLM
- Parses LLM responses into structured claims
- Implements fallback extraction using heuristic patterns

**claim_validator.py:** Validates extracted claims against predefined schemas. This service:
- Enforces claim value constraints
- Normalizes claim formats
- Detects and flags suspicious or malformed claims
- Generates validation reports

**zk_generator.py:** Implements the ZK proof generation pipeline:
- Compiles claims into witness data
- Generates Groth16 proofs
- Verifies proofs locally before submission
- Handles snarkjs integration

**storage.py:** Provides abstraction over storage backends (local filesystem, S3). Enables:
- Encrypted document storage
- Retrieval of stored documents
- Storage backend configuration switching

**document_parser.py:** Handles document format detection and initial parsing:
- Detects PDF vs. image formats
- Extracts text from PDFs using PyMuPDF
- Handles image encoding/decoding

### Tasks Module (backend/app/tasks/)

**proof_task.py:** Implements the Celery task pipeline for document processing:

```
upload_document
  ├─> decrypt_and_parse
  ├─> extract_claims (LLM)
  ├─> validate_claims
  ├─> generate_proof (ZK)
  └─> store_metadata
```

Each pipeline step includes error handling and logging, with failures triggering notifications and retry logic.

### Models Module (backend/app/models/)

**database.py:** Defines SQLAlchemy ORM models:

- **Document:** Stores document metadata (upload timestamp, user, encryption key reference)
- **Job:** Tracks async job status and progress
- **Claim:** Stores extracted claims with validation status
- **Proof:** Records generated proofs and blockchain submission status

**schemas.py:** Defines Pydantic models for request/response validation, ensuring consistent API contracts.

## 3.3 Data Flow and Processing Pipeline

The complete data flow from document upload to on-chain verification:

**Phase 1 - Upload & Encryption:**
1. User selects document in frontend
2. Document is encrypted client-side (optional) or server-side
3. POST request to `/api/v1/documents/upload`
4. FastAPI returns `{ doc_id, job_id }`

**Phase 2 - Asynchronous Processing:**
1. Celery dequeues the processing task
2. Document is retrieved and decrypted
3. Format detection (PDF vs. image)
4. Text extraction using PyMuPDF or OCR
5. LLM processes extracted text, generates claims

**Phase 3 - Validation & Storage:**
1. Extracted claims validated against schema
2. Claims normalized into standard formats
3. Claim data persisted to database
4. Status updated to "validation_complete"

**Phase 4 - ZK Proof Generation:**
1. Claims converted to witness format
2. snarkjs generates Groth16 proof
3. Proof verified locally
4. Proof and metadata stored to database
5. Status updated to "done"

**Phase 5 - Blockchain Submission:**
1. User signs proof with wallet
2. Frontend submits proof to CredentialVerifier contract
3. Contract emits event and stores proof mapping

**Phase 6 - Verification:**
1. Third party queries contract with `(address, claim_bitmap)`
2. Contract checks if matching proof exists
3. Returns boolean result

---

# 4. FRONTEND IMPLEMENTATION

## 4.1 React 18 + Vite Framework

The frontend is built as a Single Page Application (SPA) using React 18 with Vite as the build tool. The architecture emphasizes performance, maintainability, and user experience.

### Component Structure

Components are organized hierarchically with clear responsibility boundaries:

**Page Components** (`pages/`):
- `Upload.tsx`: Document upload interface and processing status
- `Dashboard.tsx`: Central hub displaying job history and proof status
- `Verify.tsx`: Third-party verification interface

**Functional Components** (`components/`):
- `UploadZone.tsx`: Drag-and-drop file upload with format validation
- `ProofCard.tsx`: Displays proof details and submission status
- `WalletButton.tsx`: Wallet connection and account management

Each component is implemented as a functional component using React hooks, ensuring modern React patterns throughout the application.

### Vite Configuration

Vite is configured to optimize development and production builds. Key features include API proxying to the development FastAPI server, modern JavaScript target compatibility, manual chunk splitting for optimized caching, and development hot-reload for rapid iteration. The configuration balances developer experience with production performance requirements.

## 4.2 User Interface Components

### UploadZone Component

The `UploadZone` component provides the primary user interaction point for document submission. It implements drag-and-drop functionality, file validation, and integration with the job store for status tracking. When users drag documents over the drop zone, visual feedback indicates the drop is enabled. Upon file selection or drop, the component validates the file format, encrypts the document payload, and submits it to the backend API. The API response triggers job status polling through Zustand's job store, enabling real-time progress updates in the UI.

### ProofCard Component

The `ProofCard` displays extracted claims and generated proofs in a visually organized format. This component fetches proof details from the store, displays normalized claims with human-readable labels, and provides a submit button for users to post the proof to the blockchain. Before submission, the component verifies wallet connection and validates proof completeness. Upon successful submission, the component displays confirmation feedback and transitions the proof status to pending verification.

## 4.3 State Management with Zustand

Zustand stores are implemented for wallet and job state management. This lightweight state management approach replaces the need for more complex solutions like Redux while providing all necessary functionality for this application.

### Wallet Store

The wallet store manages blockchain connection state including user address, network information, and account balance. It provides methods to connect and disconnect MetaMask wallets, switch networks between testnet and mainnet, and handle network change events. The store maintains the current network context for proper transaction submission and proof verification.

### Job Store

The job store tracks all asynchronous document processing jobs with their current status (queued, processing, done, or failed). It provides methods to add new jobs, update progress as processing advances, and remove completed jobs. The store maintains a dictionary of jobs indexed by job ID, enabling real-time UI updates as background processing progresses. Components subscribe to job updates and automatically re-render when status changes occur.

## 4.4 Wallet Integration

The application integrates Web3 wallet functionality for blockchain interaction. A custom `useWeb3` hook initializes the ethers.js provider using MetaMask's injected Ethereum object, creating a bridge between the browser wallet and the application. The hook establishes listeners for account changes and network switches, automatically updating the wallet store when users change accounts or networks. The submit proof functionality uses the wallet's signer to sign transactions, ensuring user authorization for all blockchain operations. Contract interaction is abstracted through this hook, providing a clean interface for submitting proofs and querying verification status.

---

# 5. BACKEND SERVICES

## 5.1 FastAPI Framework

The FastAPI backend serves as the central processing engine, exposing REST endpoints for frontend consumption and coordinating asynchronous tasks.

### Route Organization

Routes are organized by domain concern with prefix routing. Each router module handles related endpoints, grouping authentication, document operations, job monitoring, and proof management respectively. This modular approach ensures clean separation of concerns and makes the codebase maintainable and scalable.

### Middleware Stack

Custom middleware handles cross-cutting concerns including CORS for enabling cross-origin requests from the frontend, request logging for debugging and monitoring, and error handling providing consistent error response formats. The middleware stack intercepts all requests before reaching route handlers, allowing centralized handling of security, observability, and error concerns.

## 5.2 Authentication and Security

### JWT Authentication

JWT tokens provide stateless authentication throughout the API. When users log in or submit documents, the system generates access tokens with 24-hour expiration and refresh tokens with 7-day expiration. Each API endpoint validates incoming tokens before processing requests. Token validation verifies the signature against the server's secret key and checks expiration time. The bearer token scheme is used for HTTP authorization headers, enabling standard HTTP authentication practices.

### Encryption at Rest and in Transit

Documents are encrypted using AES-256-GCM, one of the most secure symmetric encryption algorithms. A key derivation function (PBKDF2) converts user identifiers into encryption keys, ensuring each user's documents are independently protected. Each document receives a unique nonce and salt, preventing patterns across multiple documents. Encryption occurs before storage, whether in local filesystem or AWS S3, ensuring sensitive data remains encrypted in all locations.

## 5.3 Core Service Modules

### LLM Parser Service

The LLM parser orchestrates intelligent claim extraction from documents. It implements a multi-model strategy where GPT-4o is preferred for its advanced understanding of document semantics, followed by LLaMA models as a cost-effective alternative, and lastly heuristic-based extraction as a fallback when LLMs are unavailable. This redundancy ensures the system continues operating even during API outages. The extracted claims are validated against expected schemas before normalization.

### Claim Validator Service

The claim validator ensures extracted data integrity by validating against predefined schemas. Age values are checked against minimum and maximum life expectancy ranges. Nationality values are verified against a list of valid countries. Document expiration dates are parsed and validated. Any validation failures are logged with specific error messages for debugging and auditing purposes.

### ZK Generator Service

The ZK generator transforms validated claims into cryptographic proofs. It converts claims into witness data compatible with the Circom circuit, invokes snarkjs for proof generation, and verifies the generated proof locally before submission. This multi-stage approach catches issues early without requiring blockchain interaction.

## 5.4 Database Design

### SQLAlchemy Models

The database schema models all system entities through SQLAlchemy ORM models. The User model stores authentication credentials and wallet connections. The Document model tracks uploaded files with encryption parameters and storage locations. The Job model monitors asynchronous processing status and progress. The Claim model stores extracted claims with validation flags. The Proof model records generated zero-knowledge proofs along with blockchain submission details. Relationships between models enable queries across the system, such as retrieving all claims for a specific job or all proofs submitted by a user.

---

# 6. DOCUMENT PROCESSING AND LLM INTEGRATION

## 6.1 Document Upload and Storage

Document handling implements a secure, encrypted storage pipeline. When a user uploads a document, the system immediately encrypts it using the user's derived encryption key. The encrypted content is stored either in AWS S3 (for production scalability) or local filesystem (for development). The system maintains a metadata record including the storage path, encryption nonce, and salt. This allows the system to retrieve and decrypt documents on-demand while ensuring even an attacker with storage access cannot read document contents without the user's credentials.

## 6.2 LLM-Based Claim Extraction

The extraction service handles multiple document formats intelligently. When a document is received, the system determines its file type (PDF, image, or text) and routes it to the appropriate extraction handler. PDFs are processed using PyMuPDF for text extraction. Images are passed through Tesseract OCR if they contain scanned content. Text files are decoded directly to UTF-8. The extracted text content is then truncated to fit within LLM context limits and passed to the language model for intelligent claim extraction. The LLM understands document semantics and extracts structured claims even from complex or poorly formatted documents.

## 6.3 Claim Validation and Normalization

Extracted claims are validated and normalized into standard formats. Age values must fall within reasonable bounds (0-150). Nationality values are checked against a list of valid countries. Dates are parsed from various formats (DD/MM/YYYY, MM/DD/YYYY, ISO 8601) and normalized to ISO 8601 format. Boolean values are normalized regardless of their source representation ("true", "yes", "1", etc.). This normalization ensures consistent data format for cryptographic proof generation, where exact data format is critical.

---

# 7. ZERO-KNOWLEDGE PROOF GENERATION

## 7.1 Circom Circuit Design

The credential.circom circuit implements the mathematical constraints for ZK proofs. The circuit accepts:  private inputs known only to the prover (age, nationality hash, document expiration, secret nonce) and public inputs representing commitments to claims. The circuit performs cryptographic verification proving that the prover knows valid claims satisfying specified conditions without revealing claim details. For example, the circuit can prove age >= 18 without revealing the actual age. The circuit uses Poseidon hash functions optimized for zero-knowledge applications, providing efficient hashing within the circuit constraints.

## 7.2 Witness Generation

Witness data transforms claims into circuit-compatible format. The system converts age values directly to integers, hashing string values like nationality to numeric representations. The document expiration date is converted to a Unix timestamp. The secret nonce is converted to a numeric value within the field modulus. All values are constrained to the BN128 elliptic curve field (2^254) to ensure they work within the zero-knowledge proof system. This transformation is deterministic, meaning the same claims always produce the same witness data.

## 7.3 Proof Generation with snarkjs

The ZK generator creates Groth16 proofs using snarkjs. The proof generation pipeline starts with circuit compilation which converts the Circom circuit into arithmetic constraints and generates the proving key. Witness generation transforms claims into circuit-compatible format. The snarkjs library generates the actual cryptographic proof demonstrating knowledge of valid claims. Before submission to the blockchain, the system verifies the proof locally using the verification key, catching any errors before incurring blockchain transaction costs. This local verification ensures proof validity while providing clear error messages if generation fails.

---

# 8. SMART CONTRACT INTEGRATION

## 8.1 Solidity CredentialVerifier Contract

The smart contract stores and verifies on-chain proofs. The contract maintains a mapping from user addresses to their proof data. When a user submits a proof, the contract verifies the proof structure using a verifier component, then stores the proof indexed by the sender's address. The contract provides functions for third parties to query whether an address possesses a valid proof. Event logging enables off-chain systems to monitor proof submissions and create audit trails. Access control prevents unauthorized proof submissions, ensuring only valid proofs are recorded.

## 8.2 On-Chain Verification Logic

The contract's verification logic checks proofs against the verifier contract. When a user submits a proof, the contract calls the verifier component to perform cryptographic validation. The verifier accepts the proof components (pi_a, pi_b, pi_c) and public inputs, performing complex elliptic curve arithmetic to confirm the proof is mathematically valid. If verification succeeds, the proof and metadata are stored permanently. The blockchain creates an immutable record of which addresses have proven possession of valid claims. Third parties can query the contract at any time to verify if an address has a valid proof.

---

# 9. ASYNCHRONOUS TASK PROCESSING

## 9.1 Celery Architecture

Celery enables distributed processing of document pipelines. The task queue decouples document upload from intensive processing, allowing the API to return immediately while processing continues asynchronously. The message broker (Redis) receives task enqueue requests and distributes them to worker processes. Multiple workers can process tasks in parallel, enabling horizontal scaling—adding more workers increases throughput. The result backend stores task completion status and results, enabling the frontend to poll for progress without direct worker connection.

## 9.2 Task Pipeline

The processing pipeline is modular and chainable. Document decryption forms the first task, retrieving the encrypted document and verifying it matches stored metadata. Claim extraction passes decrypted content to LLM services. Claim validation checks extracted values against schemas and rejects malformed data. Proof generation converts validated claims to witness format and invokes snarkjs. Result storage persists all intermediate and final outputs. Each task includes error handling that logs failures and updates job status. The pipeline is configured with task timeouts preventing hanging processes and retry logic handling transient failures.

---

# 10. SECURITY AND ENCRYPTION

## 10.1 End-to-End Encryption

Data protection is implemented at multiple layers:

1. **In Transit:** All API communications use HTTPS with TLS 1.3
2. **At Rest:** Documents are encrypted with AES-256-GCM before storage
3. **Application Level:** Sensitive fields are encrypted before database storage

```python
class SecurityService:
    @staticmethod
    def create_secure_session(user_id: str) -> str:
        """Create encrypted session token"""
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow(),
            "session_id": secrets.token_urlsafe(32)
        }
        
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        
        # Store session metadata in Redis
        redis_client.setex(
            f"session:{token}",
            86400,  # 24 hours
            json.dumps(payload)
        )
        
        return token
    
    @staticmethod
    def encrypt_sensitive_field(value: str, user_id: str) -> str:
        """Encrypt individual field for database storage"""
        # Derive key from user_id and master key
        combined = settings.MASTER_ENCRYPTION_KEY + user_id
        key = hashlib.sha256(combined.encode()).digest()
        
        cipher = AESGCM(key)
        nonce = os.urandom(12)
        ciphertext = cipher.encrypt(nonce, value.encode(), None)
        
        # Return encrypted value with nonce prefix
        return f"{nonce.hex()}:{ciphertext.hex()}"
    
    @staticmethod
    def decrypt_sensitive_field(encrypted_value: str, user_id: str) -> str:
        """Decrypt sensitive field from database"""
        nonce_hex, ciphertext_hex = encrypted_value.split(":")
        nonce = bytes.fromhex(nonce_hex)
        ciphertext = bytes.fromhex(ciphertext_hex)
        
        combined = settings.MASTER_ENCRYPTION_KEY + user_id
        key = hashlib.sha256(combined.encode()).digest()
        
        cipher = AESGCM(key)
        plaintext = cipher.decrypt(nonce, ciphertext, None)
        
        return plaintext.decode()
```

## 10.2 JWT Authentication

JWT tokens provide stateless authentication without requiring server-side session storage. Access tokens contain user identity and expiration information, signed with the server's secret key. Tokens are validated on each request by verifying the signature and checking expiration. Refresh tokens enable extended sessions, allowing users to obtain new access tokens without re-entering credentials. Token validation occurs in middleware before route handlers execute, ensuring early rejection of invalid requests.

## 10.3 Data Protection Measures

Multiple security measures protect user data:

1. **Input Validation:** All inputs validated before processing
2. **Rate Limiting:** Prevent brute force and DoS attacks
3. **CORS Configuration:** Restrict cross-origin requests
4. **SQL Injection Prevention:** Parameterized queries through SQLAlchemy ORM
5. **XSS Prevention:** Content-Security-Policy headers
6. **Secrets Management:** Environment variables for sensitive configuration

---

# 11. DEPLOYMENT AND DEVOPS

## 11.1 Docker Containerization

Services are containerized for consistent deployment across environments. The backend container includes Python, FastAPI, and all required libraries. The frontend container uses Node.js for building the React SPA and Nginx for serving optimized production builds. Containers define health checks enabling orchestration systems to monitor service status and restart unhealthy instances. Volume mounts enable local development while preserving containerization benefits during testing.

## 11.2 Docker Compose Configuration

Complete stack orchestration is managed through Docker Compose configuration. The configuration defines services for frontend, backend, Celery workers, PostgreSQL database, and Redis message broker. Environment variables configure database connections, API keys, and service parameters. Volumes enable data persistence for the database and documents. Networks isolate services while allowing inter-service communication. Health checks monitor service status, and dependency declarations ensure services start in the correct order.

---

# 12. TESTING AND VALIDATION

## 12.1 Circuit Testing

Circom circuits are tested to ensure constraint correctness:

```bash
#!/bin/bash
# scripts/test_circuit.sh

# Compile circuit
circom credential.circom --r1cs --wasm -o build

# Generate powers of tau
snarkjs powersoftau new bn128 12 build/pot12_0000.ptau -v

# Phase 1
snarkjs powersoftau contribute build/pot12_0000.ptau build/pot12_0001.ptau

# Phase 2
snarkjs powersoftau prepare phase2 build/pot12_0001.ptau build/pot12_final.ptau -v

# Generate zkey
snarkjs groth16 setup build/credential.r1cs build/pot12_final.ptau build/circuit_0000.zkey

# Contribute to phase 2
snarkjs zkey contribute build/circuit_0000.zkey build/circuit_final.zkey

# Export verification key
snarkjs zkey export verificationkey build/circuit_final.zkey build/verification_key.json

# Test with sample witness
cat > /tmp/test_input.json <<EOF
{
  "age": 25,
  "nationality_hash": 123456789,
  "document_expiration_timestamp": 1735689600,
  "secret_nonce": 987654321,
  "age_threshold": 18,
  "nationality_commitment": 123456789,
  "expiration_commitment": 1735689600
}
EOF

# Generate proof
snarkjs wtns generate build/credential.wasm /tmp/test_input.json /tmp/witness.wtns
snarkjs groth16 prove build/circuit_final.zkey /tmp/witness.wtns /tmp/proof.json /tmp/public.json

# Verify proof
snarkjs groth16 verify build/verification_key.json /tmp/public.json /tmp/proof.json

echo "Circuit tests completed"
```

## 12.2 API Testing

Comprehensive API tests using pytest:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_document_upload(client):
    """Test document upload endpoint"""
    
    # Create test document
    test_content = b"Test document content"
    files = {"document": ("test.pdf", test_content)}
    
    # Upload document
    response = await client.post(
        "/api/v1/documents/upload",
        files=files,
        headers={"Authorization": "Bearer test_token"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "doc_id" in data
    assert "job_id" in data

@pytest.mark.asyncio
async def test_job_status(client):
    """Test job status polling"""
    
    job_id = "test_job_123"
    
    response = await client.get(
        f"/api/v1/jobs/{job_id}/status",
        headers={"Authorization": "Bearer test_token"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["queued", "processing", "done", "failed"]

@pytest.mark.asyncio
async def test_unauthorized_access(client):
    """Test unauthorized access rejection"""
    
    response = await client.get(
        "/api/v1/jobs/test_job_123"
    )
    
    assert response.status_code == 401
```

## 12.3 End-to-End Smoke Testing

The end-to-end smoke test validates the complete pipeline:

```python
#!/usr/bin/env python3
# scripts/e2e_smoke.py

import asyncio
import argparse
import requests
import json
from pathlib import Path

async def run_smoke_test(
    doc_path: str,
    expected_claims: dict,
    api_url: str = "http://localhost:8000"
):
    """Run complete end-to-end workflow"""
    
    print(f"Starting E2E smoke test with {doc_path}")
    
    # 1. Upload document
    print("1. Uploading document...")
    with open(doc_path, 'rb') as f:
        response = requests.post(
            f"{api_url}/api/v1/documents/upload",
            files={"document": f},
            headers={"Authorization": "Bearer test_token"}
        )
    
    assert response.status_code == 200
    result = response.json()
    doc_id = result['doc_id']
    job_id = result['job_id']
    print(f"   ✓ Document uploaded: {doc_id}")
    
    # 2. Poll job status
    print("2. Polling job status...")
    import time
    max_attempts = 60
    for attempt in range(max_attempts):
        response = requests.get(
            f"{api_url}/api/v1/jobs/{job_id}/status",
            headers={"Authorization": "Bearer test_token"}
        )
        
        data = response.json()
        status = data['status']
        
        if status == "done":
            print(f"   ✓ Processing complete")
            break
        elif status == "failed":
            print(f"   ✗ Processing failed: {data.get('error')}")
            return False
        else:
            time.sleep(2)
            print(f"   → Status: {status} ({attempt+1}/{max_attempts})")
    else:
        print("   ✗ Timeout waiting for processing")
        return False
    
    # 3. Retrieve proof
    print("3. Retrieving generated proof...")
    response = requests.get(
        f"{api_url}/api/v1/proofs/{job_id}",
        headers={"Authorization": "Bearer test_token"}
    )
    
    assert response.status_code == 200
    proof_data = response.json()
    print(f"   ✓ Proof retrieved")
    
    # 4. Verify expected claims
    print("4. Validating extracted claims...")
    extracted_claims = proof_data.get('claims', {})
    
    for expected_key, expected_value in expected_claims.items():
        actual_value = extracted_claims.get(expected_key)
        if actual_value == expected_value:
            print(f"   ✓ Claim {expected_key}: {actual_value}")
        else:
            print(f"   ✗ Claim mismatch {expected_key}: expected {expected_value}, got {actual_value}")
            return False
    
    print("\n✓ All smoke tests passed!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", required=True, help="Path to test document")
    parser.add_argument("--expected-claims", required=True, help="JSON string of expected claims")
    parser.add_argument("--api-url", default="http://localhost:8000")
    
    args = parser.parse_args()
    
    expected_claims = json.loads(args.expected_claims)
    
    success = asyncio.run(run_smoke_test(
        args.doc,
        expected_claims,
        args.api_url
    ))
    
    exit(0 if success else 1)
```

---

# 13. FUTURE ENHANCEMENTS

## 13.1 Scalability Improvements

1. **Kubernetes Deployment:** Containerized services orchestrated via Kubernetes for auto-scaling
2. **Database Sharding:** Partition user data across multiple PostgreSQL instances
3. **Caching Layer:** Redis cluster for distributed caching
4. **CDN Integration:** CloudFlare or similar for static content distribution
5. **Message Queue Optimization:** Apache Kafka replacing Redis for higher throughput

## 13.2 Additional Document Types

1. **Medical Records:** Support for medical documents with HIPAA-compliant processing
2. **Financial Documents:** Tax returns, bank statements, investment portfolios
3. **Educational Records:** Transcripts, diplomas, certificates with grade verification
4. **Professional Credentials:** Licenses, certifications with expiry tracking

## 13.3 Advanced Features

1. **Multi-Signature Proofs:** Enable group verification of claims
2. **Incremental Proofs:** Update claims without re-generating complete proofs
3. **Selective Disclosure:** Users choose which specific claims to prove
4. **Claim Delegation:** Enable users to authorize third parties to submit proofs
5. **Cross-Chain Verification:** Support multiple blockchain networks (Polygon, Arbitrum, etc.)

---

# 14. CHALLENGES AND SOLUTIONS

## 14.1 Technical Challenges

**Challenge 1: LLM Variability**
- **Problem:** Different LLMs extract claims differently; inconsistent formatting and missing data
- **Solution:** Implemented multi-model fallback chain (GPT-4o → LLaMA → heuristic) with claim normalization service ensuring consistency

**Challenge 2: Proof Generation Performance**
- **Problem:** Circom circuit compilation and proof generation is time-intensive
- **Solution:** Implemented async processing with Celery; added local proof verification caching; optimized circuit constraints

**Challenge 3: Storage and Encryption Overhead**
- **Problem:** Encrypted document storage increases database size significantly
- **Solution:** Implemented external storage (S3) for documents while maintaining encryption; used compression before storage

**Challenge 4: Blockchain Gas Costs**
- **Problem:** On-chain proof verification is expensive in gas fees
- **Solution:** Batch proof submissions; explored layer 2 solutions (Polygon, Arbitrum) for reduced costs

---

# 15. CONCLUSION

The ZK Credential Verification System represents a significant advance in privacy-preserving identity verification. By combining Large Language Model-driven document processing with zero-knowledge cryptography and blockchain technology, the system enables users to prove claims from identity documents without exposing sensitive information to verifiers.

The architecture successfully addresses the fundamental challenge of digital identity: how to enable trustless verification of claims while respecting user privacy. The integration of modern technologies—React for responsive interfaces, FastAPI for high-performance APIs, Celery for scalable processing, and Circom/snarkjs for cryptographic proofs—creates a robust, production-ready system.

Key achievements include:
- **Document-Agnostic Processing:** Support for PDFs, images, and scanned documents through intelligent LLM extraction
- **Privacy-First Design:** End-to-end encryption with zero-knowledge proofs preventing verifier access to raw documents
- **Scalable Architecture:** Asynchronous processing enabling handling of high document volumes
- **On-Chain Permanence:** Smart contracts creating immutable records of verified claims
- **User-Friendly Interface:** Streamlined React-based UI abstracting cryptographic complexity

The system is positioned for deployment in financial services, border control, education verification, and employment screening applications where privacy-preserving verification is critical.

---

# 16. REFERENCES

1. Ben-Sasson, E., Chiesa, A., Genkin, D., Hamilis, E., Kopelowitz, E., Mesch, R., ... & Tromer, E. (2014). "SNARKs for C: Verifying Program Executions Succinctly and in Zero Knowledge." Advances in Cryptology–CRYPTO 2013, 90-110.

2. Bünz, B., Bootle, J., Boneh, D., Poelstra, A., Wuille, P., & Maxwell, G. (2018). "Bulletproofs: Short Proofs for Confidential Transactions and More." 2018 IEEE Symposium on Security and Privacy (SP), 315-334.

3. Zcash Protocol Specification. (2022). "The Zcash Protocol." Available at: https://github.com/zcash/zips

4. snarkjs Documentation. "SNARKs in JavaScript." Available at: https://github.com/iden3/snarkjs

5. Circom Documentation. "Circom Language Constructor." Available at: https://docs.circom.io

6. FastAPI Official Documentation. Available at: https://fastapi.tiangolo.com

7. OWASP. "OWASP Top 10 Web Application Security Risks." 2021 Edition. Available at: https://owasp.org/www-project-top-ten/

8. Dwork, C. (2006). "Differential Privacy." Automata, Languages and Programming, 1-12.

9. Ethereu Foundation. "Solidity Documentation." Available at: https://docs.soliditylang.org

10. Vitalik Buterin. "ZK-SNARKs: A Primer." Ethereum Foundation Blog, 2016. Available at: https://blog.ethereum.org/

---

**END OF DOCUMENTATION**

*This comprehensive project report documents the architecture, implementation, and deployment of the ZK Credential Verification System—a state-of-the-art application demonstrating practical implementation of zero-knowledge cryptography for privacy-preserving identity verification.*

---

*Document Generated: April 10, 2026*
*Total Pages: 48*
