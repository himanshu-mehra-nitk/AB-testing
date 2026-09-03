import ProductCard from "./ProductCard";
import axios from "axios";
import { useState } from "react";
import Results from "./Results";

const MobileSection = () => {
  const [response, setResponse] = useState(null);
  const mobiles_20k_30k = [
    {
      id: 1,
      name: "IQOO Neo 10R 5G",
      brand: "IQOO",
      price: "₹26,998",
      image: "/IQOO Neo 10R 5G.jpg",
      specs: {
        os: "Funtouch OS 15",
        ram: "8 GB",
        storage: "256 GB",
        processor: "Snapdragon 8s Gen 3",
      },
    },
    {
      id: 2,
      name: "realme 15 5G",
      brand: "Realme",
      price: "₹25,999",
      image: "/realme 15 5G.jpg",
      specs: {
        os: "Android 15",
        ram: "8 GB",
        storage: "128 GB",
        processor: "Dimensity 7300 Plus",
      },
    },
    {
      id: 3,
      name: "Samsung Galaxy A35 5G",
      brand: "Samsung",
      price: "₹19,385",
      image: "/Samsung Galaxy A35 5G.jpg",
      specs: {
        os: "Android 14",
        ram: "8 GB",
        storage: "128 GB",
        processor: "Samsung Exynos 1380",
      },
    },
    {
      id: 4,
      name: "Xiaomi 14 CIVI",
      brand: "Xiaomi",
      price: "₹29,249",
      image: "/Xiaomi 14 CIVI.jpg",
      specs: {
        os: "Xiaomi HyperOS",
        ram: "12 GB",
        storage: "512 GB",
        processor: "Snapdragon 8s Gen 3",
      },
    },
  ];

  const mobiles_60k_70k = [
    {
      id: 1,
      name: "iPhone 16 128 GB",
      brand: "Apple",
      price: "₹66,900",
      image: "/iPhone 16 128 GB.jpg",
      specs: {
        os: "iOS",
        ram: "128 GB",
        storage: "128 GB",
        processor: "Apple A18",
      },
    },
    {
      id: 2,
      name: "Samsung Galaxy Z Flip6",
      brand: "Samsung",
      price: "₹68,970",
      image: "/Samsung Galaxy Z Flip6.jpg",
      specs: {
        os: "Android 14",
        ram: "12 GB",
        storage: "256 GB",
        processor: "Snapdragon",
      },
    },
    {
      id: 3,
      name: "OnePlus 13",
      brand: "OnePlus",
      price: "₹63,999",
      image: "/OnePlus 13.jpg",
      specs: {
        os: "Android 15, OxygenOS",
        ram: "12 GB",
        storage: "256 GB",
        processor: "Snapdragon 8 Elite",
      },
    },
    {
      id: 4,
      name: "Google Pixel 10 5G",
      brand: "Google",
      price: "₹70,320",
      image: "/Google Pixel 10 5G.jpg",
      specs: {
        os: "Android 16",
        ram: "12 GB",
        storage: "256 GB",
        processor: "Google Tensor",
      },
    },
  ];

  const handleCompare = async (section, priceSegment) => {
    try {
      // Example data to send
      const payload = {
        section: section, // "mobile"
        priceSegment: priceSegment, // Ex: "20000-30000"
      };

      const res = await axios.post("http://127.0.0.1:8000/results", payload);

      // set response null if previous comparison exists
      setResponse(null);

      console.log("Response from backend:", res.data); // handle results here

      setResponse(res.data);
      console.log("Response state updated:", response);
      alert("Comparison Successful! Check console for response");
    } catch (error) {
      console.error("Error while comparing:", error);
      alert("Something went wrong!");
    }
  };

  return (
    <>
      {/* First segment of mobiles (20-30k)  */}
      <div>
        <div className="text-xl font-semibold text-slate-900 mb-8 flex items-center">
          <span className="w-3 h-3 bg-blue-600 rounded-full mr-3"></span>
          20k - 30k Mobile Devices
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {mobiles_20k_30k.map((mobile) => (
            <ProductCard key={mobile.id} product={mobile} type="mobile" />
          ))}
        </div>
        {/* Compare Button */}
        <div className="max-w-7xl mx-auto my-8 flex justify-center">
          <button
            onClick={() => handleCompare("mobiles", "20000-30000")}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-all duration-200 transform hover:scale-105 hover:cursor-pointer active:scale-95 shadow-lg"
          >
            Compare
          </button>
        </div>
        {/* results section  */}
        {response ? (
          <div className="max-w-7xl mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
            <h3 className="text-2xl font-bold mb-4">Comparison Results:</h3>
            <pre className="bg-slate-100 p-4 rounded-lg overflow-x-auto">
              {JSON.stringify(response, null, 2)}
            </pre>
            <Results data={response} />
          </div>
        ) : (
          <div className="text-center font-semibold">
            Click on the compare button to see the results......
          </div>
        )}
      </div>

      {/* Second segment of mobiles (60-70k) */}
      <div>
        <div className="text-xl font-semibold text-slate-900 mb-8 flex items-center">
          <span className="w-3 h-3 bg-blue-600 rounded-full mr-3"></span>
          60k - 70k Mobile Devices
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {mobiles_60k_70k.map((mobile) => (
            <ProductCard key={mobile.id} product={mobile} type="mobile" />
          ))}
        </div>
        {/* Compare Button */}
        <div className="max-w-7xl mx-auto my-8 flex justify-center">
          <button
            onClick={() => handleCompare("mobiles", "60000-70000")}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-all duration-200 transform hover:scale-105 hover:cursor-pointer active:scale-95 shadow-lg"
          >
            Compare
          </button>
        </div>
        {/* results section  */}
        {response ? (
          <div className="max-w-7xl mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
            <h3 className="text-2xl font-bold mb-4">Comparison Results:</h3>
            <pre className="bg-slate-100 p-4 rounded-lg overflow-x-auto">
              {JSON.stringify(response, null, 2)}
            </pre>
            <Results data={response} />
          </div>
        ) : (
          <div className="text-center font-semibold">
            Click on the compare button to see the results......
          </div>
        )}
      </div>
    </>
  );
};

export default MobileSection;
