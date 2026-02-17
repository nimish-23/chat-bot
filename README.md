# Chatbot API with Ollama

A Flask-based chatbot API that integrates with Ollama (local AI) using clean, production-ready architecture with service layer pattern and dependency injection.

## 🏗️ Architecture Overview

This project implements a **3-tier loosely coupled architecture**:

```
┌─────────────────────────────────────────┐
│  HTTP Layer (Routes)                    │
│  - Handles HTTP requests/responses      │
│  - Input validation at HTTP level       │
│  - Error code handling (200, 400, 500)  │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Business Logic Layer (Service)         │
│  - Message validation                   │
│  - Business rules                       │
│  - Orchestrates LLM calls               │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Integration Layer (LLM Client)         │
│  - Communicates with Ollama API         │
│  - Formats requests/responses           │
│  - Handles API-specific logic           │
└─────────────────────────────────────────┘
```

## 📁 Project Structure

```
chat-bot/
├── app/
│   ├── __init__.py              # Application factory with dependency injection
│   ├── api/
│   │   └── chat_routes.py       # HTTP routes (thin layer)
│   ├── services/
│   │   └── chat_service.py      # Business logic and validation
│   ├── llm/
│   │   ├── base.py              # Abstract base class for LLM providers
│   │   └── ollama_client.py     # Ollama implementation
│   ├── core/
│   │   ├── __init__.py
│   │   └── logger.py            # Centralized logging configuration
│   ├── static/
│   │   ├── style.css            # Frontend styles
│   │   └── script.js            # Frontend JavaScript
│   └── templates/
│       └── index.html           # Chat interface
├── frontend/                    # Additional frontend resources (if any)
├── logs/
│   └── chatbot.log              # Application logs (auto-generated)
├── LICENSE                      # License file
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── dockerfile                   # Docker configuration
└── run.py                       # Application entry point
```

## ✨ Key Features Implemented

### 1. **Service Layer Pattern**

- Clear separation between HTTP handling and business logic
- Routes handle ONLY HTTP concerns
- Business logic isolated in service layer
- Easy to test each layer independently

### 2. **Dependency Injection**

- Services injected into routes via `init_routes()`
- LLM clients injected into services
- No hard-coded dependencies
- Easy to swap implementations (Ollama → OpenAI)

### 3. **Loose Coupling**

- Each layer depends on interfaces, not implementations
- Routes don't know which service implementation
- Services don't know which LLM implementation
- Easy to extend and modify

### 4. **Input Validation**

- Message structure validation
- Empty message checking
- Required field validation
- Type checking

### 5. **Error Handling**

- Proper HTTP status codes (200, 400, 500)
- Descriptive error messages
- Validation errors vs server errors
- Graceful failure handling

### 6. **Extensible Design**

- Abstract `BaseLLM` class allows multiple AI providers
- Easy to add OpenAI, Claude, or other LLMs
- Configuration-driven approach

### 7. **Centralized Logging System**

- Production-ready logging with file rotation
- Dual output: console + file (`logs/chatbot.log`)
- Performance monitoring with latency tracking
- Error tracking with full stack traces
- Automatic log rotation (5MB per file, 3 backups)

**Log Levels:**

- `INFO`: Request latency, performance metrics
- `ERROR`: Validation failures, exceptions
- `DEBUG`: Detailed diagnostic information (available if needed)

**Sample Logs:**

```
2026-02-17 20:01:36,937 | INFO | Model: llama3.2 | Latency: 18.193s | Requests: 1
2026-02-17 20:02:13,995 | INFO | Model: llama3.2 | Latency: 15.869s | Requests: 1
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Flask and requests libraries

### Installation

1. Clone the repository

```bash
git clone <your-repo-url>
cd chat-bot
```

2. Install dependencies

```bash
pip install flask requests
```

3. Start Ollama server (if not running)

```bash
ollama serve
```

4. Run the application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 📡 API Usage

### Send a Chat Message

**Endpoint:** `POST /chat`

**Request:**

```json
{
  "messages": [{ "role": "user", "content": "Hello, how are you?" }],
  "temperature": 0.7
}
```

**Response (Success - 200):**

```json
{
  "content": "I'm doing well, thank you! How can I help you today?",
  "model": "llama3.2",
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 12,
    "total_tokens": 27
  }
}
```

**Response (Validation Error - 400):**

```json
{
  "error": "Messages cannot be empty"
}
```

**Response (Server Error - 500):**

```json
{
  "error": "Internal server error",
  "details": "Connection to Ollama failed"
}
```

## 💡 Learning Journey - Questions & Solutions

During development, several important concepts were explored:

### Q1: What does `BaseLLM` do?

**Answer:** `BaseLLM` is a blueprint/template (abstract base class) that defines the interface all LLM providers must follow. It ensures consistency across different AI providers (Ollama, OpenAI, etc.) so they can be swapped without changing the rest of the code.

### Q2: How does the `OllamaLLM.generate()` method work?

**Answer:** It sends an HTTP POST request to the Ollama API with the conversation messages, waits for the AI response (with 60-second timeout), and returns a formatted response with content, model name, and token usage.

### Q3: Who controls the response JSON format?

**Answer:** There are TWO different JSON structures:

- **Ollama's response** (controlled by Ollama API) - we can't change this
- **Our return format** (controlled by us) - we extract what we need from Ollama's response and create our own clean, standardized format

This allows us to provide a consistent API regardless of which LLM provider we use.

### Q4: Why separate `ChatService` and `chat_routes`?

**Answer:** Separation of concerns following the service layer pattern:

- **Routes** = HTTP handling only (extract request, return response)
- **Service** = Business logic only (validation, orchestration)
- **Benefits**: Testability without Flask, reusability in CLI/tests/other frameworks, maintainability with clear responsibilities

### Q5: How does `app/__init__.py` work?

**Answer:** It's an **application factory** that:

1. Creates the Flask app
2. Creates dependencies (LLM → Service)
3. Injects dependencies into routes
4. Registers routes with Flask
5. Returns the configured app

This pattern enables testing, multiple configurations, and centralized dependency management.

### Q6: Why use `init_routes(service)` instead of creating service in routes?

**Answer:** **Dependency injection** for flexibility:

- ✅ Easy to swap services for testing (inject mock services)
- ✅ Easy to change LLM providers (just change what's injected)
- ✅ Routes don't control their own dependencies
- ✅ Central configuration in one place (`create_app`)

### Q7: What is "loose coupling" in this architecture?

**Answer:** Each layer knows about interfaces but not implementations:

- Routes know `service.chat()` exists, but not which service
- Service knows `llm.generate()` exists, but not which LLM
- Any component can be swapped without breaking others

This makes the code flexible, testable, and maintainable.

## 🎯 Design Patterns Used

1. **Service Layer Pattern** - Separates business logic from HTTP handling
2. **Dependency Injection** - Components receive dependencies from outside
3. **Abstract Base Class** - Defines interface for LLM providers
4. **Application Factory** - Creates configured Flask app instances
5. **Blueprint Pattern** - Organizes Flask routes into modules

## 🔧 Future Enhancements

- [ ] Conversation history persistence (database integration)
- [ ] Multiple LLM provider support (OpenAI, Claude, etc.)
- [ ] Rate limiting
- [x] Request/response logging ✅
- [x] Streaming responses ✅
- [ ] User authentication
- [ ] Conversation memory management
- [ ] Metrics dashboard for log analytics

## 📚 What I Learned

1. **Architecture matters** - Clean separation of concerns makes code maintainable
2. **Dependency injection enables flexibility** - Easy to test and swap implementations
3. **Loose coupling is powerful** - Components can evolve independently
4. **Service layer pattern improves testability** - Business logic can be tested without HTTP
5. **HTTP layer should be thin** - Routes should only handle HTTP, not business logic

## 🤝 Contributing

Feel free to fork this project and experiment with:

- Adding new LLM providers (OpenAI, Claude)
- Implementing conversation history
- Adding streaming support
- Improving error handling

## 📄 License

[Your License Here]

---

**Built with:**

- Flask - Web framework
- Ollama - Local AI inference
- Python 3 - Programming language
