# CompanyHunter Project TODO List

## Job Search Features

- [x] Find jobs in specific areas
  - [x] Support multiple area search
  - [x] Integrate with larger job search system
- [ ] Job site integration
  - [ ] Implement blacklist for results
  - [x] Add autofill functionality
- [ ] Office space search (OpenStreetMaps)
  - [ ] Implement company blacklist (excluding government embassies)
  - [ ] Find contact information
    - [ ] Web crawler for company websites
    - [ ] Email discovery
      - [ ] Pattern matching for email addresses
      - [ ] Recruitment email identification
      - [ ] Automated application submission
        - [ ] AI-powered application customization

## Autofill Project

### Overview

The autofill system will help users automatically fill out job application forms by learning from common form patterns and user input.

### Implementation Steps

1. Create user CV input form
2. Develop flexible dictionary system
   - Map different terminology across job sites
   - Train model to recognize equivalent fields
   - Handle variations in form structure

### Technical Requirements

- Pattern recognition for form fields
- Flexible mapping system
- User data storage and management
- Cross-platform compatibility