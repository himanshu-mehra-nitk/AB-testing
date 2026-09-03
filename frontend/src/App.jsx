import MobileSection from "./components/MobileSection";
import LaptopSection from "./components/LaptopSection";
import HeadphoneSection from "./components/HeadphoneSection";

export default function App() {
  const handleCompare = () => {
    console.log("Compare button clicked - printed");
    alert("Compare button clicked - dummy action");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12 px-4 md:px-8">
      {/* Header */}
      <header className="max-w-7xl mx-auto mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-3">
          Tech Comparison Hub
        </h1>
        <p className="text-lg text-slate-600">
          Compare the latest mobiles and laptops side by side
        </p>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto space-y-16">
        {/* Mobile Section */}
        <section>
          <h2 className="text-3xl font-bold text-slate-900 mb-8 flex items-center">
            <span className="w-2 h-8 bg-blue-600 rounded mr-3"></span>
            Mobile Devices
          </h2>
          <MobileSection />
        </section>

        {/* Laptop Section */}
        <section>
          <h2 className="text-3xl font-bold text-slate-900 mb-8 flex items-center">
            <span className="w-2 h-8 bg-purple-600 rounded mr-3"></span>
            Laptops
          </h2>
          <LaptopSection />
        </section>

        {/* Headphone Section */}
        <section>
          <h2 className="text-3xl font-bold text-slate-900 mb-8 flex items-center">
            <span className="w-2 h-8 bg-purple-600 rounded mr-3"></span>
            Headphones
          </h2>
          <HeadphoneSection />
        </section>
      </div>
    </div>
  );
}
