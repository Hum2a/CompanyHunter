# CompanyHunter 🎯

<div align="center">

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=for-the-badge&logo=appveyor)](https://github.com/yourusername/CompanyHunter/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge&logo=appveyor)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.0%2B-blue?style=for-the-badge&logo=react)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/flask-2.0%2B-red?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)

</div>

<div align="center">
  <img src="https://i.imgur.com/placeholder-for-screenshot.png" alt="CompanyHunter Screenshot" width="800">
  <br>
  <em>Find your dream job with our advanced multi-API job search platform</em>
</div>

## ✨ Features

<details>
<summary>Click to expand features</summary>

| Feature | Description | Status |
|---------|-------------|--------|
| 🔄 Multi-API Integration | Aggregates job listings from Adzuna, Reed, Indeed, and more | ✅ |
| 🗺️ Interactive Map | Visualize job locations using Google Maps | ✅ |
| 🔍 Advanced Filtering | Filter by job category, job type, and distance | ✅ |
| 🎨 Modern UI | Sleek design with animations powered by Framer Motion | ✅ |
| 🏢 Company Info | View detailed company information and metadata | ✅ |
| 📱 Responsive Design | Works on desktop and mobile devices | ✅ |

</details>

## 🚀 Technology Stack

### Frontend
<div align="center">

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.0+ | UI Framework |
| Framer Motion | Latest | Animations |
| Google Maps API | Latest | Map Integration |
| Styled Components | Latest | CSS-in-JS |

</div>

### Backend
<div align="center">

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Backend Language |
| Flask | 2.0+ | Web Framework |
| aiohttp | Latest | Async HTTP Client |
| SQLAlchemy | Latest | Database ORM |

</div>

## 📋 Prerequisites

<details>
<summary>System Requirements</summary>

- Node.js (v14+)
- Python (v3.9+)
- API keys for the services:
  - Google Maps API key
  - Adzuna API credentials
  - Reed API key (optional)
  - Indeed Publisher ID (optional)

</details>

## 🔧 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/CompanyHunter.git
cd CompanyHunter
```

### 2️⃣ Backend Setup
```bash
cd server
pip install -r requirements.txt

# Create .env file with your API keys
touch .env
```

<details>
<summary>Backend Environment Variables</summary>

```env
# Required
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_API_KEY=your_adzuna_api_key

# Optional
REED_API_KEY=your_reed_api_key
INDEED_PUBLISHER_ID=your_indeed_publisher_id
```

</details>

### 3️⃣ Frontend Setup
```bash
cd client
npm install

# Create .env file for frontend
touch .env
```

<details>
<summary>Frontend Environment Variables</summary>

```env
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
REACT_APP_API_URL=http://localhost:5000
```

</details>

## 🚀 Running the Application

### Backend Server
```bash
cd server
python app.py
```

### Frontend Development Server
```bash
cd client
npm start
```

> The application will be available at [http://localhost:3000](http://localhost:3000)

## 📖 How to Use

<details>
<summary>User Guide</summary>

1. **Search for Jobs** 🔍
   - Enter a location (city, address, or postal code)
   - Set a search radius using the slider
   - Click "Search Jobs"

2. **Filter Results** ⚙️
   - Use the Filter Options panel to filter by job category and job type
   - Selected filters will be displayed as tags

3. **View Job Details** 📄
   - Click on a job card to view detailed information
   - Job location is displayed on the map

4. **Save Favorites** ⭐
   - Click the "Save" button on a job to save it to your favorites

</details>

## 📁 Project Structure

```plaintext
CompanyHunter/
├── client/                  # React frontend
│   ├── public/              # Static files
│   └── src/                 # Source files
│       ├── components/      # React components
│       └── App.js           # Main application component
│
└── server/                  # Flask backend
    ├── api_connectors/      # API connector modules
    │   ├── adzuna_connector.py
    │   ├── reed_connector.py
    │   ├── indeed_connector.py
    │   ├── google_jobs_connector.py
    │   └── aggregator.py    # Job aggregation logic
    ├── app.py               # Flask application
    └── requirements.txt     # Python dependencies
```

## 🔜 Future Enhancements

<details>
<summary>Planned Features</summary>

- [ ] User authentication and saved job management
- [ ] Email notifications for new job matches
- [ ] Enhanced company profiles with reviews and ratings
- [ ] Salary insights and comparisons
- [ ] Application tracking system
- [ ] AI-powered job matching
- [ ] Resume builder and optimization
- [ ] Interview preparation tools

</details>

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

<div align="center">

| Technology | Link |
|------------|------|
| React | [reactjs.org](https://reactjs.org/) |
| Flask | [flask.palletsprojects.com](https://flask.palletsprojects.com/) |
| Google Maps | [developers.google.com/maps](https://developers.google.com/maps) |
| Adzuna API | [developer.adzuna.com](https://developer.adzuna.com/) |
| Reed API | [reed.co.uk/developers](https://www.reed.co.uk/developers/jobseeker) |
| Indeed API | [developer.indeed.com](https://developer.indeed.com/) |
| Framer Motion | [framer.com/motion/](https://www.framer.com/motion/) |

</div>

---

<div align="center">

Made with ❤️ by [Your Name](https://github.com/yourusername)

[![GitHub followers](https://img.shields.io/github/followers/yourusername?style=social)](https://github.com/yourusername)
[![Twitter Follow](https://img.shields.io/twitter/follow/yourusername?style=social)](https://twitter.com/yourusername)

</div>