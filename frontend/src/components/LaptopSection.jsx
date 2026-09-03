import ProductCard from "./ProductCard";
import { useState } from "react";
import Results from "./Results";
import axios from "axios";

const LaptopSection = () => {
  const [response, setResponse] = useState(null);
  const laptops_60k_90k = [
    {
      id: 1,
      name: "Apple MacBook Air M2",
      brand: "Apple",
      price: "₹75,490",
      image: "/MacBook Air M2.jpg",
      specs: {
        os: "Mac OS",
        ram: "16 GB",
        storage: "256 GB SSD",
        processor: "Apple M2",
      },
    },
    {
      id: 2,
      name: "ASUS Vivobook S 14 Flip",
      brand: "ASUS",
      price: "₹72,990",
      image: "/ASUS Vivobook S 14 Flip.jpg",
      specs: {
        os: "Windows 11",
        ram: "16 GB",
        storage: "512 GB SSD",
        processor: "Intel Core Ultra 5",
      },
    },
    {
      id: 3,
      name: "HP Pavilion Gaming",
      brand: "HP",
      price: "₹64,990",
      image: "/HP Pavilion Gaming.webp",
      specs: {
        os: "Windows 11",
        ram: "8 GB",
        storage: "512 GB SSD",
        processor: "AMD integrated SoC",
      },
    },
    {
      id: 4,
      name: "Lenovo Ideapad Gaming 3",
      brand: "Lenovo",
      price: "₹67,995",
      image: "/Lenovo Ideapad Gaming 3.jpg",
      specs: {
        os: "Windows 11",
        ram: "16 GB",
        storage: "512 GB SSD",
        processor: "Intel Core i5",
      },
    },
  ];

  const laptops_110k_130k = [
    {
      id: 1,
      name: "Apple 2025 MacBook Air",
      brand: "Apple",
      price: "₹1,19,900",
      image: "/Apple 2025 MacBook Air.jpg",
      specs: {
        os: "macOS Sonoma",
        ram: "16 GB",
        storage: "256 GB SSD",
        processor: "Apple M2",
      },
    },
    {
      id: 2,
      name: "HP Omen",
      brand: "HP",
      price: "₹1,27,990",
      image: "/HP Omen.jpg",
      specs: {
        os: "Windows 11",
        ram: "16 GB",
        storage: "1 TB HDD",
        processor: "Intel Core i7",
      },
    },
    {
      id: 3,
      name: "Legion 5 Gen 10",
      brand: "Lenovo",
      price: "₹1,22,990",
      image: "/Legion 5 Gen 10.jpg",
      specs: {
        os: "Windows 11",
        ram: "24 GB",
        storage: "512 GB SSD",
        processor: "Intel Core i7",
      },
    },
    {
      id: 4,
      name: "Lenovo LOQ Gen 10",
      brand: "Lenovo",
      price: "₹1,24,990",
      image: "/Lenovo LOQ Gen 10.jpg",
      specs: {
        os: "Windows 11 Pro",
        ram: "16 GB",
        storage: "512 GB SSD",
        processor: "Intel i7-1365U",
      },
    },
  ];

  const handleCompare = async (section, priceSegment) => {
    try {
      // Example data to send
      const payload = {
        section: section, // "laptop"
        priceSegment: priceSegment, // Ex: "20000-30000"
      };

      const res = await axios.post("http://127.0.0.1:8000/results", payload);

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
      {/* First price segment - 60k-90k */}
      <div>
        <div className="text-xl font-semibold text-slate-900 mb-8 flex items-center">
          <span className="w-3 h-3 bg-purple-600 rounded-full mr-3"></span>
          60k - 90k Laptops
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {laptops_60k_90k.map((laptop) => (
            <ProductCard key={laptop.id} product={laptop} type="laptop" />
          ))}
        </div>
        {/* Compare Button */}
        <div className="max-w-7xl mx-auto my-8 flex justify-center">
          <button
            onClick={() => handleCompare("laptops", "60000-90000")}
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

      {/* Second price segment - 110k-130k */}
      <div>
        <div className="text-xl font-semibold text-slate-900 mb-8 flex items-center">
          <span className="w-3 h-3 bg-purple-600 rounded-full mr-3"></span>
          110k - 130k Laptops
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {laptops_110k_130k.map((laptop) => (
            <ProductCard key={laptop.id} product={laptop} type="laptop" />
          ))}
        </div>
        {/* Compare Button */}
        <div className="max-w-7xl mx-auto my-8 flex justify-center">
          <button
            onClick={() => handleCompare("laptops", "110000-130000")}
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

export default LaptopSection;
