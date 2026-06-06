# Sakhi

Sakhi is a full-stack web application built to provide support, resources, and a secure reporting platform for women facing cyber harassment. The core of the application is an AI-powered conversational assistant (Sakhi) that offers guidance on reporting procedures, emotional support, and actionable advice tailored to each user's situation.

## Features

- **AI Chat Assistant**: A context-aware conversational AI powered by Google Gemini, acting as a supportive and knowledgeable companion.
- **Secure Reporting System**: A dedicated portal to securely file cyber harassment reports, complete with file upload capabilities for evidence.
- **Admin Dashboard**: A secure, passcode-protected interface for administrators to review, manage, and update the status of submitted reports.
- **Modern UI**: A responsive, accessible, and calming "glassmorphism" design built with Tailwind CSS.
- **Robust Authentication**: JWT-based secure authentication for user accounts and chat history retention.

## Tech Stack

**Frontend**
- React 19 + TypeScript
- Vite (Build Tool)
- Tailwind CSS (Styling)
- React Router (Navigation)
- React Markdown (Rich text rendering)

**Backend**
- Python 3.11+
- FastAPI (High-performance web framework)
- SQLAlchemy + SQLite (ORM and Database)
- Google Generative AI SDK (Gemini Integration)
- bcrypt + python-jose (Security & JWT)

---

## Local Development Setup

To run Sakhi locally, you'll need to set up both the frontend and the backend. The project uses `concurrently` to make running the entire stack as simple as possible.

### Prerequisites
- [Node.js](https://nodejs.org/) (v20 or newer)
- [Python](https://www.python.org/) (v3.11 or newer)

### 1. Environment Configuration

1. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/yourusername/sakhi.git
   cd sakhi
   ```

2. Create a `.env` file in the root directory. You can copy the template:
   ```bash
   cp .env.example .env
   ```

3. Open `.env` and fill in the required variables, most importantly your Google Gemini API key:
   ```env
   # Get yours at: https://aistudio.google.com/apikey
   GEMINI_API_KEY=your_actual_api_key_here

   # Generate a random secret for JWT signing
   JWT_SECRET_KEY=your_secure_random_string

   # The passcode required to access the /admin dashboard
   VITE_ADMIN_PASSCODE=your_admin_passcode
   ```

### 2. Backend Setup

You need to create a Python virtual environment and install the FastAPI dependencies.

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Return to root directory
cd ..
```

### 3. Frontend Setup & Running the App

Once your Python environment is ready, install the Node dependencies and start the app.

```bash
# Install frontend dependencies
npm install

# Start both the frontend and backend servers simultaneously
npm run dev:full
```

- The React frontend will be available at: `http://localhost:5173`
- The FastAPI backend will be running at: `http://localhost:8000`
- The auto-generated Swagger API documentation will be at: `http://localhost:8000/docs`

---

## Production Deployment

Sakhi is designed to be deployed as a decoupled application:

### Frontend (Vercel)
The React frontend is optimized for zero-config deployment on [Vercel](https://vercel.com).
1. Import your GitHub repository into Vercel.
2. Vercel will automatically detect the Vite build settings.
3. In the Vercel dashboard, add your environment variables (`VITE_API_URL` pointing to your backend, and `VITE_ADMIN_PASSCODE`).
4. The included `vercel.json` file ensures that React Router works correctly on page refreshes.

### Backend (Render)
The FastAPI backend can be easily deployed as a Web Service on [Render](https://render.com).
1. Create a New Web Service connected to your repository.
2. Set the Root Directory to `backend`.
3. Set the Build Command to `pip install -r requirements.txt`.
4. Set the Start Command to `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`.
5. Add your environment variables (`GEMINI_API_KEY`, `JWT_SECRET_KEY`, and set `FRONTEND_URL` to your live Vercel domain to secure CORS).

---

## License

This project is licensed under the MIT License.