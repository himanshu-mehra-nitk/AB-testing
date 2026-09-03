import React from "react";

function Results({ data }) {
  if (!data)
    return <p className="text-center mt-10 text-gray-500">No results yet...</p>;

  const {
    top_performing_product,
    product_rankings,
    key_insights,
    roi_analysis,
    cost_efficiency,
  } = data;

  return (
    <div className="p-8 space-y-10">
      {/* Top Product Highlight */}
      <div className="bg-gray-900 text-white p-6 rounded-xl shadow-lg">
        <h2 className="text-2xl font-bold mb-3">🎯 Top Performing Product</h2>
        <p className="text-lg">
          <span className="font-semibold">{top_performing_product?.name}</span>
        </p>
        <p className="text-sm mt-1">
          Score: {top_performing_product?.score.toFixed(3)}
        </p>
        <p className="text-sm">
          Improvement over {top_performing_product?.second_best}:{" "}
          {top_performing_product?.improvement_over_second.toFixed(2)}%
        </p>
      </div>

      {/* Rankings Table */}
      <div>
        <h3 className="text-xl font-semibold mb-4">📊 Product Rankings</h3>
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-200 text-left">
              <th className="p-3">Rank</th>
              <th className="p-3">Product</th>
              <th className="p-3">Score</th>
            </tr>
          </thead>
          <tbody>
            {product_rankings?.map((item) => (
              <tr key={item.rank} className="border-b hover:bg-gray-50">
                <td className="p-3">{item.rank}</td>
                <td className="p-3">{item.product}</td>
                <td className="p-3">{item.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Key Insights */}
      <div>
        <h3 className="text-xl font-semibold mb-4">
          🔍 Key Insights (Conversion Funnel)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {key_insights?.map((item) => (
            <div key={item.product} className="p-5 rounded-lg border shadow-sm">
              <h4 className="font-semibold mb-2">{item.product}</h4>
              <p>CTR: {(item.CTR * 100).toFixed(2)}%</p>
              <p>
                View Content Rate: {(item.View_Content_Rate * 100).toFixed(2)}%
              </p>
              <p>
                Add to Cart Rate: {(item.Add_to_Cart_Rate * 100).toFixed(2)}%
              </p>
              <p>Purchase Rate: {(item.Purchase_Rate * 100).toFixed(2)}%</p>
            </div>
          ))}
        </div>
      </div>

      {/* ROI Comparison */}
      <div>
        <h3 className="text-xl font-semibold mb-4">💰 ROI Analysis</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {roi_analysis?.map((item) => (
            <div key={item.product} className="p-5 rounded-lg border shadow-sm">
              <h4 className="font-semibold">{item.product}</h4>
              <p>ROI: {item.ROI.toFixed(2)}%</p>
            </div>
          ))}
        </div>
      </div>

      {/* Cost Efficiency */}
      <div>
        <h3 className="text-xl font-semibold mb-4">
          🛒 Cost Efficiency (Cost Per Purchase)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {cost_efficiency?.map((item) => (
            <div key={item.product} className="p-5 rounded-lg border shadow-sm">
              <h4 className="font-semibold">{item.product}</h4>
              <p>Cost per Purchase: ${item.cost_per_purchase.toFixed(2)}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Campaign Recommendations */}
      <div>
        <h3 className="text-xl font-semibold mb-4">
          🎯 Campaign Budget Recommendations
        </h3>

        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="bg-gray-200 text-left">
              <th className="p-3">Campaign</th>
              <th className="p-3">Current Spend</th>
              <th className="p-3">Optimal Spend</th>
              <th className="p-3">Change</th>
              <th className="p-3">Revenue Forecast</th>
              <th className="p-3">Model R²</th>
              <th className="p-3">Recommendation</th>
            </tr>
          </thead>

          <tbody>
            {data.campaign_recommendations?.map((item) => {
              const spend = item.spend;
              const revenue = item.revenue;

              return (
                <tr key={item.campaign} className="border-b hover:bg-gray-50">
                  <td className="p-3 font-semibold">{item.campaign}</td>

                  <td className="p-3">${spend.current_avg_spend.toFixed(2)}</td>
                  <td className="p-3">${spend.optimal_spend.toFixed(2)}</td>

                  {/* color-coded improvement */}
                  <td
                    className={`p-3 font-medium ${
                      spend.improvement_pct > 0
                        ? "text-green-600"
                        : spend.improvement_pct < 0
                        ? "text-red-600"
                        : "text-gray-600"
                    }`}
                  >
                    {spend.improvement_pct.toFixed(2)}%
                  </td>

                  <td className="p-3">
                    ${revenue.historical_avg_revenue.toFixed(0)} → $
                    {revenue.forecast_avg_revenue.toFixed(0)}
                  </td>

                  <td className="p-3">
                    <span className="block">
                      Spend R²: {spend.r2.toFixed(2)}
                    </span>
                    <span className="block">
                      Revenue R²: {revenue.r2.toFixed(2)}
                    </span>
                  </td>

                  {/* Recommendation badge */}
                  <td className="p-3">
                    <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
                      {item.recommendation}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Results;
