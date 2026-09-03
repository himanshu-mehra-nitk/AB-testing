const ProductCard = ({ product, type }) => {
  return (
    <div className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300 border border-slate-200">
      {/* Image Container */}
      <div className="h-[330px] bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center overflow-hidden">
        <img
          src={product.image || "/placeholder.svg"}
          alt={product.name}
          className="w-full h-full object-cover"
        />
      </div>

      {/* Content Container */}
      <div className="p-6">
        {/* Brand */}
        <p className="text-sm font-semibold text-blue-600 uppercase tracking-wide mb-2">
          {product.brand}
        </p>

        {/* Product Name */}
        <h3 className="text-lg font-bold text-slate-900 mb-3 line-clamp-2">
          {product.name}
        </h3>

        {/* Price */}
        <p className="text-2xl font-bold text-slate-900 mb-4">
          {product.price}
        </p>

        {/* Specs */}
        <div className="space-y-2 border-t border-slate-200 pt-4">
          <div className="flex justify-between text-sm">
            <span className="text-slate-600">Frequency Range:</span>
            <span className="font-semibold text-slate-900">
              {product.specs.Frequency_Range}
            </span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-600">Connectivity Technology:</span>
            <span className="font-semibold text-slate-900">
              {product.specs.ConnectivityTechnology}
            </span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-600">Ear Placement:</span>
            <span className="font-semibold text-slate-900">
              {product.specs.Ear_Placement}
            </span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-600">Impedance:</span>
            <span className="font-semibold text-slate-900">
              {product.specs.Impedance}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
