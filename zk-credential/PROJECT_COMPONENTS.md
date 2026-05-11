# ZK CREDENTIAL VERIFICATION SYSTEM - COMPONENTS LIST

## Project Overview
A comprehensive system combining Large Language Models, Zero-Knowledge Cryptography, and Blockchain technology for privacy-preserving identity verification.

---

## 🖥️ FRONTEND COMPONENTS (Client Layer)

### Core Framework
- **React 18** - Modern React library with concurrent features and automatic batching
- **TypeScript** - Static type checking for JavaScript applications
- **Vite** - Next-generation build tool with instant HMR and optimized production builds
- **Tailwind CSS** - Utility-first CSS framework for responsive design

### Component Architecture
- **Page Components**
  - Upload.tsx - Document upload interface with status tracking
  - Dashboard.tsx - Central hub showing job history and proof status
  - Verify.tsx - Third-party verification interface
  
- **Functional Components**
  - UploadZone.tsx - Drag-and-drop file upload with format validation
  - ProofCard.tsx - Displays generated proofs and extracted claims
  - WalletButton.tsx - Wallet connection and account management

### State Management
- **Zustand** - Lightweight state management library
  - walletStore - Manages blockchain wallet connections and network state
  - jobStore - Tracks asynchronous job status and progress

### Hooks & Utilities
- **useProofStatus** - Custom hook for polling job completion
- **useWeb3** - Web3 integration for wallet interaction
- **useAPI** - API communication layer

### Blockchain Integration
- **Web3.js** / **ethers.js** - JavaScript libraries for Ethereum interaction
- **MetaMask** - Browser wallet extension for transaction signing

### UI Libraries
- **React Router** - Client-side routing
- **Axios** - HTTP client for API requests
- **React Toastify** - User notifications and alerts

---

## 🔌 BACKEND COMPONENTS (Server Layer)

### Core Framework
- **FastAPI** - Modern Python web framework with async support
- **Uvicorn** - ASGI web server for production deployment
- **Pydantic** - Data validation using Python type hints
- **Pydantic Settings** - Environment configuration management

### API Routes & Endpoints
- **Auth Routes** - User authentication and token management
- **Document Routes** - Document upload and retrieval endpoints
- **Job Routes** - Asynchronous job status tracking
- **Proof Routes** - Proof submission and verification endpoints
- **Middleware Stack** - CORS, logging, error handling

### Authentication & Security
- **Python-Jose** - JWT token encoding/decoding
- **Passlib & BCrypt** - Secure password hashing
- **PBKDF2** - Key derivation function
- **AES-256-GCM** - Symmetric encryption for documents

### Database & ORM
- **PostgreSQL** - Primary relational database
- **SQLAlchemy** - Python ORM for database operations
- **asyncpg** - Asynchronous PostgreSQL adapter
- **Alembic** - Database migration tool

### Database Models
- **User** - User account information
- **Document** - Uploaded documents metadata
- **Job** - Asynchronous processing job tracking
- **Claim** - Extracted claims with validation status
- **Proof** - Generated cryptographic proofs

---

## ⚙️ SERVICE LAYER COMPONENTS

### Document Processing
- **DocumentProcessorService** - Determines document format and extracts text
- **PyMuPDF (fitz)** - PDF text extraction
- **python-docx** - Word document parsing
- **python-pptx** - PowerPoint presentation parsing

### LLM Integration
- **LLMParserService** - Orchestrates claim extraction using LLMs
- **OpenAI API** - GPT-4o model for advanced claim extraction
- **Groq API** - LLaMA models for cost-efficient extraction
- **Fallback Extraction** - Heuristic-based extraction when LLMs unavailable
- **Pytesseract** - OCR for scanned documents and images

### Claim Processing
- **ClaimValidatorService** - Validates extracted claims against schemas
- **ClaimNormalizationService** - Normalizes claims into standard formats
- **Date Parser** - Converts various date formats to ISO 8601
- **Boolean Normalizer** - Standardizes boolean representations

### Zero-Knowledge Proof
- **ZKGeneratorService** - Orchestrates proof generation pipeline
- **WitnessGeneratorService** - Converts claims to circuit-compatible witness data
- **LocalProofVerifier** - Verifies proofs before blockchain submission

### Storage Management
- **DocumentStorageService** - Handles encrypted document storage
- **EncryptionService** - AES-256-GCM encryption and decryption
- **AWS S3 Integration** - Cloud storage for documents
- **LocalFilesystem** - Fallback local storage option

### Security Services
- **JWTService** - JWT token creation and verification
- **SecurityService** - Secure session management
- **PasswordHashService** - Password hashing and verification

---

## 📋 ASYNCHRONOUS TASK PROCESSING

### Task Queue System
- **Celery** - Distributed task queue framework
- **Redis** - Message broker and result backend
- **Task Pipeline** - Chain of document processing tasks

### Task Types
- **process_document_task** - Main orchestration task
- **decrypt_document_task** - Document decryption
- **extract_claims_task** - LLM-based claim extraction
- **validate_claims_task** - Claim validation and normalization
- **generate_proof_task** - ZK proof generation
- **store_metadata_task** - Results persistence

### Task Monitoring
- **Job Status Tracking** - Real-time job progress
- **Error Handling & Retries** - Automatic failure recovery
- **Task Logging** - Comprehensive task execution logs

---

## 🔬 CRYPTOGRAPHY & ZK COMPONENTS

### Circuit Design
- **Circom** - Circuit compiler for zero-knowledge proofs
- **credential.circom** - Main ZK circuit (~1,200 R1CS constraints)
- **Poseidon Hash** - Efficient hashing for ZK circuits

### Proof Generation
- **snarkjs** - JavaScript library for zk-SNARK operations
- **Groth16** - Zero-knowledge proof system
- **Trusted Setup Ceremony** - Circuit parameter generation
- **Witness Generation** - Converting claims to circuit inputs

### Cryptographic Primitives
- **Pedersen Commitments** - Cryptographic commitment schemes
- **Merkle Trees** - Hash tree structures for verification
- **BN128 Curve** - Elliptic curve for arithmetic

---

## ⛓️ BLOCKCHAIN & SMART CONTRACT COMPONENTS

### Development Environment
- **Hardhat** - Ethereum development framework
- **Solidity** - Smart contract programming language
- **ethers.js** - Contract interaction library

### Smart Contracts
- **CredentialVerifier.sol** - Main verification contract
- **ProofData Struct** - Off-chain proof data representation
- **IVerifier Interface** - Verifier contract abstraction

### Contract Functions
- **submitProof()** - Submit user proofs to blockchain
- **verifyProof()** - Verify proof validity
- **hasProof()** - Check if address has valid proof
- **getProof()** - Retrieve proof details
- **verifyClaimBitmap()** - Verify claim bitmap against proof

### Blockchain Networks
- **Sepolia Testnet** - Development and testing network
- **Ethereum Mainnet** - Production deployment target
- **Network Configuration** - RPC endpoints and contract addresses

---

## 💾 DATA & STORAGE COMPONENTS

### Persistent Storage
- **PostgreSQL** - Relational database for structured data
- **AWS S3** - Object storage for encrypted documents
- **Local Filesystem** - Development storage fallback

### Data Models
- User profiles and authentication
- Document metadata and encryption keys
- Extracted claims and validation results
- Generated proofs and blockchain details

### Data Encryption
- **AES-256-GCM** - Symmetric encryption at rest
- **PBKDF2** - Key derivation from user credentials
- **Nonce & Salt** - Per-document encryption parameters

---

## 🐳 DEPLOYMENT & DEVOPS COMPONENTS

### Containerization
- **Docker** - Container runtime and image management
- **Docker Compose** - Multi-container orchestration
- **Backend Container** - FastAPI application
- **Frontend Container** - Nginx + React build

### Container Services
- **Nginx** - Reverse proxy and static file serving
- **PostgreSQL Container** - Database service
- **Redis Container** - Message broker service
- **Celery Worker Container** - Task processing

### Configuration Management
- **.env Files** - Environment variables
- **docker-compose.yml** - Service configuration
- **vite.config.ts** - Frontend build configuration
- **tsconfig.json** - TypeScript configuration

### Development Tools
- **Hot Module Replacement (HMR)** - Live code reloading
- **Debug Logging** - Comprehensive application logging
- **Health Checks** - Service status monitoring

---

## 🔐 SECURITY COMPONENTS

### Authentication
- **JWT Tokens** - Stateless session management
- **Access Tokens** - 24-hour expiration
- **Refresh Tokens** - 7-day extended validity
- **Token Validation** - Request authorization

### Encryption Mechanisms
- **End-to-End Encryption** - HTTPS transport
- **At-Rest Encryption** - AES-256-GCM
- **In-Transit Encryption** - TLS 1.3
- **Key Derivation** - PBKDF2 with iterations

### Security Measures
- **SQL Injection Prevention** - Parameterized queries
- **Cross-Site Scripting (XSS)** - Content-Security-Policy headers
- **CORS Configuration** - Controlled origin access
- **Rate Limiting** - Request throttling
- **Input Validation** - Pydantic schema validation

### Secrets Management
- **Environment Variables** - Sensitive configuration
- **Secrets Isolation** - .env files in gitignore
- **API Key Protection** - Secure external service credentials

---

## 📚 EXTERNAL SERVICES & INTEGRATIONS

### Language Models
- **OpenAI GPT-4o** - State-of-the-art LLM for extraction
- **Groq LLaMA** - Cost-efficient alternative
- **Model Fallback** - Automatic provider switching

### Cloud Services
- **AWS S3** - Document storage service
- **Ethereum Nodes** - Blockchain RPC endpoints
- **OpenAI API** - LLM inference service

### OCR & Image Processing
- **Tesseract OCR** - Text recognition from images
- **Pillow (PIL)** - Image manipulation library
- **PyMuPDF** - PDF rendering and text extraction

---

## 📊 TESTING & VALIDATION COMPONENTS

### Circuit Testing
- **Circom Compiler** - Circuit syntax validation
- **snarkjs Testing** - Proof generation verification
- **Local Verification** - Off-chain proof checking

### API Testing
- **pytest** - Python testing framework
- **httpx** - Async HTTP client for testing
- **Test Fixtures** - Database and mock setup

### End-to-End Testing
- **E2E Smoke Tests** - Complete workflow validation
- **Document Upload Testing** - File handling verification
- **Proof Generation Testing** - ZK proof validation
- **Blockchain Testing** - Contract interaction verification

---

## 📈 MONITORING & LOGGING

### Application Logging
- **Python logging** - Structured log output
- **Request Logging** - API call tracking
- **Error Logging** - Exception and failure tracking

### Database Monitoring
- **Query Logging** - SQL execution tracking
- **Connection Pooling Monitoring** - Database performance

### Task Monitoring
- **Celery Monitoring** - Task execution tracking
- **Job Status Updates** - Progress reporting
- **Error Notification** - Failure alerts

---

## 🎯 FEATURE COMPONENTS BY LAYER

### User Experience Layer
- File upload with drag-and-drop
- Real-time job status polling
- Wallet connection interface
- Proof visualization
- Claim display and verification

### Processing Layer
- Asynchronous document processing
- Multi-format document support
- Intelligent claim extraction
- Claim validation and normalization

### Cryptography Layer
- ZK circuit compilation
- Witness generation
- Groth16 proof generation
- Local proof verification

### Blockchain Layer
- Smart contract deployment
- Proof submission
- On-chain verification
- Event emission and logging

### Infrastructure Layer
- Docker containerization
- Multi-service orchestration
- Database persistence
- Encrypted storage
- Message queue processing

---

## 📦 TOTAL COMPONENT COUNT

| Category | Count |
|----------|-------|
| Frontend Libraries | 12+ |
| Backend Services | 15+ |
| Blockchain Components | 8+ |
| Cryptography Components | 7+ |
| Storage Components | 4+ |
| DevOps Components | 6+ |
| Security Components | 10+ |
| **Total Components** | **~65+** |

---

## 🔄 Data Flow Through Components

1. **User** → Browser → React Components
2. **React Components** → Zustand Store → API Layer
3. **API Layer** → FastAPI Routes → Service Layer
4. **Service Layer** → Document → LLM Parser
5. **LLM Parser** → OpenAI/Groq → Extracted Claims
6. **Claims** → Validator → Normalized Claims
7. **Claims** → Witness Generator → Circuit Format
8. **Circuit** → ZK Generator → Groth16 Proof
9. **Proof** → Celery Task → Result Storage
10. **Proof** → Web3.js → Smart Contract
11. **Smart Contract** → Blockchain → Permanent Record

---

## 🚀 Component Integration Points

- **Frontend ↔ Backend**: REST API over HTTPS with JWT auth
- **Backend ↔ Database**: SQLAlchemy ORM with connection pooling
- **Backend ↔ Task Queue**: Celery task dispatch to Redis
- **ZK ↔ Blockchain**: snarkjs proof to contract interaction
- **LLM ↔ Backend**: API calls with fallback mechanisms
- **Storage ↔ Backend**: Encrypted document management
- **Frontend ↔ Wallet**: ethers.js blockchain interaction

---

**Last Updated:** April 10, 2026  
**Total Project Complexity:** Enterprise-Grade System  
**Technology Stack Diversity:** 65+ Components
