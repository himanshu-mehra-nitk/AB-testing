import ProductCard_headphones from "./ProductCard_headphones";
import axios from "axios";
import { useState } from "react";
import Results from "./Results";

const HeadphoneSection = () => {
  const [response, setResponse] = useState(null);
  const headphone_2k_5k = [
    {
      id: 1,
      name: "HD 400s",
      brand: "Sennheiser",
      price: "₹3,990",
      image: "/HD 400s.jpg",
      specs: {
        Frequency_Range: "18Hz - 20KHz",
        ConnectivityTechnology: "Wired",
        Ear_Placement: "Over Ear",
        Impedance: "18 Ohm",
      },
    },
    {
      id: 2,
      name: "Tune 520BT",
      brand: "JBL",
      price: "₹3,499",
      image: "/Tune 520BT.jpg",
      specs: {
        Frequency_Range: "20Hz - 20KHz",
        ConnectivityTechnology: "Wireless",
        Ear_Placement: "On Ear",
        Impedance: "30 Ohm",
      },
    },
    {
      id: 3,
      name: "PC 8 USB A",
      brand: "EPOS",
      price: "₹2,725",
      image: "/PC 8 USB A.jpg",
      specs: {
        Frequency_Range: "20Hz - 20KHz",
        ConnectivityTechnology: "Wired",
        Ear_Placement: "On Ear",
        Impedance: "32 Ohm",
      },
    },
    {
      id: 4,
      name: "Rockerz 550",
      brand: "boAt",
      price: "₹1,499",
      image: "/Rockerz 550.jpg",
      specs: {
        Frequency_Range: "20Hz - 20KHz",
        ConnectivityTechnology: "Wireless",
        Ear_Placement: "Over Ear",
        Impedance: "16 Ohm",
      },
    },
  ];


  const handleCompare = async (section, priceSegment) => {
    try {
      // Example data to send
      const payload = {
        section: section, // "headphones"
        priceSegment: priceSegment, // Ex: "2000-5000"
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
      {/* First segment of headphones (2-5k)  */}
      <div>
        <div className="text-xl font-semibold text-slate-900 mb-8 flex items-center">
          <span className="w-3 h-3 bg-blue-600 rounded-full mr-3"></span>
          2k - 5k Headphones
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {headphone_2k_5k.map((headphone) => (
            <ProductCard_headphones
              key={headphone.id}
              product={headphone}
              type="headphone"
            />
          ))}
        </div>
        {/* Compare Button */}
        <div className="max-w-7xl mx-auto my-8 flex justify-center">
          <button
            onClick={() => handleCompare("headphones", "2000-5000")}
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

export default HeadphoneSection;
