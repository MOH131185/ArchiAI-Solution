# ArchiAI Solution

An AI-powered architectural design system that can create full projects in 2D and 3D with structural and MEP details.

## Features

- **Climate-Aware Design**: Automatically detects climate and seasonal weather patterns based on location
- **Architectural Style Detection**: Analyzes local architectural styles and integrates them into designs
- **3D Surrounding Visualization**: Shows 3D view of surrounding area for context
- **Multi-Project Support**: Handles various project types (houses, hospitals, commercial buildings, etc.)
- **Portfolio Integration**: Allows architects to upload and use their design portfolios
- **AI Design Engine**: Generates complete 2D and 3D designs with structural and MEP details
- **Text-Based Modification**: Modify designs using natural language commands
- **Multi-Format Export**: Export to various architecture software formats
- **Cost Estimation**: Generate detailed cost estimates in Excel format

## Technology Stack

- **Backend**: Python with FastAPI
- **AI/ML**: TensorFlow, PyTorch, OpenAI GPT
- **3D Graphics**: Three.js, WebGL
- **Climate Data**: OpenWeatherMap API, Climate.gov
- **Maps**: Google Maps API, OpenStreetMap
- **Database**: PostgreSQL with PostGIS
- **Frontend**: React with TypeScript
- **Export**: AutoCAD API, Revit API, SketchUp API

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Start the backend server:
```bash
python main.py
```

2. Open the web interface at `http://localhost:3000`

3. Enter project location and requirements
4. Upload portfolio (optional)
5. Generate AI design
6. Modify using text commands
7. Export to desired format
8. Generate cost estimation

## Project Structure

```
├── backend/           # FastAPI backend
├── frontend/         # React frontend
├── ai_models/        # AI/ML models
├── data/            # Data storage
├── exports/         # Export modules
└── docs/            # Documentation
```
# ArchiAI-Solution
