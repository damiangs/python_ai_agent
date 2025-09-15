<div align="center">
  <h1>🤖 python_ai_agent</h1>
  <p><em>Modular, extensible Python agent framework for function-calling, file operations, and more.</em></p>
</div>

---

## 🚀 Overview

**python_ai_agent** is a flexible Python framework for building AI-powered agents that can call functions, manipulate files, and interact with your codebase. Designed for extensibility and clarity, it supports advanced workflows such as code analysis, file editing, and dynamic function invocation.

---

## ✨ Features

- Modular function-calling system (e.g., `get_files_info`, `get_file_content`, `write_file`, `run_python_file`)
- Safe file operations within a working directory
- Error handling and informative responses
- Easily extensible with new tools and functions
- Example calculator app included

---

## 📂 Project Structure

```
python_ai_agent/
│
├── main.py               # Entry point for the agent
├── call_function.py      # Function call dispatcher
├── config.py             # Configuration and setup
├── prompts.py            # Prompt templates and system instructions
├── functions/            # Modular function implementations
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/           # Example calculator app
│   ├── main.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
├── tests.py              # Project tests
├── pyproject.toml        # Project metadata
└── uv.lock               # Dependency lock file
```

---

## 🛠️ Usage

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key:**

   - Export your Gemini API key as an environment variable:
     ```bash
     export GEMINI_API_KEY=your_api_key_here
     ```

3. **Run the agent:**

   ```bash
   python main.py
   ```

4. **Run the calculator example:**
   ```bash
   python calculator/main.py
   ```

---

## 🧩 Extending the Agent

- Add new functions to the `functions/` directory.
- Register them in `main.py` and `call_function.py`.
- Update prompts and schemas as needed.

---

## 🧪 Testing

Run all tests:

```bash
python tests.py
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
  <sub>Made with ❤️ by damiangs</sub>
</div>
