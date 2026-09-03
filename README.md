# A/B Testing — Marketing Campaign Analysis

A full-stack tool for analyzing and comparing the performance of multiple ad
campaigns (laptops, mobiles, and headphones) within specific price segments.
It applies statistical hypothesis testing and machine learning to campaign
metrics like spend, impressions, clicks, and conversions, and surfaces
data-driven recommendations through a React frontend.

## Features

- Compare multiple product campaigns within a chosen category and price segment
- Statistical significance testing (t-test, Mann-Whitney U, ANOVA, Kruskal-Wallis, Shapiro-Wilk)
- Predictive modeling with Random Forest and XGBoost regressors
- Metrics analyzed: Spend, Impressions, Reach, Clicks, Searches, View Content,
  Add to Cart, Purchases, CTR, and Conversion Rate
- Simple web UI to pick a category/price segment and view recommendations

## Tech Stack

**Backend:** FastAPI, pandas, NumPy, scikit-learn, XGBoost, SciPy, Seaborn/Matplotlib
**Frontend:** React 19, Vite, Tailwind CSS, Axios

## Project Structure

```
.
├── backend/
│   ├── app.py                     # FastAPI entrypoint / API routes
│   ├── analysis.py                # Core analysis & ML logic
│   ├── laptops_60k-90k.csv
│   ├── laptops_110k-130k.csv
│   ├── mobiles_20k-30k.csv
│   ├── mobiles_60k-70k.csv
│   └── headphones_2k-5k.csv
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── components/            # Section & result components
    │   └── main.jsx
    ├── index.html
    └── package.json
```

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Backend setup

```bash
cd backend
python -m venv venv

# Activate the virtual environment
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

Start the API server:

```bash
uvicorn app:app --reload
```

The backend runs at `http://127.0.0.1:8000`.

### 3. Frontend setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The app runs at `http://localhost:5173`. Open it in your browser — make sure
the backend is running at the same time, since the frontend calls it directly.

## How It Works

1. The user selects a product category (laptops, mobiles, or headphones) and
   a price segment from the UI.
2. The frontend sends a `POST /results` request to the backend with the
   selected `section` and `priceSegment`.
3. `analysis.py` loads the matching CSV dataset, cleans it, groups it by
   campaign, runs statistical tests to check for significant differences
   between campaigns, and trains regression models to identify which metrics
   most influence conversions.
4. The backend returns recommendations, which the frontend renders for the user.

## API

### `POST /results`

**Request body:**
```json
{
  "section": "laptops",
  "priceSegment": "60000-90000"
}
```

**Response:** A list of recommendations based on the statistical and ML analysis
of the corresponding dataset.

Supported combinations:

| Section    | Price Segment    |
|------------|------------------|
| laptops    | 60000-90000      |
| laptops    | 110000-130000    |
| mobiles    | 20000-30000      |
| mobiles    | 60000-70000       |
| headphones | 2000-5000        |

## Roadmap / Ideas

- [ ] Add more product categories and price segments
- [ ] Deploy backend and frontend
- [ ] Add unit tests for `analysis.py`
- [ ] Visualize statistical test results directly in the UI

## License

Add your preferred license here (e.g., MIT).
