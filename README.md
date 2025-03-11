# Arina AI

**Arina AI – Your Intelligent Companion for Business, POM-QM Analysis, and Agricultural Insights.**

Arina AI is an intelligent and adaptable AI designed to assist in business feasibility analysis, operations research (POM-QM), agricultural insights, and natural conversations. With a strong focus on practical applications, Arina provides data-driven recommendations, market analysis, and decision-making support. Built as a local-first AI, it operates efficiently on personal devices while offering advanced memory, contextual awareness, and analytical capabilities.

## Branding Philosophy

**Arina** comes from the Arabic word **"أَرِنَا"**, meaning **"show us"** or **"guide us."** The name reflects Arina AI's core philosophy—helping users navigate decisions, gain knowledge, and optimize strategies. Arina is more than just an AI; she is a companion, an advisor, and a source of innovation.

## Features

- **Conversational Memory** – Remembers user preferences and past interactions.
- **Markdown Support** – Chat responses are formatted with rich text.
- **Dark Mode** – Toggle between light and dark themes for better readability.
- **Smooth Animations** – UI is enhanced with smooth transitions and effects.
- **Business Feasibility Analysis (Planned)** – Provides financial insights, risk assessments, and market studies.
- **POM-QM Decision Support (Planned)** – Implements quantitative methods and operations research tools for business and industrial decision-making.
- **Agricultural Intelligence (Planned)** – Analyzes geographic and climate data for crop recommendations.
- **Voice Input & Output (Planned)** – Speak and listen to Arina for a hands-free experience.
- **Web-Based Interface** – Clean, simple, and responsive design.
- **Local-First AI** – Runs on your device without requiring cloud processing.

## Development Roadmap

Arina AI follows a structured development roadmap. Each phase enhances its capabilities and expands its scope:

- **Phase 0 (Current):** Core AI functionality with memory, search integration, and language adaptation.
- **Phase 1:** Enhancing AI contextual awareness and response quality.
- **Phase 2:** Business feasibility analysis with financial insights and report exports.
- **Phase 3:** POM-QM decision support with operations research features.
- **Phase 4:** Agricultural intelligence for crop suitability and sustainability analysis.
- **Phase 5:** UI/UX refinements and frontend improvements.
- **Phase 6:** Making the server online for global access.
- **Exploratory Phase:** Blockchain integration & utility token implementation.
- **Continuous Development:** Ongoing improvements, better memory, and expanding AI-driven tools.

## Target Users

Arina AI is designed for:
- **Students & University Students** – Learning AI, business analysis, and agricultural insights.
- **Business Analysts, PPIC, & Industry Professionals** – Supporting decision-making in business, operations, and supply chain management.

## Installation

### Prerequisites

- **Python 3.9+**
- **Git**
- **Virtual Environment** (`venv`)
- **[Ollama](https://github.com/ollama/ollama)** (for AI models)

### Setup Instructions

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/adsurkasur/ArinaAI.git
   cd ArinaAI
   ```

2. **Create and Activate Virtual Environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate      # For Windows
   ```

3. **Install Dependencies:**

   ```sh
   pip install -r config/requirements.txt
   ```

   **Note:** Some dependencies may not be directly downloadable from PyPI. They might require specific installation links from the project's GitHub or modifications for hardware compatibility.

4. **Install an AI Model Using Ollama:**  
   Arina requires a compatible AI model. Use Ollama to install a suitable model:

   ```sh
   ollama pull gemma2
   ```

5. **Run Arina AI:**

   ```sh
   python main.py
   ```

## Running the Web UI

To access the Arina Web UI:

1. **Start the Backend:** Run the `main.py` script in the backend directory.

   ```sh
   python backend/main.py
   ```

2. **Open the Web UI:**

   - Navigate to the `arina-ui/public/index.html` file.
   - Open it in a browser manually or use a local web server.

   Example using Python's built-in server:

   ```sh
   cd arina-ui/public
   python -m http.server 8000
   ```

   Then open `http://localhost:8000` in your browser.

   **Note:** A major UI revamp is in progress using Figma to enhance design and interactivity.

## Usage

- **Start Chatting:** Once Arina is running, you can interact via the web interface or terminal.
- **Give Feedback:** Arina improves over time based on your interactions and feedback.
- **Customize Models:** You can experiment with different AI models using Ollama.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make changes and commit (`git commit -m "Added new feature"`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a Pull Request for review.

## License

This project is licensed under the Apache-2.0 License – see the LICENSE file for details.

## Developer Notes

Arina AI is an evolving project! Contributions, feedback, and feature suggestions are always welcome. 😃🚀
