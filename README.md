# Arina AI

**Arina AI – Your Intelligent Companion for Business, POM-QM Analysis, and Agricultural Insights.**

Arina AI is your smart, local-first assistant, designed to help in business, operations, and agricultural decision-making. With a strong focus on practical applications, Arina provides data-driven recommendations, market analysis, and decision-making support. Built as a local-first AI, it operates efficiently on personal devices while offering advanced memory, contextual awareness, and analytical capabilities.

## Branding Philosophy

**Arina AI** takes its name from the Arabic word 'أَرِنَا' (Arinā), which means 'show us' or 'guide us.' This reflects Arina's mission: not just providing answers, but guiding users through complex decisions in business, POM-QM analysis, and agriculture. Arina isn't just an assistant—she’s a companion in your decision-making journey.

## Features

### Available Features
- **Conversational Memory** – Supports user preferences and past interactions.  
- **Markdown Support** – Includes rich text formatting in chat responses.  
- **Dark Mode** – Includes a toggle between light and dark themes for better readability.   
- **Web-Based Interface** – Includes a clean, responsive, and intuitive web interface.  

### Upcoming Features
- **Business Analysis** – Will provide financial insights, risk assessments, and market studies.  
- **POM-QM Decision Support** – Will implement quantitative methods and operations research tools for business and industrial decision-making.  
- **Agriculture AI** – Will analyze geographic and climate data for crop recommendations.  
- **Voice Input & Output** – Will allow users to speak and listen to Arina for a hands-free experience.
- **Smooth Animations** – Includes enhanced UI experience with smooth transitions and effects.  
- **Hybrid AI (Local & Cloud)** – Runs both locally for offline usage and on the cloud for seamless accessibility. 


## Development Roadmap

Roadmap follows a structured plan, but continuous improvements and refinements are always ongoing.

- **Phase 0 (Current):** Core AI functionality with memory, search integration, and language adaptation.
- **Phase 1:** Enhancing AI contextual awareness and response quality.
- **Phase 2:** Business analysis with financial insights and report exports.
- **Phase 3:** POM-QM decision support with operations research features.
- **Phase 4 (UNDER REVIEW):** Agriculture AI for crop suitability and sustainability analysis.
- **Phase 5:** UI/UX refinements and frontend improvements.
- **Phase 6:** Making the server online for global access.
- **Exploratory Phase:** Blockchain integration & utility token implementation.

## Blockchain Integration

Arina AI is integrating blockchain to enhance data security, decentralization, and user control over stored information. This integration ensures that users have **secure, transparent, and verifiable** access to their data while maintaining **efficiency and scalability**.

### **Why Blockchain?**
- **Decentralized & Secure** – User data can be stored in an encrypted, tamper-proof environment.
- **User Ownership** – Provides users with full control over their data, ensuring transparency and privacy.
- **Seamless Access** – Blockchain integration allows for efficient management of AI interactions while maintaining performance.

This approach enables **a hybrid AI model**, combining the flexibility of local execution with the security and scalability of blockchain technology.

**Note:** The blockchain integration is designed to enhance accessibility and security without imposing staking requirements.

## Target Users

Arina AI is designed for:
- **Students & Researchers** – Learn AI concepts, conduct POM-QM case studies, and improve research efficiency.
- **Business Analysts & Industry Professionals** – Gain real-time insights, optimize operations, and enhance decision-making with AI.

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
   ollama pull gemma2  # You can replace 'gemma2' with any compatible AI model
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
