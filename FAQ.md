# Frequently Asked Questions

## General Questions

### What is CompanyHunter?
CompanyHunter is an advanced job search platform that aggregates listings from multiple APIs (Adzuna, Reed, Indeed) to provide a comprehensive job search experience with an interactive map interface.

### Is CompanyHunter free to use?
Yes, CompanyHunter is completely free to use. We don't charge users for accessing job listings or using our platform.

### What APIs does CompanyHunter use?
We currently integrate with:
- Adzuna API
- Reed API
- Indeed API
- Google Maps API (for location services)

## Technical Questions

### What are the system requirements?
- Node.js v14 or higher
- Python 3.9 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### How do I set up the development environment?
See our [Contributing Guide](CONTRIBUTING.md) for detailed setup instructions.

### How do I report a bug?
Please open an issue on our GitHub repository with:
1. A clear description of the bug
2. Steps to reproduce
3. Expected vs actual behavior
4. Screenshots if applicable

## API Integration

### How do I get API keys?
- Adzuna: [Sign up here](https://developer.adzuna.com/)
- Reed: [Apply here](https://www.reed.co.uk/developers/jobseeker)
- Indeed: [Register here](https://developer.indeed.com/)
- Google Maps: [Get API key](https://developers.google.com/maps)

### Are there rate limits?
Yes, each API has its own rate limits:
- Adzuna: 1000 requests/day
- Reed: 500 requests/day
- Indeed: 1000 requests/day
- Google Maps: Varies by service

## Features

### How does the map interface work?
The map interface uses Google Maps to:
- Display job locations
- Calculate distances
- Show company information
- Provide directions

### Can I save job searches?
Yes, you can:
- Save favorite jobs
- Create custom search filters
- Set up job alerts

### Is there a mobile app?
Not yet, but our web application is fully responsive and works on all devices.

## Troubleshooting

### The map isn't loading
1. Check your Google Maps API key
2. Ensure you have internet connectivity
3. Clear your browser cache
4. Try a different browser

### Jobs aren't showing up
1. Verify your API keys are correct
2. Check your search parameters
3. Ensure you're within rate limits
4. Try a different location

### The application is slow
1. Check your internet connection
2. Clear browser cache
3. Try reducing the search radius
4. Use fewer filters

## Contributing

### How can I contribute?
See our [Contributing Guide](CONTRIBUTING.md) for details on:
- Setting up the development environment
- Making code contributions
- Submitting pull requests
- Reporting issues

### What's the code style?
We follow:
- PEP 8 for Python
- ESLint for JavaScript
- Prettier for code formatting

## Legal

### What's your privacy policy?
See our [Privacy Policy](PRIVACY.md) for details on how we handle user data.

### What's your terms of service?
See our [Terms of Service](TERMS.md) for usage guidelines and limitations.

---

*Last updated: March 20, 2023* 