# CompanyHunter

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A modern job search platform that aggregates listings from multiple APIs to help you find your dream job. CompanyHunter combines data from Adzuna, Reed, Indeed, and more to provide a comprehensive job search experience with an interactive map interface.

<p align="center">
  <img src="https://i.imgur.com/placeholder-for-screenshot.png" alt="CompanyHunter Screenshot" width="800">
  <br>
  <em>Note: Replace with actual screenshot of your application</em>
</p>

## ✨ Features

- **Multi-API Integration**: Aggregates job listings from Adzuna, Reed, Indeed, and more
- **Interactive Map Interface**: Visualize job locations using Google Maps
- **Advanced Filtering**: Filter by job category, job type, and distance
- **Modern UI**: Sleek design with animations powered by Framer Motion
- **Company Information**: View detailed company information and metadata
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Technology Stack

### Frontend
- React 
- Framer Motion for animations
- Google Maps API integration
- CSS with modern design principles

### Backend
- Python with Flask
- Async API connectors using aiohttp
- Job data standardization and deduplication
- Geocoding with Google Maps API

## 📋 Prerequisites

Before you begin, ensure you have the following:
- Node.js (v14+)
- Python (v3.9+)
- API keys for the services:
  - Google Maps API key
  - Adzuna API credentials
  - Reed API key (optional)
  - Indeed Publisher ID (optional)

## 🔧 Installation

### Clone the repository
```bash
git clone https://github.com/yourusername/CompanyHunter.git
cd CompanyHunter
```

### Backend Setup
```bash
cd server
pip install -r requirements.txt

# Create .env file with your API keys
touch .env
```

Add the following to your `.env` file:
```
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_API_KEY=your_adzuna_api_key
REED_API_KEY=your_reed_api_key
INDEED_PUBLISHER_ID=your_indeed_publisher_id
```

### Frontend Setup
```bash
cd client
npm install

# Create .env file for frontend
touch .env
```

Add the following to your client `.env` file:
```
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
REACT_APP_API_URL=http://localhost:5000
```

## 🚀 Running the Application

### Start the Backend Server
```bash
cd server
python app.py
```

### Start the Frontend Development Server
```bash
cd client
npm start
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## 📖 How to Use

1. **Search for Jobs**:
   - Enter a location (city, address, or postal code)
   - Set a search radius using the slider
   - Click "Search Jobs"

2. **Filter Results**:
   - Use the Filter Options panel to filter by job category and job type
   - Selected filters will be displayed as tags

3. **View Job Details**:
   - Click on a job card to view detailed information
   - Job location is displayed on the map

4. **Save Favorites**:
   - Click the "Save" button on a job to save it to your favorites

## 📁 Project Structure

```
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

- User authentication and saved job management
- Email notifications for new job matches
- Enhanced company profiles with reviews and ratings
- Salary insights and comparisons
- Application tracking system

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [React](https://reactjs.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Google Maps Platform](https://developers.google.com/maps)
- [Adzuna API](https://developer.adzuna.com/)
- [Reed API](https://www.reed.co.uk/developers/jobseeker)
- [Indeed API](https://developer.indeed.com/)
- [Framer Motion](https://www.framer.com/motion/)